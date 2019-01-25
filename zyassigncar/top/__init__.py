'''
Created on 2012-6-29

@author: lihao
'''
from top.api.base import sign



class appinfo(object):
    def __init__(self, appkey, secret):
        self.appkey = 'dingvxnfusu3gjclrcm8'
        self.secret = 'KL4k0u70sJMo5gn-yTId5C2FewdHMM3Fk5zSKctZkZTP1mMtk5fCxnOoD1BoUVlM'
        
def getDefaultAppInfo():
    pass

     
def setDefaultAppInfo(appkey,secret):
    default = appinfo(appkey,secret)
    global getDefaultAppInfo 
    getDefaultAppInfo = lambda: default
    




    

