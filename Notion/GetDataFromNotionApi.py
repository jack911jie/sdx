import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__),'config'))
import requests
import re
import json

class NotionApi:
    def __init__(self):
        self.token='secret_UKfTBbr16loEWvcq7ZUXtzxIturJJ2yK3EFdcB2JhIt'
        # self.id=id

    def id_format(self,id):
        if len(id[0])!=32:
            return id[0]
        else:
            return '-'.join([id[0][0:8],id[0][8:12],id[0][12:16],id[0][16:20],id[0][20:]])  

    def get_notion(self,id):
        # id=self.id
        id_type=id[1]
        # print(id_type)
        id=self.id_format(id)
        # print(id)
        token = self.token
        if id_type=='page':
            url_notion = 'https://api.notion.com/v1/pages/'+id
            method='GET'
        elif id_type=='block':
            url_notion = 'https://api.notion.com/v1/blocks/'+id+'/children?pagesize=1'
            method='GET'
        elif id_type=='database':
            url_notion='https://api.notion.com/v1/databases/'+id
            method='GET'
        elif id_type=='database_query':
            url_notion='https://api.notion.com/v1/databases/'+id+'/query'
            method='POST'
        else:
            print('id_type类型错误')
        
        # print(url_notion)

        r = requests.request(
                method=method,
                url=url_notion,
                headers={"Authorization": "Bearer " + token, "Notion-Version": "2021-05-13"},
            )
        # print(r.text)
        return r.text


    def get_cus_name(self,id):
        txt=self.get_notion(id=id)
        dat=json.loads(txt)
        # print(dat)
        cus_name=dat['properties']['客户姓名']['title'][0]['plain_text']
        return cus_name

    def get_waterbill(self,id):
        txt=self.get_notion(id=id)
        dat=json.loads(txt)
        res_out=[]
        out=Vividict()
        for result in dat['results']:
            res_merge=[]
            for property in result['properties']:
                if property=='活动时间':
                    value=result['properties'][property]['date']['start']
                if property=='价格':
                    value=result['properties'][property]['number']
                    out[property]=value
                if property=='时间及项目':
                    value=result['properties'][property]['title'][0]['plain_text']
                    out[property]=value
                if property=='类型':
                    act_types=[]
                    for num,act_type in enumerate(result['properties'][property]['multi_select']):
                        value=result['properties'][property]['multi_select'][num]['name']
                        act_types.append(value)
                    out[property]=act_types
                if property=='姓名':
                    cus_dat=[]
                    for num,cus in enumerate(result['properties'][property]['relation']):
                        value=result['properties'][property]['relation'][num]['id']
                        res=self.get_cus_name([value,'page'])
                        cus_dat.append(res)
                    out[property]=cus_dat
                
                
            res_out.append(out)
                
        return res_out


class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
                

if __name__=='__main__':    
    id=['2e240480dd03486c8fa4fc7781da0ef2','database_query']
    # notion=NotionApi()
    # res=notion.get_waterbill(id=id)
    t='''
[{'价格': 1500, '类型': ['拍摄'], '姓名': ['张三', '王大'], '时间及项目': '20210726花园'}, {'价格': 1500, '类型': ['拍摄'], '姓名': ['张三', '王大'], 
'时间及项目': '20210726花园'}, {'价格': 1500, '类型': ['拍摄'], '姓名': ['张三', '王大'], '时间及项目': '20210726花园'}, {'价格': 1500, '类型': ['拍摄
'], '姓名': ['张三', '王大'], '时间及项目': '20210726花园'}, {'价格': 1500, '类型': ['拍摄'], '姓名': ['张三', '王大'], '时间及项目': '20210726花园'}, {'价格': 1500, '类型': ['拍摄'], '姓名': ['张三', '王大'], '时间及项目': '20210726花园'}, {'价格': 1500, '类型': ['拍摄'], '姓名': ['张三', '王大'], 
'时间及项目': '20210726花园'}]
'''
    print(t)
    
