# 猎聘网"数据分析"招聘情况分析

通过python编写爬虫，爬取了猎聘网关键词“数据分析”的全国范围内1月内发布的企业职位。

本次分析源数据的职位发布日期：2017年9月19日-2017年10月19日

爬虫介绍：[爬取猎聘网职位信息](https://zhuanlan.zhihu.com/p/30284529)

源数据：

# 数据清洗

观察原始数据（共27633条）情况，并使用MySQL对爬取的原始数据进行清洗。

原始数据字段如下所示：

* `JobTitle` VARCHAR(255) ：职位名称
* `company` VARCHAR(255)：公司名称
* `salary` VARCHAR(255)：薪酬
* `position` VARCHAR(255)：工作地
* `PubTime` VARCHAR(255)：发布时间
* `qualification` VARCHAR(255)：职位要求，包含学历、工作经验、语言、年龄
* `tag_list` VARCHAR(255)：职位标签，'tag1,tag2,...'
* `description` TEXT：职位描述，详细介绍职位工作内容，任职要求等信息
* `industry` VARCHAR(255)：行业
* `industry_detail` VARCHAR(255)：猎聘更加细化的行业区分
* `companySize` VARCHAR(255)：公司规模，人员数
* `is_end` INT(255)：职位是否已结束，未结束为0，结束为1

## 薪酬数据

`salary`格式如'4-5万 72小时反馈'、'面议 24小时反馈'，包含职位反馈时间信息

* 新建字段`min_salary` INT(255)、`max_salary` INT(255)、`average_salary` FLOAT
* 从salary字段中提取min_salary、max_salary，并有average_salary = avg(min_salary,max_salary)
* 薪酬为'面议'时，min_salary = max_salary = average_salary = 0

## 工作地数据

`position`格式为'国家' 、 '城市' 、 '城市-区县'，如：'新加坡'、'北京'、'广州-天河区'，将'-'前后两部分分开

* 新建字段`position1` VARCHAR(255)、`position2`  VARCHAR(255)
* 若position包含'-'，前一部分为position1，后一部分为position2
* 若position不包含'-'，则position1 = position，position2 = null

## 发布时间

`PubTime`格式为'XXXX年XX月XX日'，是字符串形式

* 新建字段`pdate`  date
* 提取pubtime中年月日，转化成 pdate = '%Y-%m-%d'

## 异常及空值处理

* 因猎聘网职位详情页源码格式问题，若职位未给出公司规模数据，则爬取得到的公司规模字段实际为公司地址，令出现问题的行comAddress = companySize，并删除companySize字段内容
* industry_detail字段为空时，令industry_detail = industry
* comAddress字段为空时，令comAddress = position
* companySize、tag_list、description字段为空，填充'null'

## 用于分析的数据

根据分析目的筛选用于分析的数据，获得2320条

* 因猎聘网搜索较为模糊，结果中包含'会计助理'、'项目运营'等无关职位，对`JobTitle`进行筛选：包含'数据分析'、'大数据'、'数据运营'、'data'等
* 只分析未结束职位：is_end = 0
* 去重

