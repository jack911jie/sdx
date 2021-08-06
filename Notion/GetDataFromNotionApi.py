import os
import sys

from numpy import save
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'modules'))
import readConfig 
import requests
import re
import json
import time
import pandas as pd

class NotionApi:
    def __init__(self):
        self.token='secret_UKfTBbr16loEWvcq7ZUXtzxIturJJ2yK3EFdcB2JhIt'
        config=readConfig.readConfig(os.path.join(os.path.dirname(__file__),'config','Notion.config'))
        self.output_dir=config['输出文件夹']

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
        print('\n正在连接Notion服务器获取数据……',end='')
        txt=self.get_notion(id=id)
        print('完成')        
        print('\n正在处理数据……',end='')
        dat=json.loads(txt)
        # print(dat)
        res_out=[]        
        for result in dat['results']:
            out=Vividict()
            res_merge=[]
            for property in result['properties']:
                if property=='活动时间':
                    value=result['properties'][property]['date']['start']
                    out[property]=value
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
        print('完成')
        return res_out


    def exp_waterbill(self,id,save_name='notion_waterbill',save_format='csv'):        
        res=self.get_waterbill(id=id)
        df=pd.DataFrame(res)        

        # df=pd.read_csv('d:\\temp\\sdx\\notion_waterbill.csv',converters={'类型': eval,'姓名':eval})
        df['姓名']=df['姓名'].apply(lambda x:','.join(x))
        df['类型']=df['类型'].apply(lambda x:','.join(x))

        print('\n正在导出{}文件……'.format(save_format),end='')
        # df.to_csv(save_name,index=None)
        save_name=os.path.join(self.output_dir,save_name+'.'+save_format)
        if save_format=='csv':
            df.to_csv(save_name,index=None)
        if save_format=='xlsx':
            df.to_excel(save_name,index=None)
        # print(df)
        print('完成')

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
                

if __name__=='__main__':    
    id=['2e240480dd03486c8fa4fc7781da0ef2','database_query']
    notion=NotionApi()
    # res=notion.get_waterbill(id=id)
    # print(res)
    notion.exp_waterbill(id=id,save_name='notiton_export',save_format='xlsx')

    
