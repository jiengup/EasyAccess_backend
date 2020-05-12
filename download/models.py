from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100,
                            default='',
                            null=True,
                            blank=True,
                            )
    submit_time = models.DateTimeField(auto_now=True)
    belong_to_grade = models.ForeignKey('myauth.Grade',
                                        on_delete=models.SET_NULL,
                                        related_name='course_of_grade',
                                        null=True,
                                        blank=True,
                                        )
    submitter = models.ForeignKey('myauth.User',
                                  on_delete=models.SET_NULL,
                                  related_name='course_who_submit',
                                  null=True,
                                  blank=True,
                                  )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-submit_time']


class Resource(models.Model):
    name = models.CharField(max_length=50, default='')
    desc = models.CharField(max_length=100,
                            default='',
                            null=True,
                            blank=True,
                            )
    icon = models.ImageField(verbose_name=u'图标',
                             upload_to='icons',
                             null=True,
                             blank=True)
    download_url = models.URLField()

    belong_to_course = models.ForeignKey('Course',
                                         on_delete=models.SET_NULL,
                                         related_name='tools_of_course',
                                         null=True,
                                         blank=True,
                                         )

    def __str__(self):
        return self.name
