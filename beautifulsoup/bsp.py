from bs4 import BeautifulSoup,ResultSet,Tag
from requests import get
import pandas as pd

class BSPlus:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    my_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS\
            X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/71.0.3578.98 Safari/537.36", \
            "Accept":"text/html,application/xhtml+xml,application/xml;\
            q=0.9,image/webp,image/apng,*/*;q=0.8"}
    bs_result : BeautifulSoup

    def __init__(self,url):
        resp = get(url=url,headers=BSPlus.my_headers)
        self.bs_result=BeautifulSoup(markup=resp.content,features='html5lib')

    def get_all_tables(self)->pd.DataFrame:
        tables:ResultSet[Tag] = self.bs_result.find_all(name='table')

        result_tables=[]
        for index,table in enumerate(tables):
            
            current_table = []
            for index,row in enumerate(table.find_all('tr')):
                row : Tag
                current_row = []
                for data in row.find_all('td'):
                    data : Tag
                    current_row.append(data.text)
                current_table.append(current_row)
            result_tables.append(pd.DataFrame(current_table))
        return result_tables