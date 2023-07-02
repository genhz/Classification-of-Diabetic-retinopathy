import os

import cv2
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render

from . import Fundus_grading
from .models import *


# Create your views here.
def login_views(request):
    return render(request, 'login.html')


def login_views_submit(request):
    u = request.POST.get('user')
    p = request.POST.get('password')
    if u and p:
        user = Patient.objects.filter(pat_id=u, pat_password=p).count()
        if user >= 1:
            request.session["username"] = u
            return render(request, 'index.html')
        else:
            messages.error(request, '用户名或密码不正确')
            return HttpResponseRedirect("/")
    else:
        messages.error(request, '请输入用户名和密码')
        return HttpResponseRedirect("/")


def register_view(request):
    return render(request, 'register.html')

#用户注册
def register_view_submit(request):
    u = request.POST.get('user')
    n = request.POST.get('name')
    a = int(request.POST.get('age'))
    s = request.POST.get('sex')
    ad = request.POST.get('address')
    ph = request.POST.get('phone')
    p1 = request.POST.get('password1')
    p2 = request.POST.get('password2')
    if u and n and a and s and ad and ph and p1 and p2:
        if Patient.objects.filter(pat_id=u):
            messages.error(request, '用户已存在')
            return HttpResponseRedirect("/register")
        elif p1 == p2:
            Patient.objects.create(pat_id=u, pat_phone=ph, pat_name=n, pat_address=ad, pat_password=p1, pat_age=a,
                                   pat_sex=s)
            messages.error(request, '注册成功')
            return HttpResponseRedirect("/")
        else:
            messages.error(request, '两次密码不一致')
            return HttpResponseRedirect("/register")
    else:
        messages.error(request, '请填写完整的表格')
        return HttpResponseRedirect("/register")


def scaleRadius(img, scale):
    x = img[int(img.shape[0] / 2), :, :].sum(1)  # 图像中间1行的像素的3个通道求和。输出（width*1）
    r = (x > x.mean() / 10).sum() / 2  # x均值/10的像素是为眼球，计算半径
    s = scale * 1.0 / r
    return cv2.resize(img, (0, 0), fx=s, fy=s)

#医生注册
def doc_register(request):
    if request.method == 'POST':
        u = request.POST.get('user')
        n = request.POST.get('name')
        a = int(request.POST.get('age'))
        img = request.FILES.get('img')
        img_name=request.FILES.get('img').name
        ranks = request.POST.get('ranks')
        subject = request.POST.get('subject')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        text=request.POST.get('doc_text')
        if u and n and a and img and ranks and subject and p1 and p2:
            if Patient.objects.filter(pat_id=u):
                messages.error(request, '用户已存在')
                return HttpResponseRedirect("/register")
            elif p1 == p2:
                new_doc=Doctor(
                    doc_id=u,
                    doc_name=n,
                    doc_age=a,
                    doc_password=p1,
                    doc_img=img,
                    img_path= './media/img/' + img_name,
                    ranks=ranks,
                    subject=subject,
                    doc_text=text
                )
                new_doc.save()
                messages.error(request, '注册成功')
                return HttpResponseRedirect("/")
            else:
                messages.error(request, '两次密码不一致')
                return HttpResponseRedirect("/register")
        else:
            messages.error(request, '请填写完整的表格')
            return HttpResponseRedirect("/register")
    else:
        return render(request,'doc_register.html')
#系统处理
def grading(request):
    context = {}
    context['title'] = '糖尿病视网膜病变分级系统'
    context['from_local_upload_image'] = '从本地上传图像'
    context['identify_button'] = '识别'
    context['identify_result'] = '识别结果:'
    context['figure'] = '级别:'
    context['time_consuming'] = '识别耗时:'
    context['second'] = '秒'
    context['path'] = './static/src/eyeai_resize.jpg'
    print(context['path'])
    context['identify'], context['time'], context['a0'], context['a1'], context['a2'], context['a3'], context[
        'a4'] = Fundus_grading.main(context['path'])
    try:
        if request.method == 'POST':
            pat_id = request.session.get("username")
            IMG.objects.filter(pat_id_id=pat_id, img_type='dr').delete()
            new_img = IMG(
                pat_id_id=pat_id,
                img=request.FILES.get('img'),
                img_type='dr',
                name=request.FILES.get('img').name
            )
            name = new_img.name
            name = name.replace(' ', '_')
            context['path'] = './media/img/' + name
            path = context['path']
            after_path = context['path'][:-4] + '_resize.jpg'
            context['path'] = after_path
            new_img.after_img = after_path
            # obj=IMG.objects.get(pat_id_id=pat_id,img_type='dr')
            # obj.after_img=after_path
            # obj.save()
            if os.path.exists(path):
                os.remove(path)
            if os.path.exists(after_path):
                os.remove(after_path)
            new_img.save()
            scale = 300
            temp_img = cv2.imread(path)
            temp_img = scaleRadius(temp_img, scale)
            # subtract local mean color
            temp_img = cv2.addWeighted(temp_img, 4,
                                       cv2.GaussianBlur(temp_img, (0, 0), scale / 30, sigmaY=16), -4,
                                       128)
            dim = (224, 224)
            resize_img = cv2.resize(temp_img, dim)
            cv2.imwrite(after_path, resize_img)
            context['identify'], context['time'], context['a0'], context['a1'], context['a2'], context['a3'], context[
                'a4'] = Fundus_grading.main(after_path)
            dr = Dr.objects.get(dr_id=context['identify'])
            context['identify'] = dr.dr_name
            context['advice'] = dr.advice
            img = IMG.objects.get(pat_id_id=pat_id)
            img.rating = context['identify']
            img.save()
            return render(request, 'grading.html', context)

    except AttributeError:
        pass
    else:
        pass
    return render(request, 'grading.html', context)

#患者病例
def pat_case_view(request):
    cases = IMG.objects.filter(pat_id_id=request.session.get("username"))
    context = {'cases': cases}
    return render(request, 'pat_case.html', context)


def appointment(request):
    pat = request.session.get("username")
    doc = request.POST.get("")
    return request

#医生列表
def doc_list_view(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    # render函数：载入模板，并返回context对象
    return render(request, 'docList.html', context)

#医生预约
def doc_appointment(request, id):
    pat_id = request.session.get("username")
    doc_id = id
    if IMG.objects.get(pat_id_id=pat_id):
        user = IMG.objects.get(pat_id_id=pat_id)
        if user.doc_id == 'null':
            img = IMG.objects.get(pat_id_id=pat_id)
            img.doc_id = doc_id
            img.save()
            messages.error(request, '预约成功')
            return HttpResponseRedirect("/docList/")
        else:
            messages.error(request, '请不要重复预约')
            return HttpResponseRedirect("/docList/")
    else:
        messages.error(request, '请先诊断以提交病例')
        return HttpResponseRedirect("/docList/")

#查看医生的病人
def doc_patlist(request):
    id=1
    # id=request.session.get("doc_id")
    doc_pat=Patient.objects.filter(pat_id=0)
    docs=IMG.objects.filter(doc_id=id)
    for doc in docs:
        doc_pats=Patient.objects.filter(pat_id=doc.pat_id_id)
        doc_pat=doc_pat | doc_pats
    context = {'doc_pats':doc_pat}
    return render(request,'doc_patlist.html',context)

#查看病例
def doc_dealcase(request,id):
    doc_deals=IMG.objects.filter(pat_id_id=id)
    context = {'doc_deals':doc_deals}
    doc_pats = Patient.objects.filter(pat_id=id)
    context['doc_pats']=doc_pats
    return render(request,'doc_dealcase.html',context)
#查找病人
def findpatname(request):
    if request.method=='POST':
        patname=request.POST.get('patname')
        id=1
        # id=request.session.get("doc_id")
        doc_pat = Patient.objects.filter(pat_id=0)
        docs = IMG.objects.filter(doc_id=id)
        for doc in docs:
            doc_pats = Patient.objects.filter(pat_id=doc.pat_id_id,pat_name=patname)
            doc_pat = doc_pat | doc_pats
        doc_pats=Patient.objects.filter(pat_name=patname)
        doc_pat=doc_pats & doc_pat
        context = {'doc_pats': doc_pat}
        return render(request, 'doc_patlist_name.html', context)

def updatepropose(request,propose):
    obj = IMG.Publisher.objects.get(id=id)  # 先查询
    obj.propose = propose  # 在内存中修改
    obj.save()  # 将修改保存到数据库


def set_session(request):
    """设置session"""
    request.session["username"] = "jkc"
    return HttpResponse("session_view")


def get_session(request):
    """获取session"""
    username = request.session.get("username")
    return HttpResponse(f"session的值为{username}")


def clear_session(request):
    """清除session"""
    request.session.clear()
    return HttpResponse("清除session成功")

