from django.db import models


# Create your models here.
class Major(models.Model):
    full_name = models.CharField(max_length=50, default='')
    short_name = models.CharField(max_length=10, default='')
    total_population = models.IntegerField(default=0)

    def __str__(self):
        return self.short_name


class Grade(models.Model):
    grade = models.CharField(max_length=4, default='2020')

    def __str__(self):
        return self.grade


class User(models.Model):
    TEACHER = "TC"
    STUDENT = "SD"
    USER_TYPE_CHOICE = [
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]
    user_name = models.CharField(max_length=20, default='')
    desc = models.CharField(max_length=100, default='')
    user_type = models.CharField(max_length=2,
                                 choices=USER_TYPE_CHOICE,
                                 default=STUDENT)
    head_portrait = models.ImageField(verbose_name=u'头像',
                                      upload_to='portraits',
                                      null=True,
                                      blank=True)
    email = models.EmailField(verbose_name=u'电子邮件', primary_key=True)
    password = models.CharField(verbose_name=u'密码', max_length=20)
    belong_to_major = models.ForeignKey(Major,
                                        on_delete=models.PROTECT,
                                        verbose_name=u'用户所处专业',
                                        related_name='user_major')
    belong_to_grade = models.ForeignKey(Grade,
                                        on_delete=models.PROTECT,
                                        verbose_name=u'学生用户所处年级',
                                        related_name='SD_user_grade',
                                        null=True,
                                        blank=True)

    def __str__(self):
        return self.email
