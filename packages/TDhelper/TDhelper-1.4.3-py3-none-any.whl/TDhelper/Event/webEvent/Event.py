#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-
'''
@File    :   Event.py
@Time    :   2020/09/29 22:07:04
@Author  :   Tang Jing 
@Version :   1.0.0
@Contact :   yeihizhi@163.com
@License :   (C)Copyright 2020
@Desc    :   None
'''

# here put the import lib
import json
import logging
from TDhelper.network.http.REST_HTTP import GET, POST
from TDhelper.reflect import reflect
# code start


class Manager:
    def __init__(self, service_uri, platformKey: str):
        self._event_service_uri = service_uri  # 事件服务地址
        self._event_cache = {}  # 事件缓存
        self._platform = platformKey
        self._handleName= ''
        self._getRemoteEventRelation()

    def _getRemoteEventRelation(self):
        if not self._event_cache:
            if self._event_service_uri.find('/', len(self._event_service_uri)-1) > -1:
                self._event_service_uri+'/'
            m_uri = self._event_service_uri + \
                "events/?plateform=%s" % self._platform
            try:
                state, body = GET(m_uri, time_out=15)
                if state == 200:
                    ret = json.loads(str(body, encoding='utf-8'))
                    if ret['state'] == 200:
                        self._event_cache = ret['msg']
                else:
                    logging.error('access %s error. code(%s), body(%s)' %
                                (m_uri, state, body))
            except Exception as e:
                logging.error(e)

    def handleRegister(self, name, key, description, params):
        # todo register handle
        pass

    def triggerRegister(self, name: str, section: str, sync: bool = False, systemEvent: bool = False, handle: int = None):
        # todo register trigger
        pass

    def trigger(self,func):
        def wapper(*args, **kwargs):
            self._handleName = func.__qualname__.replace('.', '_').upper()
            self.on(self._handleName, "BEFORE", *args, **kwargs)
            ret = func(*args, **kwargs)
            kwargs['func_results'] = ret
            self.on(self._handleName, "COMPLETE", *args, **kwargs)
            return ret
        return wapper

    def on(self, handle, event, *args, **kwargs):
        if not handle:
            handle= self._handleName
        m_event = handle.upper() + "." + event.upper()
        if handle in self._event_cache:
            for item in self._event_cache[handle][m_event]:
                self._call_router(item)
        else:
            logging.error("%s can not found trigger handle." % m_event)
        return False
        
    def _call_router(self,item):
        '''
            event trigger router
        '''
        m_type= item['handleType'].upper()
        if m_type == 'MICROSERVICES':
            return self._api_call(item)
        elif m_type == 'LOCATION':
            return self._location_call(item)
        elif m_type == 'RPC':
            return self._rpc_call(item)
        else:
            logging.error("%s handle type is error."%item['key'])
            return None

    def _location_call(self,item):
        '''
            location moudle call
        '''
        extendPath= item["extendPath"]
        m_handle= item["callHandle"]
        m_params= item["params"]
        m_checkedState= item["checkedState"]
        pass

    def _rpc_call(self,item):
        '''
            rpc service moudle call
        '''
        pass

    def _api_call(self,item):
        '''
            RestFul api call
        '''
        pass

ss = Manager("http://192.168.0.100:8006/api/", 'WEB')


class WEB:
    @ss.trigger
    def REGISTER(self,i):
        '''
            http headers.
        '''
        print(i)
        return 'ccc', True
    def ccc(self):
        '''
        http headers
        '''
        return True

class test():
    def __init__(self):
        pass
    def cc(self, i=1):
        print(i)

def WEB_REGISTER(id=0):
    #ss.on('WEB_REGISTER','BEFORE', id=0)
    print(id)
    
if __name__ == "__main__":
    #ddd = WEB()
    #ddd.REGISTER(1)
    #print("--------------------------")
    #gggg()
    #ddd=test("http://192.168.0.100:8006/api/","WEB")
    #ddd.cc()
    ss.trigger(WEB_REGISTER)(5)