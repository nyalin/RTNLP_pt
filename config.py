import platform

import my_config

# LOCAL(default) / DEV / LIVE
SERVER_TYPE = 'LOCAL'
if platform.system() == 'Windows':
    SERVER_TYPE = 'DEV'
elif platform.system() == 'Linux':
    SERVER_TYPE = 'LIVE'

# SQL_INFO
DB_INFO = my_config.DB_INFO[SERVER_TYPE]

# SQL SETTING
DB_HOST = DB_INFO['HOST']
DB_PORT = int(DB_INFO['PORT'])
DB_USER_ID = DB_INFO['USER_ID']
DB_USER_PW = DB_INFO['USER_PW']
DB_NAME = DB_INFO['DB_NAME']
DB_CHARSET = DB_INFO['DB_CHARSET']

# KONEPS
DATA_GO_KR_API_KEY = my_config.DATA_GO_KR_API_KEY
KONEPS_API_URL = 'http://apis.data.go.kr/1230000'

# collected channel list (TABLE_NAME-IDX)
# 인기검색어(이슈키워드)는 반드시 XXX0으로 지정
CLT_CHANNEL_INFOMATION = {
    'NAMUWIKI_TRENDSEARCH': ['0100', '나무위키 인기검색어', 'NMWK_TrendSearch', 'provide_datetime'],
    'NAMUWIKI_RECENTCHANGES': ['0101', '나무위키 최근변경', 'NMWK_RecentChanges', 'edit_datetime'],
    'NEWS_NAVER_RECENTNEWS': ['0211', '뉴스 네이버 최신뉴스', 'NAVR_RecentNews', 'news_datetime'],
    'ZUM_TRENDSEARCH': ['0300', '줌 인기검색어', 'ZUM_TrendSearch', 'provide_datetime'],
    'NATE_TRENDSEARCH': ['0400', '네이트 인기검색어', 'NATE_TrendSearch', 'provide_datetime'],
}
