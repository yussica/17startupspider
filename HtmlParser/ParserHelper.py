# -*- coding: utf-8 *-
'''
Created on 2013-1-29

@author: white
'''

from pyquery import PyQuery as pq
from lxml import etree
import urllib
from ParseModel import Company, CEO
import urllib2

class ParserHelper(object):
    '''
    classdocs
    '''

    def __init__(self, email, pwd):
        '''
        Constructor
        '''
        self.DoLogin(email, pwd)
        self.timeout = 3

    def doParse(self):
        uri = 'http://www.17startup.com/location'
        url = urllib2.urlopen(uri, timeout = self.timeout)
        d = pq(url.read().decode('utf-8'))
        p = d(".grid_12 p")
        for c in p.children():
            a = pq(c)
            print(a.text())
    
    def UnitTest(self, cid):
        try:
            page = 1
            uri = "http://www.17startup.com/startup/location/{0}?page={1}".format(cid, page + 1)
            url = urllib2.urlopen(uri, timeout = self.timeout)
            location = pq(url.read().decode('utf-8'))
            companies = location(".startup-one-col")
            nIndex = 1
            for c in companies.children():
                li = pq(c)
                c_name = li("h4 a").text()
                team_url = li("h4 a").attr["href"]
                company = self.getCompanyDetail(team_url, c_name)
                #print("{0}. {1}".format(page * 10 + nIndex, c_name))
                print("{0}. {1}".format(page * 10 + nIndex, company.ToString()))
                nIndex += 1
                #break
        except Exception as e:
            print(e)
            #self.getCompanyList(cid, start)
    
    def getCompanyList(self, cid, start = -1):
        try:
            totalpages = self.getTotalPages(cid)
            if start > -1:
                totalpages = start + 1
                csvfile = open("D:/{0}-{1}.csv".format(cid, start + 1), "w+")
            else:
                start = 0
                csvfile = open("D:/{0}.csv".format(cid, start), "w+")
            
            for page in range(start, totalpages):
                uri = "http://www.17startup.com/startup/location/{0}?page={1}".format(cid, page + 1)
                url = urllib2.urlopen(uri, timeout = self.timeout)
                location = pq(url.read().decode('utf-8'))
                companies = location(".startup-one-col")
                nIndex = 1
                for c in companies.children():
                    li = pq(c)
                    c_name = li("h4 a").text()
                    team_url = li("h4 a").attr["href"]
                    company = self.getCompanyDetail(team_url, c_name)
                    csvfile.write(company.ToString())
                    csvfile.write("\n")
                    print("{0}. {1}".format(page * 10 + nIndex, c_name))
                    nIndex += 1
            
            #csvfile.close()
        except Exception as e:
            print("getCompanyList connect failed")
            self.getCompanyList(cid, start)
    
    def getCompanyDetail(self, url, name):
        detailcontent = ""
        try:
            request = urllib2.urlopen(url, timeout = self.timeout)
            detail = pq(request.read().decode('utf-8'))
            title = detail(".grid_8 h1").remove(".less-important").text()
            dr = pq(detail(".grid_8 .startup-right").html())
            d_website = dr("p").eq(0).remove(".less-important").find("a").attr["href"].lstrip().rstrip()
            d_state = dr("p").eq(1).remove(".less-important").html().lstrip().rstrip()
            d_category = dr("p").eq(2).remove(".less-important").html().lstrip().rstrip()
            d_location = dr("p").eq(3).remove(".less-important").html().lstrip().rstrip()
            d_teams = dr("p").eq(4).remove(".less-important").text().lstrip().rstrip()
            d_ceo = ""
            ceoList = []
            ceos = d_teams.split(' ')
            ceocount = len(ceos)
            if ceocount > 0:
                for ceo in ceos:
                    cs = ceo.split('/')
                    if len(cs) == 2:
                        ceoList.append(self.getCEO(cs[0], name))
            else:
                pass
            d_finance = dr("p").eq(5).remove(".less-important").html().lstrip().rstrip()
            d_rating = dr("p").eq(6).remove(".less-important").html().lstrip().rstrip()
            d_description = dr("p").eq(7).remove(".less-important").html().lstrip().rstrip()
            detailcontent = "{0},{1},{2},{3}".format(url, title, d_website, d_ceo)
            detailcontent = Company(",", url, name, d_website, d_state, d_category, d_location, d_teams, ceoList, d_finance, d_rating, d_description)
        except Exception as e:
            print("getCompanyDetail connect failed")
            detailcontent = self.getCompanyDetail(url, name)
        return detailcontent
    
    def getTotalPages(self, cid):
        uri = "http://www.17startup.com/startup/location/{0}".format(cid)
        url = urllib2.urlopen(uri, timeout = self.timeout)
        pages = pq(url.read().decode('utf-8'))
        lastpage = pages(".pagination li:last").prev().text();
        import string
        return string.atoi(lastpage)
    
    def getCEO(self, name, company):
        c_url = ""
        c_name = ""
        c_email = ""
        c_weibo = ""
        try:
            uri = "http://www.17startup.com/search/people?keyword={0}".format(name.encode("utf-8"))
            c_url = uri
            people = self.getPeople(uri)
            if people.hasClass("people-right"):
                c_name = people(".people-right").children().eq(0).remove(".less-important").text()
                c_email = people(".people-right").children().eq(2).remove(".less-important").text()
                c_weibo = people(".people-right").children().eq(3).remove(".less-important").text()
            else:
                childrenlen = len(people(".people-one-col-grid li").children())
                for c in range(childrenlen):
                    li = pq(people(".people-one-col-grid li").eq(c).html())
                    if li.html() == None:
                        break
                    p_name = li("p a").text().replace(".", "")
                    if company.find(p_name) != -1:
                        uri = li("a").attr["href"]
                        response = urllib2.urlopen(uri)
                        c_url = uri
                        s_people = pq(response.read().decode("utf-8"))(".grid_8")
                        c_name = s_people(".people-right").children().eq(0).remove(".less-important").text()
                        c_email = s_people(".people-right").children().eq(2).remove(".less-important").text()
                        c_weibo = s_people(".people-right").children().eq(3).remove(".less-important").text()
        except Exception as e:
            print("getCompanyDetail connect failed")
            ceo = self.getCEO(name, company)
            c_url = ceo.url
            c_name = ceo.name
            c_email = ceo.email
            c_weibo = ceo.weibo

        return CEO(c_url, c_name, c_email, c_weibo)
    
    def getPeople(self, url):
        try:
            response = urllib2.urlopen(url, timeout = self.timeout)
            people = pq(response.read().decode("utf-8"))(".grid_8")
            return people
        except Exception as e:
            print("getPeople connect failed")
            return self.getPeople(url)
        return None
    
    def DoLogin(self, email, pwd):
        import cookielib
        
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        urllib2.urlopen("http://www.17startup.com/user/login")
        headers = { 
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17",
                   }
        postData = { "email": email, "password": pwd }
        
        request = urllib2.Request("http://www.17startup.com/user/login", urllib.urlencode(postData), headers)
        urllib2.urlopen(request)
        
if __name__ == '__main__':
    email = "331253025@qq.com"
    pwd = "123qwe"
    startup = ParserHelper(email, pwd)
    #startup.getCompanyList(25)
    #for i in range(94, 129):
        #startup.getCompanyList(25, i)
    startup.getCompanyList(2)
    #startup.getCompanyList(25, 0)
    #startup.UnitTest(25)
    #startup.UnitTest(2)
    
    print("OK")
    #startup.getCompanyDetail("http://17startup.com/startup/view/199", "DoCute")


