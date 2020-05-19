import json

from django.http import HttpResponse
from django.shortcuts import render

from .models import Tag, Wanted
from myauth.models import User


# Create your views here.
def index(request):
    return HttpResponse("You're at the teamwork index")


def get_tag_list(request):
    tags = Tag.objects.all()
    data_list = []
    for i, tag in enumerate(tags):
        tag_info = {"name": tag.name,
                    "id": tag.id}
        data_list.append(tag_info)
    try:
        return HttpResponse(json.dumps({
            'code': 0,
            'data': data_list,
        }), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
            'data': "failed to connect"
        }, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_teacher_list(request):
    teachers = User.objects.filter(user_type=User.TEACHER)
    data_list = []
    for i, teacher in enumerate(teachers):
        teacher_info = {"name": teacher.user_name,
                        "id": teacher.email}
        data_list.append(teacher_info)
    try:
        return HttpResponse(json.dumps({
            'code': 0,
            'data': data_list,
        }), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
            'data': "failed to connect"
        }, ensure_ascii=False), content_type="application/json,charset=utf-8")


def get_wanted_list(request):
    data = json.loads(request.body)
    pull_tags = data['tags']
    pull_teachers = data['teachers']
    data_list = []
    if len(pull_tags) == 0 and len(pull_teachers) == 0:
        wanteds = Wanted.objects.all()
        for i, wanted in enumerate(wanteds):
            tag_info = {"id": wanted.id,
                        "title": wanted.title}
            data_list.append(tag_info)
    else:
        wanteds = Wanted.objects.none()
        for pull_tag in pull_tags:
            wanteds = wanteds.union(Wanted.objects.filter(tags=Tag.objects.get(id=pull_tag)))
        for pull_teacher in pull_teachers:
            wanteds = wanteds.union(Wanted.objects.filter(publisher=User.objects.get(email=pull_teacher)))
        for i, wanted in enumerate(wanteds):
            tag_info = {"id": wanted.id,
                        "title": wanted.title}
            data_list.append(tag_info)
    try:
        return HttpResponse(json.dumps({
            'code': 0,
            'data': data_list
        }, ensure_ascii=False), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
            'data': "failed to connect"
        }, ensure_ascii=False), content_type="application/json,charset=utf-8")