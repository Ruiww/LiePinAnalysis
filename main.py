from LiePinSpider.spider import *

def main(para) :
    #起始url:全国 一个月以内 企业职位 数据分析
    '''
    start_url = 'https://www.liepin.com/zhaopin/?industries=&dqs=&salary=*&\
    jobKind=2&pubTime=30&compkind=&compscale=&industryType=&searchType=1&clean_condition=&isAnalysis=&init=1&\
    sortFlag=15&flushckid=0&fromSearchBtn=1&headckid=d49c1e39b298ad65&d_headId=79b279ac595d64a6487245249e136c8b&\
    d_ckId=5a2414e599d7471b7c61d72f3e1e9d3e&d_sfrom=search_unknown&d_curPage=0&d_pageSize=40&\
    siTag=ZFDYQyfloRvvhTxLnVV_Qg~_XXFBbhWcWTjV9QfCvO04A&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90'
    '''
    #industry_ergodic(start_url)
    industry = para['industry']
    print(industry)
    parse_detail_savedata_rollpage(para)



if __name__ == '__main__':
    start_url = 'https://www.liepin.com/zhaopin/?industries=&dqs=&salary=*&\
        jobKind=2&pubTime=30&compkind=&compscale=&industryType=&searchType=1&clean_condition=&isAnalysis=&init=1&\
        sortFlag=15&flushckid=0&fromSearchBtn=1&headckid=d49c1e39b298ad65&d_headId=79b279ac595d64a6487245249e136c8b&\
        d_ckId=5a2414e599d7471b7c61d72f3e1e9d3e&d_sfrom=search_unknown&d_curPage=0&d_pageSize=40&\
        siTag=ZFDYQyfloRvvhTxLnVV_Qg~_XXFBbhWcWTjV9QfCvO04A&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90'
    html = index_page_html(start_url)
    industry_url_list = get_industry_url(html)
    groups1 = list(industry_url_list.keys())
    groups2 = list(industry_url_list.values())
    pool = Pool(4)
    para_groups = []
    for element in industry_url_list.items():
        para = {
            'industry' : element[0],
            'url': element[1]
        }
        para_groups.append(para)
        print(para)
    #pool.map(main,groups1,groups2)
    pool.map(main,para_groups)
    #print(groups1)
    #print(groups2)