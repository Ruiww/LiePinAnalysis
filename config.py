#mongoDB
import random

mongo_url = 'localhost'
mongo_DB = 'LiePin'
mongo_table = 'LiePin_Analysis'


#请求头参数
user_Agent = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
]

ua = random.choice(user_Agent)
#print(ua)

hds = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'__uuid=1507945036987.90; gr_user_id=6b0e0234-ac4c-4cf6-8165-d26cbef2901d; user_kind=0; \
is_lp_user=true; c_flag=57f42656143009d84cf45c0d686280a5; new_user=false; WebImPageId=webim_pageid_364027361196.51575;\
 _fecdn_=1; fe_download_tips=true; city_site=bj.liepin.com; verifycode=86b4588df1c040dea596018c8003fff6; abtest=0;\
  JSESSIONID=7B4237C881EE38DF21BABD7B830E179E; __tlog=1508066212265.73%7C00000000%7CR000000075%7C00000000%7C00000000;\
   __session_seq=54; __uv_seq=315; gr_session_id_bad1b2d9162fab1f80dde1897f7a2972=b5a2b0a7-66d1-421a-b505-a4aeccd698ba; \
   Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1508031834,1508036562,1508054968,1508066212; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200\
   =1508074703',
'Host':'www.liepin.com',
'Referer':'https://www.liepin.com/zhaopin/?&jobTitles=&fromSearchBtn=2&ckid=66b9b401d4cbc8f3&d_=&isAnalysis=true&&init=-1&\
searchType=1&dqs=010&industryType=industry_01&jobKind=2&&&degradeFlag=1&industries=040&salary=100$999&&&key=\
%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&headckid=1df6064fb78a4c7c&d_pageSize=40&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EJC8W0LLXNSaYEa5s\
-pFFNQ&d_headId=7afc6ea79fd6b57ff64af3acaa62a467&d_ckId=2a62b38677d7ed1e7c0a0cd919475b0b&d_sfrom=search_unknown&d_&curPage=1',
'Upgrade-Insecure-Requests':'1',
'User-Agent':ua
}
#print(hds)


