import json
from django.http import HttpResponse
from django.shortcuts import render

from myauth.models import Grade, Major
from .models import Resource, Course


# Create your views here.
def index(request):
    return HttpResponse("You're at the download index")


def get_resource_list(request):
    resource_belong_to_grade = request.GET.get("grade")
    resource_belong_to_major = request.GET.get("major")
    print(resource_belong_to_grade, resource_belong_to_major)
    data_list = []
    query_set = Resource.objects.none()
    if resource_belong_to_grade == "null" and resource_belong_to_major == 'null':
        resource_data = Resource.objects.all()
        for i, resource in enumerate(resource_data):
            resource_info = {'name': resource.name,
                             'desc': resource.desc,
                             'icon_url': resource.icon.url,
                             'download_url': resource.download_url,
                             'belong_to_course': resource.belong_to_course.name, }
            data_list.append(resource_info)
    else:
        if resource_belong_to_major == "null":
            courses = Course.objects.filter(belong_to_grade=Grade.objects.get(grade=resource_belong_to_grade))
            for i, course in enumerate(courses):
                query_set = query_set.union(Resource.objects.filter(belong_to_course=course))
        elif resource_belong_to_grade == "null":
            courses = Course.objects.filter(belong_to_major=Major.objects.get(short_name=resource_belong_to_major))
            for i, course in enumerate(courses):
                query_set = query_set.union(Resource.objects.filter(belong_to_course=course))
        else:
            courses = Course.objects.filter(belong_to_major=Major.objects.get(short_name=resource_belong_to_major),
                                            belong_to_grade=Grade.objects.get(grade=resource_belong_to_grade))
            print(len(courses))
            for i, course in enumerate(courses):
                query_set = query_set.union(Resource.objects.filter(belong_to_course=course))
            print(len(query_set))
        for i, resource in enumerate(query_set):
            resource_info = {'name': resource.name,
                             'desc': resource.desc,
                             'icon_url': resource.icon.url,
                             'download_url': resource.download_url,
                             'belong_to_course': resource.belong_to_course.name, }
            data_list.append(resource_info)
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
