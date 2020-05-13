from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import User
from .utils import send_email


# Create your views here.
def index(request):
    return HttpResponse("You're at the myauth index")


def send_auth_code(request):
    print(request.body, request.POST)
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        data = request.POST

    print("请求参数： ", data)
    email = data['email']
    code = data['code']
    print("接收到的发送验证码的请求：", email, code)
    user = User.objects.filter(email=email).first()
    if user:
        result = {"ret": 2, "desc": "用户已存在"}
        print("用户已存在")
    else:
        ret_code, ret_desc = send_email("验证码", code, email)
        if ret_code != 0:
            result = {"ret": ret_code, "desc": '邮件发送失败' + ret_desc}
        else:
            result = {"ret": ret_code, "desc": '验证码已经发送到您的邮箱,请注意查收'}
        return HttpResponse(json.dumps(result), content_type="application/json")


def login(request):
    data = json.loads(request.body)
    print("request args: ", data)
    email = data['email']
    password = data['password']
    print("receive login request:", email, password)
    user = User.objects.filter(email=email).first()
    if not user:
        result = {"ret": 1, "desc": "此用户不存在"}
        print("user not exist")
    else:
        if password == user.password:
            result = {"ret": 0,
                      "desc": "登陆成功",
                      "email": user.email,
                      "password": user.password,
                      "username": user.user_name,
                      "userType": user.user_type,
                      "userDesc": user.desc,
                      "headPortrait": user.head_portrait.url,
                      "belongToMajor": user.belong_to_major.full_name,
                      "belongToGrade": user.belong_to_grade.grade}
            print("login success")
        else:
            result = {"ret": 1, "desc": "密码错误"}
            print("password incorrect")
    return HttpResponse(json.dumps(result), content_type="application/json")