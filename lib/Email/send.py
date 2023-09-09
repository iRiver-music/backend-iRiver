

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

context = {
    'title': '邮件标题',
    'username': '用户名',
    'content': '邮件内容',
    'buttonURL': '#',
    'buttonName': '按钮文本',
    'who': '接收者姓名',
    'comp': settings.COMP,
    "message": "",
}


def mail(subject, recipient_list, html_template=None, context=None):
    if html_template and context:
        # 渲染HTML模板并生成HTML消息
        html_message = render_to_string(html_template, context)
    else:
        html_message = None

    # 发送邮件
    send_mail(
        subject,
        context["content"],
        settings.EMAIL_HOST_USER,
        recipient_list,
        html_message=html_message,  # 使用HTML消息
        fail_silently=False,
    )
# 使用示例


# def test(request):
#     context = {
#         'title': '邮件标题',
#         'username': '用户名',
#         'content': '邮件内容',
#         'buttonURL': '#',
#         'buttonName': '按钮文本',
#         'who': '接收者姓名',
#         'comp': '賴泓瑋 lai09150915@gmail.com'
#     }

#     # 调用 send_email 函数，并传递HTML模板和上下文
#     send_email(
#         '测试邮件',
#         ['lai09150915@gmail.com'],
#         html_template='select_style_request.html',
#         context=context,
#     )

#     return HttpResponse('邮件发送成功！')


def send_style_mail(who: str, email: str):

    context = {
        'title': '更新discover 資料',
        'username': who,
        'content': '這個月新的style資料已經出來，需要做選擇。',
        'buttonURL': settings.ADMIN_DNS,
        'buttonName': '前往至管理頁面',
        'who': "iriver系統",
        'comp': settings.COMP,
        'message': "更新discover 資料",
        'additional_content_1': '這些新的style資料將幫助我們提供更好的服務。',
        'additional_content_2': '請在管理頁面上查看和選擇適合的選項。',
        'contact_support': '如果您有任何問題或需要幫助，請隨時聯繫我們的支持團隊。',
    }
    try:
        mail(subject=settings.SUBJECT,
             recipient_list=[email],
             html_template="email/select_style_request.html",
             context=context)
        return True
    except Exception as e:
        print(e)
        return False


def send_error_mail(who: str, email: str, mes: str):
    context = {
        'title': 'iriver 系統錯誤!!',
        'username': who,
        'content': '系統遇到了一個錯誤:',
        'error_message': mes,
        'buttonURL': settings.ADMIN_DNS,
        'buttonName': '前往至管理頁面',
        'who': "iriver系統",
        'comp': settings.COMP,
        'additional_content_1': '起盡快處理這些錯誤。',
        'additional_content_2': '請在管理頁面上查看和選擇適合的選項。',
        'contact_support': '如果您有任何問題或需要幫助，請隨時聯繫我們的支持團隊。',
    }

    try:
        mail(subject=settings.SUBJECT,
             recipient_list=[email],
             html_template="email/error_email_request.html",
             context=context)
        return True
    except Exception as e:
        print(e)
        return False

# 定期報告


def send_repot_mail(who: str, email: str, mes: str):
    context = {
        'title': 'iriver 每日報告',
        'username': who,
        'content': mes,
        'buttonURL': settings.ADMIN_DNS,
        'buttonName': '去聽歌',
        'who': "iriver系統",
        'comp': settings.COMP,
        'additional_content_2': '請在管理頁面上查看和選擇適合的選項。',
        'contact_support': '如果您有任何問題或需要幫助，請隨時聯繫我們的支持團隊。',
    }

    try:
        mail(subject=settings.SUBJECT,
             recipient_list=[email],
             html_template="email/report_email_request.html",
             context=context)
        return True
    except Exception as e:
        print(e, "mail failed")
        return False


#  新增admin 管理者 ??


# user


def send_user_requset_error_mail(who: str, email: str, mes: str):
    context = {
        'title': 'iriver 音樂',
        'username': who,
        'content': mes,
        'buttonURL': settings.WEB_MUSIC_DNS,
        'buttonName': '去聽歌',
        'who': "iriver系統",
        'comp': settings.COMP,
        'additional_content_1': '謝謝你願意回饋問題',
        'contact_support': '如果您有任何問題或需要幫助，請隨時聯繫我們的支持團隊。',
    }

    try:
        mail(subject="iriver 回報通知",
             recipient_list=[email],
             html_template="email/user/requset_error.html",
             context=context)
        return True
    except Exception as e:
        print(e, "mail failed")
        return False


def sned_request_reviews_mail(who: str, email: str, mes: str):
    context = {
        'title': 'iriver 系統',
        'username': who,
        'content': mes,
        'buttonURL': settings.ADMIN_DNS,
        'buttonName': '前往至管理頁面',
        'who': "iriver系統",
        'comp': settings.COMP,
        'additional_content_1': '謝謝你願意回饋問題',
        'contact_support': '如果您有任何問題或需要幫助，請隨時聯繫我們的支持團隊。',
    }

    try:
        mail(subject="iriver 回報通知",
             recipient_list=[email],
             html_template="email/admin/request_reviews.html",
             context=context)
        return True
    except Exception as e:
        print(e, "mail failed")
        return False
