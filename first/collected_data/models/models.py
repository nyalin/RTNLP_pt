from django.db import models


class NMWK_TrendSearch(models.Model):
    rank_num = models.IntegerField()
    search_word = models.CharField(max_length=200)
    provide_datetime = models.DateTimeField("When provided")

    def __str__(self):
        return f"[{self.provide_datetime}]{self.rank_num}_{self.search_word}"

    class Meta:
        db_table = 'NAMUWIKI_TRENDSEARCH'
        db_table_comment = "나무위키 인기검색어"


class NMWK_RecentChanges(models.Model):
    document_name = models.CharField(max_length=200)
    edit_datetime = models.DateTimeField("edit datetime")
    edit_editer = models.CharField(max_length=200)
    edit_comment = models.CharField(max_length=1000, null=True)
    edit_len_byte = models.IntegerField()

    def __str__(self):
        return f"[{self.edit_datetime}]{self.document_name}({self.edit_editer}, {self.edit_len_byte}) - {self.edit_comment}"

    class Meta:
        db_table = 'NAMUWIKI_RECENTCHANGES'
        db_table_comment = "나무위키 최근변경"


class NAVR_RecentNews(models.Model):
    news_unique_id = models.BigIntegerField(primary_key=True)
    news_page_id = models.CharField(max_length=15)
    news_title = models.CharField(max_length=250)
    news_datetime = models.DateTimeField("news published datetime")
    news_press_id = models.CharField(max_length=5)
    news_press_name = models.CharField(max_length=100)
    news_lede = models.CharField(max_length=200)

    def __str__(self):
        return f"[{self.news_unique_id}]{self.news_page_id}_{self.news_title}_{self.news_datetime}_{self.news_press_id}_{self.news_press_name}_{self.news_lede}"

    class Meta:
        db_table = 'NEWS_NAVER_RECENTNEWS'
        db_table_comment = "뉴스 네이버 최신뉴스"


class ZUM_TrendSearch(models.Model):
    rank_num = models.IntegerField()
    search_word = models.CharField(max_length=200)
    rank_updown = models.CharField(max_length=20)
    provide_datetime = models.DateTimeField("When provided")

    def __str__(self):
        return f"[{self.provide_datetime}]{self.rank_num}_{self.rank_updown}_{self.search_word}"

    class Meta:
        db_table = 'ZUM_TRENDSEARCH'
        db_table_comment = "줌 인기검색어"


class NATE_TrendSearch(models.Model):
    rank_num = models.IntegerField()
    search_word = models.CharField(max_length=200)
    rank_updown = models.CharField(max_length=20)
    provide_datetime = models.DateTimeField("When provided")

    def __str__(self):
        return f"[{self.provide_datetime}]{self.rank_num}_{self.rank_updown}_{self.search_word}"

    class Meta:
        db_table = 'NATE_TRENDSEARCH'
        db_table_comment = "네이트 인기검색어"


class CLTDATA_MainInfo(models.Model):
    clt_channel_idx = models.IntegerField(primary_key=True)
    clt_channel_eng = models.CharField(max_length=100)
    clt_channel_kor = models.CharField(max_length=100)
    clt_channel_initial = models.CharField(max_length=20)
    clt_datetime_recent_collected_data = models.DateTimeField("Lasted data update datetime")

    def __str__(self):
        return f"[{self.clt_channel_idx}]{self.clt_channel_eng}_{self.clt_channel_kor}_{self.clt_channel_initial}_{self.clt_datetime_recent_collected_data}"

    class Meta:
        db_table = 'CLTDATA_MAININFO'
        db_table_comment = "수집채널 메인 정보"
