import requests
import pymongo
import time
from LiePinSpider.config import hds, mongo_url, mongo_DB, mongo_table
from pyquery import PyQuery as pq

#mongDB初始化
client = pymongo.MongoClient(mongo_url)
mongoDB = client[mongo_DB]
#停止变量,使用该变量作为停止网页解析并跳出循环记号
global stopvalue
stopvalue = 0

#获取索引页
def index_page_html(index_url):
    try:
        response = requests.get(index_url,headers = hds,timeout = 5)
        time.sleep(3)
        html = pq(response.text)
        print('解析索引页:',index_url)
        return html
    except Exception:
        print('get index Failed')
        index_page_html(index_url)

#解析索引页：获取详情页urllist
def get_detail_url(index_html):
    selector = '.sojob-list li'# .job-info h3 a'
    detail_url_list = []
    for item in index_html(selector).items():
        #出现降级搜索代码，后面的内容是不想要的，因此跳出循环，并停止获取下一页
        if item('.downgrade-search'):
            stopvalue = 1
            break
        else:
            detail_url = item('.job-info h3 a').attr.href
            if detail_url.find('https://www.liepin.com/job/') >= 0:
                detail_url_list.append(detail_url)
            else:
                pass
    return detail_url_list

#解析indexpage获取下一页url
def get_next_page_url(index_html):
    try:
        selector = '.job-content .sojob-result .pagerbar a'
        items = index_html(selector).items()
        if items:
            next_page_url = ''
            for item in items:
                if item.text() == '下一页':
                    if item.attr('class') != 'disabled':
                        next_page_url = 'https://www.liepin.com' + item.attr.href
                    else:
                        next_page_url = None
        else:
            next_page_url = None
        return next_page_url
    except Exception:
        print('get next page failed')
        get_next_page_url(index_html)

#解析索引页：获取行业urllist
def get_industry_url(index_page_html):
    industry_lis = index_page_html('.search-conditions .short-dd li')
    industry_url = {}
    for li in industry_lis.items():
        print('industry',li('span').text())
        for a in li('.sub-industry a').items():
            industry_url[a.text()] = 'https://www.liepin.com' + a.attr.href
            print('sub-industry',a.text())
            print(industry_url[a.text()])
    return industry_url

# sojob > div.container.sojob-search > form > div.wrap > div > div.search-conditions > dl:nth-child(1) > dd > ul > li:nth-child(1) > div


#获取详情页
def detail_page_html(detail_url):
    try:
        response = requests.get(detail_url, headers=hds,timeout = 5)
        time.sleep(3)
        html = pq(response.text)
        return html
    except Exception:
        print('get detail page failed')
        detail_page_html(detail_url)

#解析详情页
def parse_detail_page(detail_html):
    title = detail_html('.about-position .title-info h1').text()
    company = detail_html('.about-position .title-info h3 a').text()
    salary = detail_html('.about-position .job-item .job-item-title').text().split()[0]
    position = detail_html('.about-position .job-item .basic-infor span a').text()
    # 发布时间
    time = detail_html('.about-position .job-item .basic-infor time').attr('title')
    # 学历、工作、语言、年龄,
    #education = detail_html('.about-position .job-item .job-qualifications span:nth-child(1)').text()
    #work_experience = detail_html('.about-position .job-item .job-qualifications span:nth-child(2)').text()
    #language = detail_html('.about-position .job-item .job-qualifications span:nth-child(3)').text()
    #age = detail_html('.about-position .job-item .job-qualifications span:nth-child(4)').text()
    #四项不一定全部存在
    qualification = detail_html('.about-position .job-item .job-qualifications span').text()

    # 标签列表
    tag_list = []
    lis = detail_html('div.tag-list span').items()
    for li in lis:
        tag_list.append(li.text())
    # 职位描述
    description = detail_html('.about-position div:nth-child(3) .content').text()
    #industry有两种格式，一种为行业，一种为领域/融资，数据清洗时注意
    industry = detail_html('.right-blcok-post .new-compintro li:nth-child(1)').text()
    companySize = detail_html('.right-blcok-post .new-compintro li:nth-child(2)').text()[5:]
    comAddress = detail_html('.right-blcok-post .new-compintro li:nth-child(3)').text()[5:]
    #判断职位是否已结束
    if detail_html('.title-info label').text() == '该职位已结束':
        is_end = 1
    else:
        is_end = 0
    data = {
        'JobTitle':title,
        'company':company,
        'salary':salary,
        'position':position,
        'PubTime':time,
        #'education':education,
        #'work_experience':work_experience,
        #'language':language,
        #'age':age,
        'qualification':qualification,
        'tag_list':tag_list,
        'description':description,
        'industry':industry,
        'companySize':companySize,
        'comAddress':comAddress,
        'is_end':is_end
    }
    return data

#保存数据至mongoDB
def save_to_mongo(data):
    try:
        if mongoDB[mongo_table].insert(data):
            print('保存成功',data)
            return  True
    except Exception:
        print('Failed')

#解析详情+获取下一页并解析下一页的详情直到nextpage=None
def parse_detail_savedata_rollpage(url):
    html = index_page_html(url)
    #获取当前index详情页url
    detail_url_list = get_detail_url(html)
    #解析当前index每一个详情页，并保存数据
    for url in detail_url_list:
        print('解析详情页:',url)
        #detail_html = detail_page_html(url)
        #data = parse_detail_page(detail_html)
        #data['url'] = url
        #存入mongoDB
        #save_to_mongo(data)

    #nextPage回调
    #出现降级搜索代码，后面的内容是不想要的，因此跳出循环，并停止获取下一页
    if stopvalue != 1:
        next_page = get_next_page_url(html)
        #print(next_page)
        if next_page != None:
            parse_detail_savedata_rollpage(next_page)


def industry_ergodic(url):
    html = index_page_html(url)
    industry_url_list = get_industry_url(html)
    for industry in industry_url_list.keys():
        print('解析行业:',industry)
        industry_url = industry_url_list[industry]
        parse_detail_savedata_rollpage(industry_url)
    print('Complete！')

