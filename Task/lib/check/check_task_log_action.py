from datetime import timedelta
import datetime
from Task.models import TaskLog
from Track.models import DailyViews, MusicViews, RegisterViews, SongViewsCount, ArtistViewsCount,  FavSongViewsCount, Tab, TabViews, UserDevice


def check_log_action(check_task_log_reglur_day: int, check_track_log_reglur_years: int):
    check_task_log_action(day=check_task_log_reglur_day)
    check_track_log_action(years=check_track_log_reglur_years)


def check_task_log_action(day: int):
    # 獲取當前日期
    current_date = datetime.now()

    # 計算三個月前的日期
    three_months_ago = current_date - timedelta(days=day)

    # 刪除三個月前的 TaskLog 數據
    TaskLog.objects.filter(created_at__lt=three_months_ago).delete()


def check_track_log_action(years: int):
    # 獲取當前日期
    current_date = datetime.now()

    # 計算三個月前的日期
    three_months_ago = current_date - timedelta(days=years * 365)

    # 刪除三個月前的 TaskLog 數據
    DailyViews.objects.filter(created_at__lt=three_months_ago).delete()

    MusicViews.objects.filter(created_at__lt=three_months_ago).delete()

    RegisterViews.objects.filter(created_at__lt=three_months_ago).delete()

    SongViewsCount.objects.filter(created_at__lt=three_months_ago).delete()

    # ArtistViewsCount.objects.filter(created_at__lt=three_months_ago).delete()

    # FavSongViewsCount.objects.filter(created_at__lt=three_months_ago).delete()

    # TabViews.objects.filter(created_at__lt=three_months_ago).delete()

    # UserDevice.objects.filter(created_at__lt=three_months_ago).delete()
