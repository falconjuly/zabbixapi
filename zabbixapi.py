import urllib2
try:
    import simplejson as json
except:
    import json

class ZabbixAPIException(Exception):
    pass

class ZabbixTool():
    __id = 0
    __auth = ''
    def __init__(self, url, user, password):
        self.__url = 'http://'+url.rstrip('/') + '/zabbix/api_jsonrpc.php'
        self.__user = user
        self.__password = password
        self.template = []

    def json_obj(self, method, params):
        obj = {'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'id': self.__id}
        if method != 'user.login':
            obj['auth'] = self.__auth
        return json.dumps(obj)

    def post_request(self, json_obj):
        headers = {'Content-Type': 'application/json-rpc',
                   'User-Agent': 'python/zabbix_api'}
        req = urllib2.Request(self.__url, json_obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        self.__id += 1
        return content

    def login(self):
        user_info = {'user': self.__user,
                     'password': self.__password}
        obj = self.json_obj('user.login', user_info)
        try:
            content = self.post_request(obj)
        except urllib2.HTTPError:
            raise ZabbixAPIException("Zabbix URL Error")
        try:
            self.__auth = content['result']
            print self.__auth
        except KeyError, e:
            e = content['error']['data']
            raise ZabbixAPIException(e)

    def data_get(self,method,element,t_list=None):
        e_list = element.split()
        t_list = []
        r_list = []
        template_info = {
            'output': 'extend',
            'filter'  : {
                'host' : t_list
            }
        }
        obj = self.json_obj(method,template_info)
        try:
            content = self.post_request(obj)
        except urllib2.HTTPError:
            raise ZabbixAPIException("Zabbix URL Error")
        for element in e_list:
            try:
                resault = content['result'][0][element]
                print resault
                r_list.append(str(resault))
                print r_list
            except IndexError,e:
                raise  ZabbixAPIException('templated didnot found')
            except KeyError, e:
                e = content['error']['data']
                raise ZabbixAPIException(e)

    


test = ZabbixTool(url='xxx.xxx.xxx.xxx',user='Admin',password='zabbix')
test.login()
test.data_get('template.get','templateid','Template App FTP Service')
test.data_get('host.get','hostid','LegacyRTAP03401FW001')
