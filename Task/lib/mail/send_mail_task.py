

from Reviews.models import ActivityLog
from lib.Email.send import sned_request_reviews_mail
from lib.admin.get import get_admin_user
from datetime import datetime, date


def send_mail_action():
    today = date.today()

    # sned mail Reviews

    comment_c = ActivityLog.objects.filter(
        log_type="comment", timestamp__date=today).count()
    error_c = ActivityLog.objects.filter(
        log_type="error", timestamp__date=today).count()

    mes = ""
    if comment_c > 0:
        mes += f"有 {comment_c} 評論 \n"
    if error_c > 0:
        mes += f"有{error_c} 錯誤 \n"
    if comment_c or error_c:
        for user in get_admin_user():
            sned_request_reviews_mail(
                who=user["username"],
                email=user["email"],
                mes=mes
            )
