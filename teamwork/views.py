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


def get_wanted_detail(request):
    wanted_id = request.GET.get("_id");
    wanted = Wanted.objects.get(id=wanted_id)
    if wanted:
        data = {"code": 0,
                "title": wanted.title,
                "head": wanted.publisher.head_portrait.url,
                "user_name": wanted.publisher.user_name,
                "pub_time": str(wanted.publish_time)[0:16],
                "desc": wanted.desc,
                "tel": wanted.contact_number,
                "email": wanted.contact_email}
    else:
        data = {"code": 1,
                "ret": "data error"}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


def publish(request):
    data = json.loads(request.body)
    publisher_email = data["publisher_email"]
    title = data["title"]
    desc = data["desc"]
    tel = data["tel"]
    email = data["email"]
    tags = data["tags"].split('；')
    author = User.objects.get(email=publisher_email)
    try:
        new_wanted = Wanted.objects.create(title=title,
                                           desc=desc,
                                           contact_number=tel,
                                           contact_email=email,
                                           publisher=author)
        for tag_name in tags:
            tag = Tag.objects.filter(name=tag_name).first()
            if tag:
                new_wanted.tags.add(tag)
            else:
                tag = Tag.objects.create(name=tag_name)
                new_wanted.tags.add(tag)
        return HttpResponse(json.dumps({
            'code': 0,
        }), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
        }), content_type="application/json,charset=utf-8")
