from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.landing_page, name='landing_page'),
    path('', views.index, name="index"),
    path('try_signin', views.try_signin, name="try_signin"),
    path('try_signup', views.try_signup, name="try_signup"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('user_dashboard', views.user_dashboard, name="user_dashboard"),
    path('logout', views.logout, name="logout"),
    path('start_quiz', views.start_quiz, name="start_quiz"),
    path('change_img', views.change_img, name="change_img"),
    path('change_password', views.change_password, name="change_password"),
    path('completed_levels', views.completed_levels, name="completed_levels"),
    path('check_ans/<ques_id>', views.check_ans, name="check_ans"),
    path('withdraw', views.withdraw, name="withdraw"),
    path('withdraw_payment', views.withdraw_payment, name="withdraw_payment"),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)