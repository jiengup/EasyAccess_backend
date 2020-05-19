from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Wanted(models.Model):
    title = models.CharField(max_length=50, default='')
    desc = models.CharField(max_length=100, default='',
                            null=True,
                            blank=True, )
    publish_time = models.DateTimeField(auto_now_add=True)
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=20, default='',
                                      null=True,
                                      blank=True)
    publisher = models.ForeignKey('myauth.User',
                                  on_delete=models.SET_NULL,
                                  related_name='wanted_who_publish',
                                  null=True,
                                  blank=True,
                                  )
    tags = models.ManyToManyField('Tag',
                                  null=True,
                                  blank=True,
                                  )

    def __str__(self):
        return self.title


