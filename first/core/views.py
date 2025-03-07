from django.shortcuts import render
from django.views.generic import TemplateView

from collected_data.models import NMWK_TrendSearch
from collected_data.models import ZUM_TrendSearch
from collected_data.models import NATE_TrendSearch

from collected_data.models import CLTDATA_MainInfo


class IndexView(TemplateView):
    # 기본 설정
    template_name = 'core/index.html'

    # 추가 설정
    cltdata_main_info = None
    dict_channel_last_datetime = {}
    list_ts_portals_inital = ['NMWK', 'ZUM', 'NATE']

    def get_CLTDATA_MainInfo(self):
        self.cltdata_main_info = CLTDATA_MainInfo.objects.all()
        for i in self.cltdata_main_info:
            self.dict_channel_last_datetime[i.clt_channel_initial] = i.clt_datetime_recent_collected_data
        return

    def get_trendsearch_portals(self, list_ts_portals_inital=None, dict_channel_last_datetime=None):
        # 파라미터 값이 없을 경우 처리 부분
        if list_ts_portals_inital is None:
            list_ts_portals_inital = self.list_ts_portals_inital
        if dict_channel_last_datetime == {}:
            self.get_CLTDATA_MainInfo()
        if dict_channel_last_datetime is None:
            dict_channel_last_datetime = self.dict_channel_last_datetime

        # 결과 구성
        results = {}
        for channel_name_inital in list_ts_portals_inital:
            results[f"{channel_name_inital}_trend_search"] = self.get_trendsearch_channel(channel_name_inital=channel_name_inital)
        return results

    def get_trendsearch_channel(self, channel_name_inital=None):
        result = None

        # 채널별 마지막 시간 확인
        try:
            target_date = self.dict_channel_last_datetime[f"{channel_name_inital}_TrendSearch"]
        except Exception as ex:
            print(ex)
            return result

        # 채널별 값 가져오기
        try:
            if channel_name_inital == 'NMWK':
                result = NMWK_TrendSearch.objects.filter(provide_datetime=target_date).order_by('rank_num').values()
            elif channel_name_inital == 'ZUM':
                result = ZUM_TrendSearch.objects.filter(provide_datetime=target_date).order_by('rank_num').values()
            elif channel_name_inital == 'NATE':
                result = NATE_TrendSearch.objects.filter(provide_datetime=target_date).order_by('rank_num').values()
            else:
                print(f"등록되지 않은 채널명입니다. - {channel_name_inital}")
        except Exception as ex:
            print(ex)

        return result

    def get(self, request):
        # 값 갱신
        self.get_CLTDATA_MainInfo()

        # 결과 생성
        results_data = {'target_date': list(self.dict_channel_last_datetime.values())[0]}
        results_data.update(self.get_trendsearch_portals())

        return render(request, self.template_name, results_data)
