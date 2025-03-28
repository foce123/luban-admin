from django.urls import path
from web import views as webView

urlpatterns = [
    path('captchaImage', webView.CaptchaImageView.as_view(), name="获取验证码"),
    path('login', webView.LoginView.as_view(), name="登录"),
    path('logout', webView.LogoutView.as_view(), name="退出登录"),
    path('getInfo', webView.GetInfoView.as_view(), name="获取登陆信息"),
    path('getRouters', webView.GetRoutersView.as_view(), name="获取用户权限路由"),
]
