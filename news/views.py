import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

from .models import News, Comment
from myauth.models import User

from .utils import classify_pub_time


# Create your views here.
def index(request):
    return HttpResponse("You're at the news index")


def get_news_list(request):
    start = int(request.GET.get('start'))
    end = int(request.GET.get('end'))
    # print(start, end)
    data_list = []
    news_list = News.objects.all()
    max_news_nums = len(news_list)
    # print(max_news_nums)
    if start >= max_news_nums:
        return HttpResponse(json.dumps({
            'code': 2,
            'data': "no more..."
        }, ensure_ascii=False), content_type="application/json,charset=utf-8")
    for i in range(start, min(end, max_news_nums)):
        news = news_list[i]
        news_info = {'_id': news.id,
                     'title': news.title,
                     'desc': news.desc,
                     'img_url': news.thumbnail,
                     'original_url': news.original_url,
                     'content': news.content,
                     'pub_time': str(news.pub_time)[0:10],
                     'total_star': news.total_stars,
                     'cate': news.category.name,
                     'author': news.author.user_name}
        data_list.append(news_info)
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


def get_news_detail(request):
    try:
        news_id = request.GET.get('_id')
        news = News.objects.filter(id=news_id).first()
        if not news:
            return HttpResponse(json.dumps({
                'code': 1,
                'data': "news does not exist"
            }, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data_list = [{'_id': news.id,
                          'title': news.title,
                          'desc': news.desc,
                          'img_url': news.thumbnail,
                          'original_url': news.original_url,
                          'content': news.content,
                          'pub_time': str(news.pub_time)[0:10],
                          'total_star': news.total_stars,
                          'cate': news.category.name,
                          'author': news.author.user_name}]
            return HttpResponse(json.dumps({
                'code': 0,
                'data': data_list
            }, ensure_ascii=False), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
            'data': "connect failed"
        }, ensure_ascii=False), content_type="application/json,charset=utf-8")


def modify_news_stars(request):
    news_id = request.GET.get('_id')
    modified_stars = request.GET.get('modified_stars')
    try:
        news = News.objects.filter(id=news_id).first()
        news.total_stars = modified_stars
        news.save()
        return HttpResponse(json.dumps({
            'code': 0,
        }), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
        }), content_type="application/json,charset=utf-8")


def get_comment_list(request):
    news_id = request.GET.get('_id')
    print(news_id)
    try:
        news = News.objects.get(id=news_id)
        comments_list = news.comments_to_news.all()
        print(len(comments_list))
        data = []
        for i, comment in enumerate(comments_list):
            comment_info = {"comment_id": comment.id,
                            "head_url": comment.author.head_portrait.url,
                            "nickname": comment.author.user_name,
                            "release_time": classify_pub_time(comment.pub_time),
                            "content": comment.content,
                            "total_stars": comment.total_star}
            data.append(comment_info)
        return HttpResponse(json.dumps({
            'code': 0,
            'data': data,
        }), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
            'data': "connect failed",
        }), content_type="application/json,charset=utf-8")


def add_comment(request):
    news_id = request.GET.get("_id")
    user_email = request.GET.get("user_email")
    content_text = request.GET.get("comment_text")
    print(news_id, user_email, content_text)
    pub_time = datetime.datetime.now()
    user = User.objects.get(email=user_email)
    news = News.objects.get(id=news_id)
    if user and news:
        try:
            Comment.objects.create(content=content_text,
                                   pub_time=pub_time,
                                   total_star=0,
                                   news=news,
                                   author=user)
            return HttpResponse(json.dumps({
                'code': 0,
                'data': "pub success"
            }), content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({
                'code': 1,
                'data': "pub failed"
            }), content_type="application/json,charset=utf-8")
    else:
        return HttpResponse(json.dumps({
            'code': 1,
            'data': "pub failed"
        }), content_type="application/json,charset=utf-8")


def modify_comment_stars(request):
    comment_id = request.GET.get('_id')
    modified_stars = request.GET.get('modified_stars')
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.total_stars = modified_stars
        comment.save()
        return HttpResponse(json.dumps({
            'code': 0,
        }), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
        }), content_type="application/json,charset=utf-8")