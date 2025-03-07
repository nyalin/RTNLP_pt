from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup


DICT_SIGN_RANK_UPDOWN = {'상승': '↑', '보합': '-', '하락': '↓'}
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15'}
TIME_ZONE_UTC = 9


def crawling_with_chromedriver(url, headers=None, timeout=None):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    for i in range(3):
        try:
            with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
                # 페이지 이동
                driver.get(url)
                driver.implicitly_wait(3)
                time.sleep(1)

                # 다시보지않기 체크
                useless_layers = driver.find_elements(By.CLASS_NAME, 'btn-layer-close-day')
                for useless_layer in useless_layers:
                    useless_layer.click()

                # 이슈검색어로 마우스 이동
                ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="app"]/div/header/div[3]/div/div/div[2]')).perform()
                time.sleep(1)

                # 페이지 소스 가져오기
                html = driver.page_source
                time.sleep(0.2)
                break
        except Exception as ex:
            print(ex)
            time.sleep(5)
    return html


def convert_text_datetime(text=None, datetime_now=datetime.now(), date_format=None):
    text = text.replace('오전', 'AM').replace('오후', 'PM')
    conv_datetime = datetime.strptime(text, '%Y.%m.%d %p %I:%M')
    return conv_datetime


def parse_data_for_trendsearch(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    try:
        provide_datetime = convert_text_datetime(soup('span', {'class': 'time'})[0].time.text.strip())
    except IndexError:
        provide_datetime = datetime.now()
    soup_issue_keywords = soup('ul', {'class': 'layer_cont issue'})[0].find_all('li')

    results = []
    for i, soup_issue_keyword in enumerate(soup_issue_keywords):
        rank_num = soup_issue_keyword('span', {'class': 'num'})[0].text.replace('.', '').strip()
        search_word = soup_issue_keyword('span', {'class': 'inner_txt'})[0].text.strip()
        rank_updown = soup_issue_keyword('span', {'class': 'ico'})[0].text.strip()
        for word, sign in DICT_SIGN_RANK_UPDOWN.items():
            rank_updown = rank_updown.replace(word, sign)

        results.append({
            'rank_num': rank_num,
            'search_word': search_word,
            'rank_updown': rank_updown,
            'provide_datetime': provide_datetime,
        })
    return results


def crawling_data(url='https://zum.com', headers=None, timeout=10):
    if headers is None:
        headers = HEADERS

    res = crawling_with_chromedriver(url, headers=headers, timeout=timeout)
    results = parse_data_for_trendsearch(res)
    return results


def main():
    crawling_data()


if __name__ == '__main__':
    main()
