# -*- coding: utf-8 *-
'''
Created on 2013-1-29

@author: zyc
'''

class Company(object):
    '''
    Company Model
    '''
    
    def __init__(self, splite = ",", url = "", name = "", website = "", state = "", category = "", location = "", teams = "", ceos = [], finance = "", rating = "", description = ""):
        self.url = url
        self.name = name
        self.website = website
        self.state = state
        self.category = category
        self.location = location
        self.teams = teams
        self.ceos = ceos
        self.finance = finance
        self.rating = rating
        self.description = description
        self.split = splite
    
    def ToString(self):
        lpCEO = ""
        if len(self.ceos) > 0:
            for ceo in self.ceos:
                if "" == lpCEO:
                    lpCEO = "{1}{0}{2}{0}{3}".format(self.split, ceo.name, ceo.email, ceo.weibo)
                else:
                    lpCEO = "{1}{0}{2}{0}{3}{0}{4}".format(self.split, lpCEO, ceo.name, ceo.email, ceo.weibo)
        else:
            lpCEO = "暂无"
        
        lpString = "{1}{0}{2}{0}{3}{0}{4}".format(self.split, self.url, self.name, self.website, lpCEO).encode("gbk")
        return lpString

class CEO(object):
    '''
    CEO Model
    '''

    def __init__(self, url = "", name = "", email = "", weibo = ""):
        '''
        Constructor
        '''
        self.url = url
        self.name = name
        self.email = email
        self.weibo = weibo