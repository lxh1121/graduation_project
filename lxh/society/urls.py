#coding:utf-8
from django.urls import path, re_path
from . import views


app_name = 'society'
urlpatterns = [
    # 后台管理界面
    path('admin/login/', views.ad_login, name='ad_login'),
    path('admin/login_check/', views.ad_login_check, name='ad_login_check'),
    path('admin/index/', views.ad_index, name='ad_index'),
    # # 资讯管理
    # 栏目
    path('admin/category/', views.ad_category, name='ad_category'),
    path('admin/category/add/', views.ad_category_add, name='ad_category_add'),
    path('admin/category/add/2', views.ad_category_add2, name='ad_category_add2'),
    path('admin/category/change/', views.ad_category_change, name='ad_category_change'),
    path('admin/category/change2/', views.ad_category_change2, name='ad_category_change2'),
    path('admin/category/delete/', views.ad_category_delete, name='ad_category_delete'),
    path('admin/category/all_cate/', views.ad_all_cate, name='all_cate'),
    # 文章审核
    path('admin/art/', views.ad_article, name='ad_article'),
    path('admin/art/add', views.ad_article_add, name='article_add'),
    path('admin/art/change', views.ad_article_change, name='article_change'),
    path('admin/art/delete', views.ad_article_delete, name='article_delete'),
    path('admin/art/all_art/', views.ad_all_art, name='all_article'),
    # 审核是否通过
    path('admin/art/check/', views.art_check, name='art_check'),
    # # 系统管理
    # 公告
    path('admin/sys/notice', views.sys_notice, name='sys_notice'),
    # 友情链接
    path('admin/sys/blogrool', views.sys_blogrool, name='sys_blogrool'),
    path('admin/sys/blogrool/add', views.sys_blogrool_add, name='sys_blogrool_add'),
    # 数据备份
    path('admin/sys/data', views.sys_data, name='sys_data'),

    # 欢迎页
    path('admin/welcome/', views.welcome, name='welcome'),
    # 退出
    path('admin/logout/', views.ad_logout, name='ad_logout'),


    # 前端界面
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),
    # 短信验证
    path('note/', views.note_code, name='note_code'),
    # 注册
    path('regis/', views.regis, name='regis'),
    path('regis_check/stu/', views.regis_check_stu, name='regis_check_stu'),
    path('regis_check/pri/', views.regis_check_pri, name='regis_check_pri'),
    # 忘记密码
    path('forget/pas/', views.forget_pas, name='forget_pas'),
    # 个人中心页面
    # 个人资料
    path('a/', views.geren, name='a'),
    path('change/data/', views.change_data, name='change_data'),
    path('iss/content/', views.iss_cont, name='iss_cont'),
    path('iss/<int:a>/', views.my_iss, name='my_iss'),
    path('i', views.my_vip, name='my_vip'),
    path('j', views.my_score, name='my_score'),
    path('k', views.pay, name='pay'),
    path('l', views.gift_ex, name='gift_ex'),
    path('g', views.new_message, name='new_message'),
    path('change/pwd/', views.change_pwd, name='change_pwd'),
    path('change/pwd2', views.change_pwd2, name='change_pwd2'),
    path('logout/', views.login_out, name='logout'),
    # 文章详情
    # path('article/deta/', views.article_deta, name='article_deta'),
    path('main/<int:a>', views.main_type, name='main_type'),
    path('fl', views.flash, name='flash'),
    path('fldeta<int:id>', views.flash_detail, name='flash_detail'),
    path('arti/<int:id>', views.article_deta, name='article_deta'),
    path('vote', views.di_vote, name='di_vote'),
    path('share/<int:id>', views.share_arti, name='share_arti'),
    path('share_suce', views.share_success, name='share_success'),
    path('com', views.comm, name='comm'),
]