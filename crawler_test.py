import config as conf

import module_func
from crawler import namuwiki
from crawler import naver_news
from crawler import zum
from crawler import nate
from crawler import KONEPS


KONEPS_SERVICE_URL = f'{conf.KONEPS_API_URL}'
API_KEY = conf.DATA_GO_KR_API_KEY


# namuwiki
results = namuwiki.recentchanges.crawling_data()
print(results)
module_func.insert_data_in_table(results, 'NAMUWIKI_RECENTCHANGES')

results = namuwiki.trendsearch.crawling_data()
print(results)
module_func.insert_data_in_table(results, 'NAMUWIKI_TRENDSEARCH')

# naver_news
results = naver_news.naver_recent_news.crawling_data()
print(results)
module_func.insert_data_in_table(results, 'NEWS_NAVER_RECENTNEWS')

# zum
results = zum.trendsearch.crawling_data()
print(results)
module_func.insert_data_in_table(results, 'ZUM_TRENDSEARCH')

# nate
results = nate.trendsearch.crawling_data()
print(results)
module_func.insert_data_in_table(results, 'NATE_TRENDSEARCH')


# KONEPS
results = KONEPS.bid_prestd_info.get_public_prcure_info(KONEPS_SERVICE_URL, API_KEY, category_type='Thng')
print(results)
# module_func.insert_data_in_table(results, 'TABLE_NAME')

results = KONEPS.bid_pub_info.get_bid_Pblanc_list_info(KONEPS_SERVICE_URL, API_KEY, category_type='Thng')
print(results)
# module_func.insert_data_in_table(results, 'TABLE_NAME')

results = KONEPS.bid_success_info.get_openg_result_list_info(KONEPS_SERVICE_URL, API_KEY, category_type='Thng')
print(results)
# module_func.insert_data_in_table(results, 'TABLE_NAME')
results = KONEPS.bid_success_info.get_Scsbid_list_Sttus(KONEPS_SERVICE_URL, API_KEY, category_type='Thng')
print(results)
# module_func.insert_data_in_table(results, 'TABLE_NAME')
