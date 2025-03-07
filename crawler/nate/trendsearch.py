from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup


DICT_SIGN_RANK_UPDOWN = {'상승': '↑', '보합': '-', '하락': '↓'}
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'}
TIME_ZONE_UTC = 9


def crawling_data_with_chromedriver(url, headers=None, timeout=None):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    issue_keywords = []
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        # 페이지 이동
        driver.get(url)
        driver.implicitly_wait(3)
        time.sleep(1)

        # 자동 스크롤 중지
        driver.find_element(By.CSS_SELECTOR, '#newsRollingBtn').click()

        # 이슈키워드 최초 수집
        list_rank_num = []
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        issue_soups = soup('ol', {'class': 'isKeywordList'})[0].find_all('li')
        for issue_soup in issue_soups:
            list_rank_num.append(issue_soup('span', {'class': 'num_rank'})[0].text.strip())
        issue_keywords.extend(issue_soups)
        time.sleep(0.2)

        # 이슈키워드 2차 수집
        check_duplicate_data = False
        while True:
            driver.find_element(By.CSS_SELECTOR, '#newsOptBtn > button.next').click()
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            issue_soups = soup('ol', {'class': 'isKeywordList'})[0].find_all('li')
            for issue_soup in issue_soups:
                if issue_soup('span', {'class': 'num_rank'})[0].text.strip() in list_rank_num:
                    check_duplicate_data = True
                    break
                else:
                    list_rank_num.append(issue_soup('span', {'class': 'num_rank'})[0].text.strip())
            if check_duplicate_data:
                break
            issue_keywords.extend(issue_soups)
            time.sleep(0.2)
    return issue_keywords


def parse_data_for_trendsearch(soup_issue_keywords):
    provide_datetime = datetime.now()

    results = []
    for i, soup_issue_keyword in enumerate(soup_issue_keywords):
        rank_num = soup_issue_keyword('span', {'class': 'num_rank'})[0].text.strip()
        search_word = soup_issue_keyword('span', {'class': 'txt_rank'})[0].text.strip()
        rank_updown = soup_issue_keyword('span', {'class': 'fc'})[0].text.strip()
        for word, sign in DICT_SIGN_RANK_UPDOWN.items():
            rank_updown = rank_updown.replace(word, sign)

        results.append({
            'rank_num': rank_num,
            'search_word': search_word,
            'rank_updown': rank_updown,
            'provide_datetime': provide_datetime,
        })
    return results


def crawling_data(url='https://nate.com', headers=None, timeout=10):
    if headers is None:
        headers = HEADERS

    res = crawling_data_with_chromedriver(url, headers=headers, timeout=timeout)
    results = parse_data_for_trendsearch(res)
    return results


def main():
    crawling_data()


if __name__ == '__main__':
    main()
