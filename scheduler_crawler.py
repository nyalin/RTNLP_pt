# import os
import time
from datetime import datetime
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler

# import config as conf
import module_func
from crawler import namuwiki
from crawler import naver_news
from crawler import zum
from crawler import nate
# from crawler import KONEPS


# 데이터베이스 저장 함수
def mf_insert_data_in_table(results=None, table_name=None):
    if results is None or table_name is None:
        error_msg = f"[CRWL] 잘못된 호출 - [{table_name}] - {results}"
        module_func.logging_file(error_msg, log_file=True, log_type='ERR')
        return None

    # 자료 없음
    if results == []:
        return

    # 데이터 저장 부분
    module_func.insert_data_in_table(results, table_name=table_name)
    module_func.update_clt_data_main_info(results[0], table_name=table_name)
    return f"[CRWL] {table_name} - {len(results)} 건 저장완료"


# 나무위키 - 최근변경 : 1분 단위(기본)
def crawl_namuwiki_recentchanges(table_name='NAMUWIKI_RECENTCHANGES'):
    results = namuwiki.recentchanges.crawling_data()
    module_func.logging_file(mf_insert_data_in_table(results, table_name), log_file=True)
    return


# 나무위키 - 실시간 검색어 : 5분 단위(기본)
def crawl_namuwiki_trendsearch(table_name='NAMUWIKI_TRENDSEARCH'):
    results = namuwiki.trendsearch.crawling_data()
    module_func.logging_file(mf_insert_data_in_table(results, table_name), log_file=True)
    return


# 네이버 뉴스 - 실시간 속보 : 1분 단위(기본)
def crawl_naver_recent_news(table_name='NEWS_NAVER_RECENTNEWS'):
    results = naver_news.naver_recent_news.crawling_data()
    module_func.logging_file(mf_insert_data_in_table(results, table_name), log_file=True)
    return


# 줌 - 실시간 검색어 : 5분 단위(기본)
def crawl_zum_trendsearch(table_name='ZUM_TRENDSEARCH'):
    results = zum.trendsearch.crawling_data()
    module_func.logging_file(mf_insert_data_in_table(results, table_name), log_file=True)
    return


# 네이트 - 실시간 검색어 : 5분 단위(기본)
def crawl_nate_trendsearch(table_name='NATE_TRENDSEARCH'):
    results = nate.trendsearch.crawling_data()
    module_func.logging_file(mf_insert_data_in_table(results, table_name), log_file=True)
    return


def main():
    datetime_now = datetime.now()
    next_run_time = datetime_now + timedelta(minutes=4-(datetime_now.minute % 5), seconds=60-datetime_now.second)
    sched = BackgroundScheduler(timezone='Asia/Seoul')
    # 나무위키
    sched.add_job(crawl_namuwiki_recentchanges, 'interval', minutes=1, id='crawl_namuwiki_recentchanges', misfire_grace_time=10, next_run_time=next_run_time)
    sched.add_job(crawl_namuwiki_trendsearch, 'interval', minutes=5, id='crawl_namuwiki_trendsearch', misfire_grace_time=10, next_run_time=next_run_time)
    # 네이버
    sched.add_job(crawl_naver_recent_news, 'interval', minutes=1, id='crawl_naver_recent_news', misfire_grace_time=10, next_run_time=next_run_time)
    # 줌
    sched.add_job(crawl_zum_trendsearch, 'interval', minutes=5, id='crawl_zum_trendsearch', misfire_grace_time=10, next_run_time=next_run_time)
    # 네이트
    sched.add_job(crawl_nate_trendsearch, 'interval', minutes=5, id='crawl_nate_trendsearch', misfire_grace_time=10, next_run_time=next_run_time)
    sched.start()  # 스케쥴링 작업 실행
    show_status_jobs(sched=sched)
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        sched.shutdown()


def show_status_jobs(sched=None):
    print(datetime.now())
    sched.print_jobs()
    return


if __name__ == "__main__":
    main()
