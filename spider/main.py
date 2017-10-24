from multiprocessing import Pool
from LiePinSpider.spider.spider import *

if __name__ == '__main__':
    #起始url:全国 一个月以内 企业职位 数据分析
    start_url = 'https://www.liepin.com/zhaopin/?industries=&dqs=&salary=&jobKind=2&pubTime=30&compkind=&compscale=&\
    industryType=&searchType=1&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=0&fromSearchBtn=1&\
    headckid=86e340b5c4d42b08&d_headId=243d5e0a38dfec3c3052f8697268e14d&d_ckId=e0c94c87defa15a17beaf540e76752d7&\
    d_sfrom=search_fp_nvbar&d_curPage=0&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg%7ENw_YksyhAxvGdx7jL2ZbaQ&key=数据分析'
    #获取分行业_index_url
    html = index_page_html(industry='ALL',cur_page='None',index_url=start_url)
    industry_url_list = get_industry_url(html)
    para_groups = []
    for element in industry_url_list.items():
        para = {
            'industry': element[0],
            'url': element[1]
        }
        para_groups.append(para)
        print(para)

    #多线程运行
    pool = Pool()
    pool.map(spider,para_groups)

    #单线程
    #for para in para_groups:
    #    spider(para)
