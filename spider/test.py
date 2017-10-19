'''
import re
from LiePinSpider.spider import *
def parse_detail_page(industry,detail_html):
    title = detail_html('.about-position .title-info h1').text()
    company = detail_html('.about-position .title-info h3').text()
    salary = detail_html('.about-position .job-title-left .job-item-title').text()#.split()[0]
    position = detail_html('.about-position .job-title-left .basic-infor span').text()
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
    industry = industry
    #正则表达式查找行业：
    #industry_detail_word = re.compile('<div.*?side.*?<ul.*?new-compintro.*?行业.*?<a.*?>(.*?)</a>',re.S)
    #industry_detail = re.search(industry_detail_word, detail_html)[0]
    industry_detail = detail_html('.right-blcok-post .new-compintro li:nth-child(1)').text()
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
        'industry_detail':industry_detail,
        'companySize':companySize,
        'comAddress':comAddress,
        'is_end':is_end
    }
    return data

url = 'https://www.liepin.com/job/198902156.shtml'
#url = 'https://www.liepin.com/a/9869247.shtml?imscid=R000000075&ckid=48e3c029e131d6cc&headckid=d43987dce3efb676&pageNo=0&pageIdx1&totalIdx=1&sup=1?d_pageSize=40&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EQ7DjKP-w9G5PIDCunOOBWQ&d_headId=ff3b412c67f72ee60d0c4b422850e3fc&d_ckId=0958da443ebfc8dd488a45a8ea9597b5&d_sfrom=search_unknown&d_curPage=0&d_posi=1'
html = detail_page_html(url)
a = parse_detail_page('sdf',html)
print(a)
'''
import pymysql
dfs = 'dddff'
ds = 'dddss'

database = 'mysql'
host = 'localhost'
user = 'root'
key = 'awr159753bnm'
mysqlDB = 'LiePinData'
# 打开数据库连接
db = pymysql.connect(host, user, key, mysqlDB)
# 使用cursor()方法获取操作游标
cursor = db.cursor()
if database == 'mysql':
    #sql = "INSERT INTO liepin3(`JobTitle`,`company`,`salary`,`position`,`PubTime`,`qualification`,`tag_list`,\
    #    `description`,`industry`,`industry_detail`,`companySize`,`comAddress`,`is_end`) \
     #   VALUES ('%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%d' )" % \
     #         ('df','sdf','df','er','er','er','er','er','er','er','er','we',1)
    sql = """CREATE TABLE `liepin32` (
            `JobTitle` CHAR,
            `company` CHAR,
            )"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()