# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 14:07
# @Author  : Smilecoc
# @FileName: fuzzy mapping by fuzzywuzzy.py
# @Software: PyCharm
# @Comment : 利用fuzzywuzzy进行点位之间的模糊匹配

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

#将需要匹配的列表放入dataframe中并将需要匹配的信息拼起来
file_path=r"fuzzywuzzy test data.xlsx"
sp_rawdata=pd.read_excel(file_path,sheet_name='rawdata',index_col='sp_code')
sp_rawdata['text']=sp_rawdata['sp_webiste']+sp_rawdata['sp_channel']+sp_rawdata['sp_position']+sp_rawdata['sp_format']
tr_rawdata=pd.read_excel(file_path,sheet_name='addcode')
tr_rawdata['text']=tr_rawdata['tr_Website']+tr_rawdata['tr_Position_Channel']+tr_rawdata['tr_Format']

#获取dataframe中cacode所有的去重后的值，并以列表的形式返回，即去重操作
sp_listtype=sp_rawdata['cacode'].unique()
tr_listtype=tr_rawdata['cacode'].unique()

scorelist=[]
rawlist=[]
#df = pd.DataFrame(columns = ["cacode", "tr_campaign_name", "tr_Website", "tr_Position_Channel", "tr_Format"])
for i in sp_listtype:
    # isin()接受一个列表，判断该列中元素是否在列表中,再根据dataframe中的布尔索引进行筛选,类似的筛选函数还有 str.contains()
    #在本例中，这个语句将cacode中属于1,2,3的dataframe拆分成三个列表，从而匹配两个dataframe时只会匹配cacode相同的信息
    sp_data = sp_rawdata[sp_rawdata['cacode'].isin([i])]
    tr_data = tr_rawdata[tr_rawdata['cacode'].isin([i])]
    #按行取dataframe中的值
    for row in  tr_data.itertuples():
        rawlist.append(row)
    for text in tr_data['text']:
        score = process.extractOne(str(text), sp_data['text'].astype(str), scorer=fuzz.token_sort_ratio)
        scorelist.append(score)

#转换list为dataframe类型
scorecode=pd.DataFrame(scorelist)
df=pd.DataFrame(rawlist)
#修改转变后的dataframe的字段名称，注意这里0和1都不是字符串
scorecode=scorecode.rename(columns={0:'sp-text',1:'score',2:"add_sp_code"})
#两个dataframe相连，axis： 需要合并链接的轴，0是行，1是列，这里按照列拼接
result=pd.concat([df,scorecode],axis=1)
result.to_excel(r" fuzzy mapping result.xlsx",index=False)