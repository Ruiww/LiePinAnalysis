# [requests,pyquery]爬取猎聘网职位数据

为了获得数据分析相关岗位的地域分布、行业分布、薪酬以及要求技能等信息，编写爬虫对猎聘网职位信息进行爬取。未使用scrapy等爬虫框架，主要使用requests与pyquery获取与解析网页，使用multiprocessing实现多线程爬取。

请关注我的知乎专栏  [从零开始数据分析](https://zhuanlan.zhihu.com/zeroDataAnalysis)
共同努力，学习，成长

---

[TOC]

# 准备工作

1. 安装python，版本3.6
2. 安装requests，版本2.18.4
3. 安装pyquery，版本1.2.17
4. 安装pymongo，版本3.5.1
5. 安装PyMySql，版本0.7.11   

# 参考

[requests文档](http://www.python-requests.org/en/master/)：requests.get()用法，如何获取网页代码，添加headers

[pyquery API文档](http://pythonhosted.org/pyquery/api.html)：CSS筛选器方法

[pymongo 文档](http://api.mongodb.com/python/current/):mongoDB数据库对象初始化及数据存入方法

[Python3 MySQL 数据库连接](http://www.runoob.com/python3/python3-mysql.html):菜鸟教程中关于使用python3操作MySQL的介绍



# 实现流程

##嵌套循环

猎聘网搜索页面最多只显示前100页，因此分行业进行遍历。

遍历网页时嵌套三层循环：

* 遍历行业
* 遍历同一行业索引页
* 遍历同一索引页内所有职位详情页

## 流程图

```flow
s=>start: 开始
e=>end: 结束
IndustryList=>operation: 获取行业索引页url列表
getIndexPage=>operation: 获取索引页源代码
getNextPage=>operation: 获取下一页
getNextInd=>operation: 获取下一个行业索引页
getDetailPage=>operation: 获取职位详情页
getNextDetailPage=>operation: 获取下一个职位详情页
saveData=>operation: 保存职位信息
lastDetail?=>condition: 索引页最后一个职位?
lastIndexPage?=>condition: 最后一页？
lastInd?=>condition: 最后一个行业？
s->IndustryList->getIndexPage->getDetailPage->saveData->lastDetail?
lastDetail?(no)->getNextDetailPage(right)->saveData
lastDetail?(yes)->lastIndexPage?
lastIndexPage?(yes)->lastInd?
lastIndexPage?(no)->getNextPage(right)->getIndexPage
lastInd?(yes)->e
lastInd?(no)->getNextInd(right)->getIndexPage
```

# 代码解析

**`main.py`**  爬取开始代码，在其中可以修改想要爬取的职位搜索条件，以及爬取进程数等

**`spider.py`** 定义爬取过程中调用各种函数

**`config.py`** 配置参数文档，数据库相关参数及请求头（headers）可在其中修改



## main.py

定义起始页，确定运行线程数

使用for循环，调用spider（in spider.py）循环解析每个行业

* start_url : 爬虫起始网页，代码中使用筛选条件为 ‘全国 1个月内 企业职位 key=数据分析’对应页的url


## config.py

### MySQL参数

用于在python中创建MySQL连接，目前MySQL存储存在bug，尚未实现

```python
host = 'localhost'
user = 'pymysql'
key = 'pymysql'
mysqlDB = 'LiePin'
```

### mongoDB参数

用于mongoDB初始化

```python
mongo_url = 'localhost' 
mongo_DB = 'LiePin' 
mongo_table = 'LiePin_Analysis' 
```

### 请求头参数

获取网页时使用的请求头，'User-Agent'从Agent池中随机选用，模仿浏览器访问，避免被网站禁止连接

* user_Agent：list形式，保存多个用于请求头的User_Agent形成Agent池

* ua：随机获取user_Agent中一个字符串的值

  ```python
  ua = random.choice(user_Agent)
  ```

* hds：requests.get()调用的请求头

  ```python
  hds['User-Agent'] = ua
  ```



## spider.py

### index_page_html(industry,cur_page,industry_url)

返回索引页源代码

* industry_url：待解析的网页
* industry,cur_page：输入url对应页面搜索结果的行业与页码，debug时便于定位发生错误的网页

```python
import requests
import time
#TIPS:requests.get()添加headers参数，模拟浏览器访问，避免网页禁止访问
response = requests.get(index_url, headers=hds, timeout=5)
time.sleep(3) #暂停3s，避免过于频繁访问，导致爬虫被禁
```

### get_industry_url(start_page_html)

解析起始页源代码，返回各行业搜索结果索引页第一页的url

### get_next_page_url(industry,cur_page,index_html)

解析当前索引页，返回下一页的url，实现翻页

* index_html:当前索引页源代码
* industry,cur_page：当前索引页对应的行业与页码，debug时便于定位发生错误的网页

### get_detail_page_url(index_html)

解析索引页中包含的职位详情页url，返回索引页中所有详情页url组成的list及停止变量构成的元组

return tuple = （detail_url_list，stopvalue）

* detail_url_list：当前页所有职位详情页url列表
* stopvalue：default = 0，若索引页中出现降级搜索，则stopvalue = 1 => 降级搜索的职位不符合要求，停止对该行业职位爬取

```python
detail_url_list = []
stopvalue = 0
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
```

### get_detail_page_html(industry,cur_page,detail_page_url)

返回职位详情页源代码

### parse_detail_page(industry,detail_html)

解析职位详情页，返回字典形式的职位

* 重点：页面元素分析，CSS筛选器

```python
data = {
    'JobTitle':title, 
    'company':company,
    'salary':salary, # 'min-max万 XX天反馈'
    'position':position, # 工作地 
    'PubTime':pubtime, # 职位发布时间
    'qualification':qualification, # 学历、工作经验、语言、年龄
    'tag_list':tag_list, #职位标签，数量不定
    'description':description, # 职位描述，一段文字TEXT
    'industry':industry, #筛选界面的subindustry
    'industry_detail':industry_detail, #detailpage右侧标注的行业或领域
    'companySize':companySize,#公司人数
    'comAddress':comAddress,#地址
    'is_end':is_end # 职位是否已结束 0:False,1:True
}
```

### save_to_mongo(industry,cur_page,i,url,data)

保存数据至mongoDB

* industry, cur_page , i , url : 定位保存的职位，i 是该职位在其索引页上的排序

```python
import pymongo
from config.py import mongo_url,mongo_DB,mongo_table
#初始化mongoDB
client = pymongo.MongoClient(mongo_url)#数据库连接
db = client[mongo_DB]#数据库
table = db[mongo_table]#数据表
#存入数据
db[mongo_table].insert(data)
```

### loop_detail_page(industry,cur_page,detail_page_url_list)

遍历某一索引页下所有职位详情页，保存职位信息

* industry,cur_page：哪一行业的哪一页，定位参数，debug时方便定位
* detail_page_url_list：get_detail_page_url获得的详情页url列表

### loop_all_page(cur_page,industry,index_html)

函数内调用loop_detail_page，保存职位信息

若存在下一页，循环调用loop_all_page，实现翻页功能

```python
#判断是否出现降级搜索：Y-->stop,N-->next_page
    if stopvalue != 1:
        next_page_url = get_next_page_url(industry,cur_page,index_html)
        if next_page_url != None:
            next_page_html = index_page_html(industry,cur_page,next_page_url)
            cur_page += 1
            loop_all_page(cur_page,industry,next_page_html)
```

### spider(parameter)

主体函数，接收main传递的参数，并调用loop_all_page开始解析



# TIPS

1. 本爬虫用于爬取企业职位类型的职位详情页，因猎头职位等其他类型职位与企业职位详情页网页代码结构不同，因此并不通用，实现职位通用爬取可添加if判断语句，并对不同情况分别编写页面解析函数
2. 对于分行业爬取仍然超过100页的情况，可通过增加循环嵌套层数，增加筛选维度

