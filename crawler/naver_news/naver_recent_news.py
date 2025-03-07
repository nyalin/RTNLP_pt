import sys
from pathlib import Path
import re
from datetime import datetime
from datetime import timedelta
from operator import itemgetter

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR.parent))  # 최상위폴더 추가

# Personal Setting
try:
    import module_func
except ImportError as e:
    raise ImportError(f"module_func.py 세팅 확인 : {e}")

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'}
TIME_ZONE_UTC = 9


def convert_ago_to_datetime(text=None, datetime_now=None, date_format=None):
    conv_datetime = None
    if text is None:
        conv_datetime = datetime_now
    if datetime_now is None:
        datetime_now = datetime.now()
    value = int(re.search(r'\d+', text).group())
    if isinstance(text, str) and text.endswith('전'):
        if text.count('초') > 0:
            conv_datetime = datetime_now - timedelta(seconds=value)
        elif text.count('분'):
            conv_datetime = datetime_now - timedelta(minutes=value)
        elif text.count('시간'):
            conv_datetime = datetime_now - timedelta(hours=value)
        elif text.count('일'):
            conv_datetime = datetime_now - timedelta(days=value)
        elif text.count('주'):
            conv_datetime = datetime_now - timedelta(days=7*value)
        elif text.count('월') or text.count('달'):
            conv_datetime = datetime_now - timedelta(days=30*value)
        elif text.count('년'):
            conv_datetime = datetime_now - timedelta(days=365*value)
        else:
            conv_datetime = None
    else:
        text = text.replace('오전', 'AM').replace('오후', 'PM')
        conv_datetime = datetime.strptime(text, '%Y.%m.%d. %p %H:%M')
    return conv_datetime


def get_prev_unique_id_list(target_datetime=None, repeat_time=5):
    if target_datetime is None:
        target_datetime = (datetime.now() - timedelta(minutes=int(repeat_time*3))).strftime("%Y-%m-%d %H:%M:%S")
    sql_query = f"SELECT news_unique_id FROM NEWS_NAVER_RECENTNEWS WHERE news_datetime >= '{target_datetime}'"
    result = module_func.read_data_in_table(sql_query=sql_query)
    return [r[0] for r in result]


def parse_data_for_recent_news(html_text, datetime_now=None, list_prev_unique_id=[], date_format='%Y.%m.%d. %p %H:%M'):
    soup = BeautifulSoup(html_text, features="html.parser")
    soup_recent_news = soup('ul', {'class': 'type06_headline'})[0].find_all('li')

    results = []
    num_duplicates = 0
    for i, soup_news in enumerate(soup_recent_news):
        idx_title = len(soup_news('dt'))

        news_page_id = soup_news('dt')[idx_title - 1].a['href'].split('?')[0].split('/')[-1].strip()
        news_title = soup_news('dt')[idx_title - 1].text.strip()
        news_datetime = convert_ago_to_datetime(soup_news('span', {'class': 'date'})[0].text.strip(), datetime_now=datetime_now, date_format=date_format)
        news_press_id = soup_news('dt')[idx_title - 1].a['href'].split('?')[0].split('/')[-2].strip()
        news_press_name = soup_news('span', {'class': 'writing'})[0].text.strip()
        news_lede = soup_news('span', {'class': 'lede'})[0].text.replace('…', '').strip()
        news_unique_id = int(news_press_id + news_page_id)

        if news_unique_id in list_prev_unique_id:
            num_duplicates += 1
            continue

        results.append({
            'news_unique_id': news_unique_id,
            'news_page_id': news_page_id,
            'news_title': news_title,
            'news_datetime': news_datetime,
            'news_press_id': news_press_id,
            'news_press_name': news_press_name,
            'news_lede': news_lede,
        })
    return results, num_duplicates


def crawling_data(url='https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001', headers=None, timeout=10, target_date=None, max_page=5):
    datetime_now = datetime.now()
    if headers is None:
        headers = HEADERS
    if target_date is None:
        target_date = datetime_now.strftime('%Y%m%d')

    datetime_now = datetime.now()
    list_prev_unique_id = get_prev_unique_id_list()
    results = []
    for page_num in range(max_page):
        target_url = f"{url}&mid=sec&listType=summary&date={target_date}&page={page_num+1}"
        res = requests.get(target_url, headers=headers, timeout=timeout)
        result, num_duplicates = parse_data_for_recent_news(res.text, datetime_now=datetime_now, list_prev_unique_id=list_prev_unique_id)
        results.extend(result)
        if num_duplicates >= 2:
            break
    results = sorted(results, key=itemgetter('news_datetime'), reverse=True)
    return results


def main():
    print(crawling_data())


if __name__ == '__main__':
    main()
