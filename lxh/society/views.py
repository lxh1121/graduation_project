import random
import urllib
import time

from django.shortcuts import render,HttpResponse, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as _login, logout
from django.contrib.messages import get_messages
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
import os
from lxh import settings
from .models import *
from .tools import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


# 后台界面
# 登录
def ad_login(request):
    return render(request, 'society/backstage/admin_login.html')


# 登录验证
def ad_login_check(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            _login(request, user)
            messages.info(request, '登录成功')
            return HttpResponseRedirect(reverse('society:ad_index'))
        else:
            messages.info(request, '用户名或密码错误')
            return render(request, 'society/backstage/admin_login.html')
    else:
        return redirect('society:ad_login')


# 欢迎页
@login_required(login_url='society:ad_login')
def welcome(request):
    return render(request, 'society/backstage/welcome.html')


# 后台详情页
@login_required(login_url='society:ad_login')
def ad_index(request):
    return render(request, 'society/backstage/admin_index.html')


# 栏目界面
@login_required(login_url='society:ad_login')
def ad_category(request):
    search = request.POST.get('search')
    if search is not None:
        if not search.isdigit():
            cate_list = Category.objects.filter(type__contains=search)
        else:
            cate_list = Category.objects.filter(Q(id=search) | Q(type__contains=search))
    else:
        cate_list = Category.objects.all()
    return render(request, 'society/backstage/category-list.html', {'cate_list': cate_list})


# 栏目添加
@login_required(login_url='society:ad_login')
def ad_category_add(request):
    storage = get_messages(request)
    return render(request, 'society/backstage/category-add.html', locals())


@login_required(login_url='society:ad_login')
def ad_category_add2(request):
    type = request.POST.get('type')
    content = request.POST.get('c_content')
    if not type:
        messages.info(request, '类目名称不能为空')
        return HttpResponseRedirect(reverse('society:ad_category_add'))
    if not content:
        messages.info(request, '描述内容不能为空')
        return HttpResponseRedirect(reverse('society:ad_category_add'))
    if Category.objects.filter(type=type).exists():
        messages.info(request, '该类目已存在')
        return HttpResponseRedirect(reverse('society:ad_category_add'))
    Category.objects.create(type=type, content=content)
    messages.info(request, '添加成功')
    return HttpResponseRedirect(reverse('society:ad_category'))


# 修改
@login_required(login_url='society:ad_login')
def ad_category_change(request):
    c_id = request.GET.get('c_id')
    if c_id is None:
        return HttpResponseRedirect(reverse('society:ad_category'))
    if not c_id.isdigit():
        return HttpResponseRedirect(reverse('society:ad_category'))
    try:
        category = Category.objects.get(pk=c_id)
    except Category.DoesNotExist:
        return HttpResponseRedirect(reverse('society:ad_category'))
    form = CategoryForm(instance=category)
    return render(request, 'society/backstage/category-change.html', locals())


@login_required(login_url='society:ad_login')
def ad_category_change2(request):
    c_id = request.POST.get('c_id')
    try:
        category = Category.objects.get(pk=c_id)
    except :
        messages.info(request, '访问不存在')
        return HttpResponseRedirect(reverse('society:ad_category'))
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
        form.save()
        messages.info(request, '修改成功')
    else:
        messages.info(request, '修改失败')
    return HttpResponseRedirect(reverse('society:ad_category'))


# 删除
@login_required(login_url='society:ad_login')
def ad_category_delete(request):
    c_id = request.GET.get('c_id')
    if c_id is None:
        return JsonResponse({'status': 0, 'msg': '删除失败'})
    try:
        category = Category.objects.get(id=c_id)
    except Category.DoesNotExist:
        return JsonResponse({'status': 0, 'msg': '删除失败'})
    if category.article_set.all():
        return JsonResponse({'status': 2, 'msg': '该类目下有文章，不能删除'})
    category.delete()
    return JsonResponse({'status': 1, 'msg': '删除成功'})


# 栏目批量删除
def ad_all_cate(request):
    return render(request, 'society/backstage/category-add.html')


# 文章审核
@login_required(login_url='society:ad_login')
def ad_article(request):
    search = request.POST.get('search')
    if search is not None:
        if not search.isdigit():
            art_list = Article.objects.filter(title__contains=search)
        else:
            art_list = Article.objects.filter(Q(id=search) | Q(title__contains=search))
    else:
        art_list = Article.objects.all().order_by('-distribute_date')
    return render(request, 'society/backstage/article-list.html', {'articles': art_list})


def art_check(request):
    art_id = request.GET.get('art_id')
    if Article.objects.filter(id=art_id).exists():
        article = Article.objects.get(id=art_id)
        sta = request.GET.get('status')
        if sta == '1':
            article.status = 1
        elif sta == '2':
            article.status = 2
        article.save()
        return JsonResponse({'status': 1, 'msg': '修改成功'})
    else:
        return JsonResponse({'status': 2, 'msg': '修改失败'})



@login_required(login_url='society:ad_login')
def ad_article_add(request):
    return render(request, 'society/backstage/article-add.html')


@login_required(login_url='society:ad_login')
def ad_article_change(request):
    return render(request, 'society/backstage/article-change.html')


def ad_article_delete(request):
    return render(request, 'society/backstage/article-delete.html')


# 批量删除文章
def ad_all_art(request):
    id_str = request.GET.get('id_str')
    if not id_str:
        return JsonResponse({'status': 0, 'msg': '删除失败'})
    article_id_str = id_str.split(',')
    art = Article.objects.filter(id__in=article_id_str)
    for article in art:
        file_path = str(article.image)
        full_path = settings.MEDIA_ROOT + file_path
        if file_path != '20181024/07.jpg':
            os.remove(full_path)
        article.delete()
    return JsonResponse({'status': 1, 'msg': '删除成功'})


# # 系统管理
# 系统公告
def sys_notice(request):
    return render(request, 'society/backstage/system-notice.html')


# 友情链接
def sys_blogrool(request):
    return render(request, 'society/backstage/system-blogrool.html')


def sys_blogrool_add(request):
    return render(request, 'society/backstage/system-blogrool-add.html')


# 数据字典
def sys_data(request):
    return render(request, 'society/backstage/system-data.html')


# 退出登录
def ad_logout(request):
    action = request.GET.get('action')
    if action == 'logout':
        logout(request)
        messages.info(request, '退出成功')
    return HttpResponseRedirect(reverse('society:ad_login'))











# 前端


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        pasnew = add_pass(password)
        # print('------------------------------')
        # print(pasnew)
        if role == '学生':
            if Student.objects.filter(username=username).exists():
                student = Student.objects.get(username=username)
                if student.password == pasnew:

                    request.session['username'] = username
                    request.session['photo'] = str(student.photo)
                    request.session['phone'] = student.phone
                    request.session['info'] = student.info
                    check = request.POST.get('check', None)
                    if check is not None:
                        request.session['password'] = password
                    return redirect('society:change_data')
                else:
                    err2 = '密码错误'
                    return render(request, 'society/baseone/login.html', locals())
            else:
                err1 = '用户不存在'
                return render(request, 'society/baseone/login.html', locals())
        elif role == '社团负责人':
            if Principal.objects.filter(Q(stu_num=username) | Q(phone=username)).exists():
                if len(username) == 11:
                    principal = Principal.objects.get(phone=username)
                else:
                    principal = Principal.objects.get(stu_num=username)
                if principal.password == pasnew:
                    request.session['username'] = principal.username
                    request.session['photo'] = str(principal.photo)
                    request.session['phone'] = principal.phone
                    request.session['mass'] = principal.mass
                    request.session['info'] = principal.info
                    request.session['vip'] = principal.vip
                    request.session['leave_count'] = principal.leave_count
                    request.session['score'] = principal.score
                    request.session['user_code'] = principal.user_code
                    request.session['stu_num'] = principal.stu_num
                    try:
                        if request.POST['check']:
                            request.session['password'] = password
                    except:
                        del request.session['password']
                    return redirect('society:change_data')
                else:
                    err2 = '密码错误'
                    return render(request, 'society/baseone/login.html', locals())
            else:
                err1 = '用户不存在'
                return render(request, 'society/baseone/login.html', locals())
        else:
            return HttpResponse(show_message('你的行为已违法！', '/pylxh/main/'))
    else:
        return render(request, 'society/baseone/login.html')


# 注册
def regis(request):
    return render(request, 'society/baseone/register.html', locals())


# 注册学生验证
def regis_check_stu(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        stu_num = request.POST.get('stu_num')
        if len(username) > 20 or len(username) < 4 or not username:
            err1 = '用户名格式错误'
            return render(request, 'society/baseone/register.html', locals())
        student = Principal.objects.filter(username=username)
        student1 = Principal.objects.filter(phone=phone)
        if len(student) > 0 or len(student1) > 0:
            err1 = '用户或手机号已存在'
            return render(request, 'society/baseone/register.html', locals())
        else:
            if judge_pass(password) is None or password != password2:
                err2 = '密码错误或不一致'
                return render(request, 'society/baseone/register.html', locals())
            if judge_phone(phone) is None:
                err3 = '手机号格式错误'
                return render(request, 'society/baseone/register.html', locals())
            note_ran = request.session.get('note_ran', None)
            if note_ran is not None:
                if request.POST['code'] == note_ran:
                    del request.session['note_ran']
                    password = add_pass(password)
                    student = Principal.objects.create(username=username, password=password, phone=phone, stu_num=stu_num)
                    return HttpResponse(show_message('注册成功', '/pylxh/login/'))
                else:
                    err4 = '验证码错误'
                    return render(request, 'society/baseone/register.html', locals())
            else:
                err4 = '验证码错误'
                return render(request, 'society/baseone/register.html', locals())
    else:
        return render(request, 'society/index.html')


# 注册负责人验证
def regis_check_pri(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        if len(username) > 20 or len(username) < 4 or not username:
            err1 = '用户名格式错误'
            return render(request, 'society/baseone/register.html', locals())
        principal = Principal.objects.filter(username=username)
        principal1 = Principal.objects.filter(phone=phone)
        if len(principal) > 0 or len(principal1) > 0:
            err1 = '用户或手机号已存在'
            return render(request, 'society/baseone/register.html', locals())
        else:
            if judge_pass(password) is None or password != password2:
                err2 = '密码错误或不一致'
                return render(request, 'society/baseone/register.html', locals())
            if judge_phone(phone) is None:
                err3 = '手机号格式错误'
                return render(request, 'society/baseone/register.html', locals())
            note_ran = request.session.get('note_ran', None)
            if note_ran is not None:
                if request.POST['code'] == note_ran:
                    del request.session['note_ran']
                    mass_name = request.POST.get('mass_name')
                    if Corporate.objects.filter(name=mass_name).exists():
                        corporate = Corporate.objects.get(name=mass_name)
                        mass_code = request.POST.get('mass_code')
                        if corporate.mass_code == mass_code:
                            password = add_pass(password)
                            principal = Principal.objects.create(username=username, password=password, phone=phone, mass=mass_name, mass_code=mass_code)
                            return HttpResponse(show_message('注册成功', '/pylxh/login/'))
                        else:
                            err6 = '编码错误'
                            return render(request, 'society/baseone/register.html', locals())
                    else:
                        err5 = '该社团不存在'
                        return render(request, 'society/baseone/register.html', locals())
                else:
                    err4 = '验证码错误'
                    return render(request, 'society/baseone/register.html', locals())
            else:
                err4 = '验证码无效'
                return render(request, 'society/baseone/register.html', locals())
    else:
        return render(request, 'society/index.html')


# 忘记密码
def forget_pas(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        note_ran = request.session.get('note_ran', None)
        if password == password2:
            if note_ran is not None:
                if request.POST.get('code') == note_ran:
                    pasnew = add_pass(password)
                    if role == '学生':
                        if Student.objects.filter(phone=phone).exists():
                            student = Student.objects.get(phone=phone)
                            student.password = pasnew
                            student.save()
                            return HttpResponse(show_message('修改成功', '/pylxh/login/'))
                        else:
                            err3 = '该手机号不存在'
                            return render(request, 'society/baseone/forget_pas.html', locals())
                    elif role == '社团负责人':
                        if Principal.objects.filter(phone=phone).exists():
                            pri = Principal.objects.get(phone=phone)
                            pri.password = pasnew
                            pri.save()
                            return HttpResponse(show_message('修改成功', '/pylxh/login/'))
                        else:
                            err3 = '该手机号不存在'
                            return render(request, 'society/baseone/forget_pas.html', locals())
                else:
                    err4 = '验证码错误'
                    return render(request, 'society/baseone/forget_pas.html', locals())
            else:
                err4 = '验证码错误'
                return render(request, 'society/baseone/forget_pas.html', locals())
        else:
            err2 = '密码不一致'
            return render(request, 'society/baseone/forget_pas.html', locals())
    else:
        return render(request, 'society/baseone/forget_pas.html')


# 个人中心界面
def geren(request):
    return render(request, 'society/base2.html')

# 个人资料修改
def change_data(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        if Principal.objects.filter(phone=phone).exists():
            principal = Principal.objects.get(phone=phone)
            if request.method == 'POST':
                form = PriForm(request.POST, request.FILES, instance=principal)
                file_path = str(principal.photo)
                if form.is_valid():
                    full_path =settings.MEDIA_ROOT + file_path
                    if file_path != '20181024/07.jpg':
                        os.remove(full_path)
                    if judge_phone(request.POST.get('phone')):
                        form.save()
                        request.session['phone'] = request.POST['phone']
                        request.session['photo'] = str(principal.photo)
                        request.session['info'] = principal.info
                        messages.info(request, '修改成功')
                        return redirect('society:a')
                    else:
                        return render(request, 'society/basetwo/change_data.html', {'form': form, 'error1': '手机号错误'})
                else:
                    return render(request, 'society/basetwo/change_data.html', {'form': form, 'error1': '数据格式错误'})
            else:
                form = PriForm(instance=principal)
                return render(request, 'society/basetwo/change_data.html', locals())
        else:
            return redirect('society:login')


# 修改密码
def change_pwd(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        if request.method == 'POST':
            phone = request.POST.get('phone')
            if Principal.objects.filter(phone=phone).exists():
                principal = Principal.objects.get(phone=phone)
                old_pwd = request.POST.get('old_pwd')
                old_pwd = add_pass(old_pwd)
                if old_pwd == principal.password:
                    return render(request, 'society/basetwo/change_pwd2.html', locals())
                else:
                    error3 = '密码错误'
                    return render(request, 'society/basetwo/change_pwd.html', locals())
            else:
                error2 = '手机号不存在'
                return render(request, 'society/basetwo/change_pwd.html',locals())

        else:
            return render(request, 'society/basetwo/change_pwd.html')


# 修改密码，成功
def change_pwd2(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if Principal.objects.filter(phone=phone).exists():
            principal = Principal.objects.get(phone=phone)
            new_pwd1 = request.POST.get('new_pwd1')
            new_pwd2 = request.POST.get('new_pwd2')
            if judge_pass(new_pwd1):
                if new_pwd1 == new_pwd2:
                    password = add_pass(new_pwd1)
                    principal.password = password
                    principal.save()
                    return redirect('society:a')
                else:
                    error2 = '两次密码不一致'
                    return render(request, 'society/basetwo/change_pwd2.html',locals())
            else:
                error1 = '密码格式错误'
                return render(request, 'society/basetwo/change_pwd2.html', locals())
    return redirect('society:a')


# 退出登录
def login_out(request):
    request.session.flush()
    return redirect('society:login')

# 发布内容
def iss_cont(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        if Principal.objects.filter(phone=phone).exists():
            author = Principal.objects.get(phone=phone)
            if request.method == 'POST':
                title = request.POST['title']
                category_id = request.POST['category']
                author_id = Principal.objects.get(username=request.POST['author']).id
                source = request.POST['source']
                digest = request.POST['digest']
                image = request.FILES.get('image')
                if len(title) <= 50 and len(source) <= 50 and len(digest) <= 200 and image.size <= 1024*1024*3:
                    content = request.POST['content']
                    Article.objects.create(title=title, category_id=category_id, source=source, digest=digest,
                                           content=content, pr_user_id=author_id, image=image)
                    # if author.leave_count > 0:
                    #     author.leave_count = author.leave_count - 1
                    #     request.session['leave_count'] = author.leave_count
                    # else:
                    #     author.score = author.score - 10000
                    #     request.session['score'] = author.score
                    author.save()
                    return render(request, 'society/baseone/iss_success.html')
                else:
                    return render(request, 'society/baseone/iss_content.html', {'error': '标题，来源，摘要，图片大小错误'})
            else:
                return render(request, 'society/baseone/iss_content.html')
        else:
            return redirect('society:login')


# 我的发布
def my_iss(request, a):
    phone = request.session.get('phone', False)
    if phone is False:
        print('----------------------------')
        return redirect('society:login')
    else:
        if Principal.objects.filter(phone=phone).exists():
            author = Principal.objects.get(phone=phone)
            if len(author.articles.all()) > 0:
                if a in [0, 1, 2]:
                    article_list = author.articles.filter(status=a).order_by('-distribute_date')
                else:
                    article_list = author.articles.all().order_by('-distribute_date')
                page = request.GET.get('page')
                page_yeshu = 4
                contacts = page_aduit(article_list, page, page_yeshu)
                return render(request, 'society/basetwo/my_iss.html', {'contacts': contacts})
            else:
                return render(request, 'society/basetwo/my_iss_no.html')
        else:
            print('++++++++++++++++++++++++++++')
            return redirect('society:login')


# 我的会员
def my_vip(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        if Principal.objects.filter(phone=phone).exists():
            author = Principal.objects.get(phone=phone)
            consumes_list = author.consumes.all()
            page = request.GET.get('page')
            page_yeshu = 10
            contacts = page_aduit(consumes_list, page, page_yeshu)
            return render(request, 'society/basetwo/my_vip.html', {'contacts': contacts})
        else:
            return redirect('society:login')


# 我的积分
def my_score(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        if Principal.objects.filter(phone=phone).exists():
            author = Principal.objects.get(phone=phone)
            bills_list = author.bills.all()
            page = request.GET.get('page')
            page_yeshu = 10
            contacts = page_aduit(bills_list, page, page_yeshu)
            return render(request, 'society/basetwo/my_score.html', {'contacts': contacts})
        else:
            return redirect('society:login')


# 支付
def pay(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        if request.method == 'POST':
            author = Principal.objects.get(phone=phone)
            money = int(request.POST['money']) * 1000
            author.money = author.money + money
            author.score = author.score + money * 10
            if money >= 2000 and money < 5000 and author.vip <= 1:
                author.vip = 1
                author.leave_count = 2
            elif money >= 5000 and money < 10000 and author.vip <= 2:
                author.vip = 2
                author.leave_count = 5
            elif money >= 10000 and author.vip <= 3:
                author.vip = 3
                author.leave_count = 10
            request.session['vip'] = author.vip
            request.session['leave_count'] = author.leave_count
            request.session['score'] = author.score
            author.save()
            consume = Consume()
            consume.title = '交易编号' + str(int(time.time()))
            consume.tran_money = money
            consume.author_id = author.id
            consume.save()
            return redirect('society:main')
        else:
            return render(request, 'society/baseone/pay.html')


# 积分兑换
def gift_ex(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        if request.method == 'POST':
            if request.POST['score']:
                score = request.POST['score']
                if Principal.objects.filter(phone=phone).exists():
                    author = Principal.objects.get(phone=phone)
                    use_score = author.score
                    score_new = use_score - int(score) * 10000
                    if score_new >= 0:
                        author.score = score_new
                        author.leave_count = author.leave_count + int(score)
                        author.save()
                        request.session['leave_count'] = author.leave_count
                        request.session['score'] = score_new
                        Bill.objects.create(author_id=author.id, title='积分兑换', score=int(score) * 10000)
                        return redirect('society:main')
                    else:
                        return render(request, 'society/baseone/gift_exchange.html', {'error': '余额不足'})
                else:
                    return redirect('society:login')
            else:
                return redirect('society:login')
        else:
            return render(request, 'society/baseone/gift_exchange.html')


# 消息通知
def new_message(request):
    phone = request.session.get('phone',False)
    if phone is False:
        return redirect('society:login')
    else:
        if Principal.objects.filter(phone=phone).exists():
            author = Principal.objects.get(phone=phone)
            article_list = author.articles.all()
            mess_list = []
            for article in article_list:
                art_mess = article.article_mess.all()
                for mess in art_mess:
                    mess_list.append(mess)
            page = request.GET.get('page')
            page_yeshu = 15
            contacts = page_aduit(mess_list, page, page_yeshu)
            return render(request, 'society/basetwo/new_message.html', {'contacts': contacts})
        else:
            return redirect('society:login')


# 首页
def main(request):
    category = request.get_signed_cookie('category', default='1', salt='waige')
    if category == '1':
        article_list = Article.objects.filter(category_id=1, status=1).order_by('-distribute_date')
    else:
        article_list = Article.objects.filter(category_id=category, status=1).order_by('-distribute_date')
    articles = article_list[:7]
    # 快讯
    flash_list = Article.objects.filter(status=1).order_by('-distribute_date')[:6]
    hotnew_list = Article.objects.filter(status=1).order_by('-votes_count')[:5]
    return render(request, 'society/main.html', {'articles': articles, 'category': category, 'flash_list': flash_list, 'hotnew_list': hotnew_list})


# 首页ajax跳转类型
def main_type(request, a):
    article_list = Article.objects.filter(category_id=a,status=1).order_by('-distribute_date')
    no_many = 'aaa'
    if request.GET.get('cb'):
        cb = request.GET.get('cb')
        cb = int(cb)
        if not cb:
            articles = article_list[:7]
        else:
            articles = article_list[0:7*(cb+1)]
            if 7*(cb+1) >= len(article_list):
                no_many = 'b'
    else:
        articles = article_list[:7]
    rep = render(request, 'society/basethree/main_type.html', {'articles': articles, 'no_many': no_many})
    rep.set_signed_cookie('category', a, salt='waige')
    return rep


# 快讯all
def flash(request):
    flash_list = Article.objects.filter(status=1).order_by('-distribute_date')[:7]
    hotnew_list = Article.objects.filter(status=1).order_by('-votes_count')[:5]
    return render(request, 'society/basethree/flash_all.html', {'flash_list': flash_list, 'hotnew_list': hotnew_list})


from datetime import datetime
# 快讯详情
def flash_detail(request, id):
    if Article.objects.filter(id=id).exists():
        fldate = Article.objects.get(id=id)
        fldate.view_count = fldate.view_count + 1
        fldate.save()
        hotnew_list = Article.objects.filter(status=1).order_by('-votes_count')[:5]
        now_week = datetime.now().weekday()
        now_we = week_chinese(now_week)
        return render(request, 'society/basethree/flash_detail.html', {'fldate': fldate, 'hotnew_list': hotnew_list, 'now_we': now_we})
    else:
        redirect('society:main')


# 文章详情
def article_deta(request, id):
    if Article.objects.filter(id=id).exists():
        essay_deta = Article.objects.get(id=id)
        phone = request.session.get('phone', False)
        if phone is False:
            error = 23
        else:
            shvo_list = Sharevote.objects.filter(article_id=id)
            author = Principal.objects.get(phone=phone)
            if len(shvo_list) > 0:
                shvo_auth = [x.pr_user_id for x in shvo_list]
                if author.id in shvo_auth:
                    index = shvo_auth.index(author.id)
                    yn = shvo_list[index].yesno
                    if yn == 1:
                        error = 24
                    else:
                        error = 22
                else:
                    error = 22
                    Sharevote.objects.create(article_id=id, pr_user_id=author.id)
                    essay_deta.view_count = essay_deta.view_count + 1
            else:
                error = 22
                Sharevote.objects.create(article_id=id, pr_user_id=author.id)
                essay_deta.view_count = essay_deta.view_count + 1
                essay_deta.save()
        hotnew_list = Article.objects.filter(status=1).order_by('-votes_count')[:5]
        return render(request, 'society/basethree/article_deta.html', {'essay_deta': essay_deta, 'hotnew_list': hotnew_list, 'error': error})
    else:
        return redirect('society:main')


# 点赞
@csrf_exempt
def di_vote(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        id = request.POST.get('ca')
        if Article.objects.filter(id=id).exists():
            article = Article.objects.get(id=id)
            vote_new = int(request.POST.get('vote'))
            vote_old = article.votes_count
            article.votes_count = vote_new
            author = Principal.objects.get(phone=phone)
            shvo = Sharevote.objects.get(student_id=author.id, article_id=id)
            if vote_new > vote_old:
                shvo.yesno = 1
            else:
                shvo.yesno = 0
            shvo.save()
            article.save()
            return JsonResponse({'vote': article.votes_count})
        else:
            return redirect('society:main')


# 分享
def share_arti(request, id):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        id = id
        if Article.objects.filter(id=id).exists():
            article = Article.objects.get(id=id)
            article.share_count = article.share_count + 1
            article.save()
            return render(request, 'society/basethree/share_success.html', {'id': id})
        else:
            return redirect('society:main')


# 分享成功
def share_success(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        xz = request.POST.get('sele')
        id = int(request.POST.get('hehe'))
        if Principal.objects.filter(phone=phone).exists():
            author = Principal.objects.get(phone=phone)
            author.score = author.score + 50
            author.save()
            bill = Bill()
            bill.title = '分享文章'
            bill.tran_money = 50
            bill.author_id = author.id
            bill.save()
            if xz == '是':
                return redirect('society:article_deta', id)
            else:
                return redirect('society:main')



# 评论
@csrf_exempt
def comm(request):
    phone = request.session.get('phone', False)
    if phone is False:
        return redirect('society:login')
    else:
        id = request.POST.get('ca')
        if Article.objects.filter(id=id).exists():
            content = request.POST.get('content')
            article = Article.objects.get(id=id)
            user = Principal.objects.get(phone=phone)
            Comment.objects.create(article_id=article.id,content=content)
            Message.objects.create(pr_user_id=user.id, article_id=article.id, content=content)
            return JsonResponse({'suce': '评论成功'})
        else:
            return JsonResponse({'suce': '评论失败'})



# 短信验证
def note_code(request):
    smsapi = "http://api.smsbao.com/"
    # 短信平台账号
    user = 'lxh1771'
    # 短信平台密码
    password = add_pass('lu1121729992')
    # 要发送的短信内容
    note_ran = random.randint(1000, 9999)
    content = "【小灰系统】您的验证码是"+ str(note_ran) + "。如非本人操作，请忽略本短信。该验证码将在30分钟内有效"
    # 要发送短信的手机号码
    phone = request.POST['phone']
    print(phone)
    data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    request.session['note_ran'] = str(note_ran)
    request.session.set_expiry(180)
    return JsonResponse({'error3': '发送成功'})