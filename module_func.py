import os
import sys
import time
from datetime import datetime
from pathlib import Path

import MySQLdb

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent))  # 최상위폴더 추가

# Personal Setting
try:
    import config
except ImportError as e:
    raise ImportError(f"config.py 세팅 확인 : {e}")


def make_connector_sql(param=None):
    if param is None:
        param = {
            'host': config.DB_HOST,
            'user': config.DB_USER_ID,
            'password': config.DB_USER_PW,
            'database': config.DB_NAME,
            'port': config.DB_PORT,
            'charset': config.DB_CHARSET,
        }

    for i in range(2):
        try:
            conn = MySQLdb.connect(host=param['host'],
                                   user=param['user'], password=param['password'],
                                   database=param['database'], port=param['port'], charset=param['charset'])
            if i > 0:
                print('재시도 성공')
            break
        except Exception as ex:
            # 처리방안 검토
            if i > 0:
                print('재시도 실패')
                return None
            print('retry aftre 30secs..')
            logging_file(log_msg=f"[ERROR]-{ex}", log_file=True, log_type="ERR")
            time.sleep(30)
    return conn


def insert_data_in_table(data=None, table_name=None, param=None):
    if data is None or table_name is None:
        raise Exception('필수값 누락')
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise Exception('필수값 오류')

    with make_connector_sql(param=param) as conn:
        if conn is None:
            return
        with conn.cursor() as cursor:
            for row in data:
                placeholders = ', '.join(['%s'] * len(row))
                columns = ', '.join(row.keys())
                sql_query = f"INSERT INTO {table_name} ( {columns} ) VALUES ( {placeholders} );"
                try:
                    cursor.execute(sql_query, list(row.values()))
                except Exception as ex:
                    logging_file(log_msg=f"[WARNING]-{ex}", log_file=True, log_type="WARN")
        conn.commit()
    return


def read_data_in_table(sql_query=None, param=None):
    result = []
    if sql_query is None:
        pass
    else:
        with make_connector_sql(param=param) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
    return result


# 메시지 및 기타 로그 저장
def logging_file(log_msg='', print_show=False, log_file=False, log_date=None, log_type=None):
    # 메시지 체크
    if log_msg is None or log_msg == '':
        return

    # 메시지 출력 여부 체크
    if print_show:
        print(log_msg)

    # 파일 저장 여부 체크
    if not log_file:
        return
    else:
        log_path = os.path.join(BASE_DIR, 'logs')

    # 날짜 지정
    if log_date is None:
        log_date = datetime.today().strftime('%Y%m%d')

    # 로그 타입 지정
    if log_type is None:
        log_type = 'main'

    # 파일명 확인 및 경로 확인
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    save_path = os.path.join(log_path, f"{log_type}_{log_date}.txt")

    # 파일 저장
    with open(save_path, 'a+', encoding='utf-8') as f:
        f.write(f"[{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}] {log_msg}\n")
    return


# Update CLTDATA_MainInfo
def update_clt_data_main_info(data=None, table_name=None, param=None, update_table='CLTDATA_MAININFO'):
    columns = ['clt_channel_idx', 'clt_channel_eng', 'clt_channel_kor',
               'clt_channel_initial', 'clt_datetime_recent_collected_data']
    try:
        values = [config.CLT_CHANNEL_INFOMATION[table_name][0], table_name, config.CLT_CHANNEL_INFOMATION[table_name][1],
                  config.CLT_CHANNEL_INFOMATION[table_name][2], data[config.CLT_CHANNEL_INFOMATION[table_name][3]]]
    except Exception as ex:
        logging_file(log_msg=f"[ERROR]-{ex}", log_file=True, log_type="ERR")
        raise Exception('중요 변수값 누락')

    if data is None or table_name is None:
        raise Exception('필수값 누락')

    with make_connector_sql(param=param) as conn:
        if conn is None:
            return
        with conn.cursor() as cursor:
            placeholders = ', '.join(['%s'] * len(values))
            lb_columns = ', '.join(columns)
            sql_query = f"INSERT INTO {update_table} ( {lb_columns} ) VALUES ( {placeholders} ) ON DUPLICATE KEY UPDATE {columns[-1]} = '{values[-1]}';"
            try:
                cursor.execute(sql_query, values)
            except Exception as ex:
                logging_file(log_msg=f"[WARNING]-{ex}", log_file=True, log_type="WARN")
        conn.commit()
    return
