import json
import urllib.parse

import requests


SERVICE_SUB_URL = 'ScsbidInfoService'


# 개찰결과 물품/외자/용역/공사 목록 조회 - getOpengResultListInfo{}
# 물품 - Thng, 외자 - Frgcpt, 용역 - Servc, 공사 - Cnstwk,
def get_openg_result_list_info(service_url=None, api_key=None, category_type='Thng', output_type='json'):
    if service_url is None or api_key is None:
        return None
    url = f"{service_url}/{SERVICE_SUB_URL}/getOpengResultListInfo{category_type}"
    params = {
        'serviceKey': api_key,
        'numOfRows': '10',
        'pageNo': '1',
        'inqryDiv': '1',
        'inqryBgnDt': '202404230000',
        'inqryEndDt': '202404232359',
        # 'bfSpecRgstNo': '356759',  # inqryDiv가 2일 경우 사용
        'type': output_type,
    }
    params = urllib.parse.urlencode(params, safe='%:+')

    res = requests.get(url, params=params)
    res.raise_for_status()

    return json.loads(res.text)


# 낙찰된 목록 현황 물품/외자/용역/공사 조회 - getScsbidListSttus{}
# 물품 - Thng, 외자 - Frgcpt, 용역 - Servc, 공사 - Cnstwk,
def get_Scsbid_list_Sttus(service_url=None, api_key=None, category_type='Thng', output_type='json'):
    if service_url is None or api_key is None:
        return None
    url = f"{service_url}/{SERVICE_SUB_URL}/getScsbidListSttus{category_type}"
    params = {
        'serviceKey': api_key,
        'numOfRows': '10',
        'pageNo': '1',
        'inqryDiv': '1',
        'inqryBgnDt': '202404230000',
        'inqryEndDt': '202404232359',
        # 'bfSpecRgstNo': '356759',  # inqryDiv가 2일 경우 사용
        'type': output_type,
    }
    params = urllib.parse.urlencode(params, safe='%:+')

    res = requests.get(url, params=params)
    print(res.url)
    res.raise_for_status()

    return json.loads(res.text)
