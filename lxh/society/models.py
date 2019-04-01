from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# 管理员
class AdminUser(User):
    info = models.CharField(max_length=200)


# 学生，游客
class Student(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=32)
    photo = models.ImageField(upload_to='%Y%m%d/',default='20181024/07.jpg')
    phone = models.CharField(max_length=11, unique=True)
    info = models.CharField(max_length=200, default='本人很懒，什么都没留下')
    score = models.PositiveSmallIntegerField(default=0)
    money = models.PositiveSmallIntegerField(default=0)
    choices = (
        (0, '普通用户'),
        (1, 'VIP 1'),
        (2, 'VIP 2'),
        (3, 'VIP 3'),
    )
    vip = models.PositiveSmallIntegerField(choices=choices, default=0)
    leave_count = models.PositiveSmallIntegerField(default=1)

    def validate_unique(self, exclude):
        super().validate_unique(exclude=['username', 'phone'])

    def __str__(self):
        return self.username


# 负责人 (不能评论)
class Principal(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=32)
    photo = models.ImageField(upload_to='%Y%m%d/',default='20181024/07.jpg')
    phone = models.CharField(max_length=11, unique=True)
    info = models.CharField(max_length=200, default='本人很懒，什么都没留下')
    score = models.PositiveSmallIntegerField(default=0)
    money = models.PositiveSmallIntegerField(default=0)
    choices = (
        (0, '普通用户'),
        (1, 'VIP 1'),
        (2, 'VIP 2'),
        (3, 'VIP 3'),
    )
    vip = models.PositiveSmallIntegerField(choices=choices, default=0)
    leave_count = models.PositiveSmallIntegerField(default=1)
    stu_num = models.CharField(max_length=10, default=151210223)
    user_code = models.CharField(max_length=10, default=0)
    mass = models.CharField(max_length=100)
    mass_code = models.CharField(max_length=200,unique=True)
    # vip_time = models.CharField(default=0,max_length=100)

    def validate_unique(self, exclude):
        super().validate_unique(exclude=['username', 'phone', 'mass_code'])

    # def is_expire(self):
    #     return

    def __str__(self):
        return self.username


# 栏目，分类
class Category(models.Model):
    type = models.CharField(max_length=20, unique=True)
    content = models.CharField(max_length=200, default='0')
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.type


# # 社团编码存放
class Corporate(models.Model):
    name = models.CharField(max_length=20)
    mass_code = models.CharField(max_length=200,default=0)

    def __str__(self):
        return self.name


# 社团文章表
class Article(models.Model):
    pr_user = models.ForeignKey(Principal, on_delete=models.CASCADE,related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    source = models.CharField(max_length=50, null=True)
    digest = models.CharField(max_length=200)
    image = models.ImageField(upload_to='article/%Y%m%d/')
    content = models.TextField()
    view_count = models.PositiveSmallIntegerField(default=0)
    votes_count = models.PositiveSmallIntegerField(default=0)
    share_count = models.PositiveSmallIntegerField(default=0)
    distribute_date = models.DateTimeField(auto_now_add=True)
    status_choice = (
        (0, '待审核'),
        (1, '已发布'),
        (2, '未通过'),
    )
    status = models.PositiveSmallIntegerField(choices=status_choice, default=0)

    def __str__(self):
        return self.title


# 消息，回复表
class Message(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_messages', blank=True, null=True)
    pr_user = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name='messages')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_mess')
    content = models.CharField(max_length=100)
    send_time = models.DateTimeField(auto_now_add=True)


# 评论表
class Comment(models.Model):
    pr_user = models.ForeignKey(Principal, related_name='stu_coms', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    send_time = models.DateTimeField(auto_now_add=True)


# 观察，点赞
class Sharevote(models.Model):
    pr_user = models.ForeignKey(Principal, on_delete=models.DO_NOTHING, related_name='stu_shares')
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name='arti_shares')
    yesno = models.PositiveSmallIntegerField(default=0)


# 积分账单表
class Bill(models.Model):
    author = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name='bills')
    title = models.CharField(max_length=20, default='分享文章')
    score = models.CharField(max_length=10, default='+50')
    cost_date = models.DateTimeField(auto_now_add=True)


# 消费记录表
class Consume(models.Model):
    author = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name='consumes')
    title = models.CharField(max_length=200)
    tran_money = models.PositiveSmallIntegerField(default=0)
    tran_date = models.DateTimeField(auto_now_add=True)


# 系统信息表
# class dx(models.Model):