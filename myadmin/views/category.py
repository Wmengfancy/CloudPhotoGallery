#分类信息管理视图文件
import random

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from mygallery.models import category,user,photo
from django.db.models import Q
from datetime import datetime

# Create your views here.

def index(request,pIndex=1):
    '''浏览信息'''
    mywhere=[]

    # 产生各个分类的相片数量，并连同原表字段合成新表
    catelist = category.objects.all()
    countlist_cate = []
    for vo in catelist:
        photoob = photo.objects.filter(Category_id=vo.id)
        pc = photoob.count()
        c = {'id': vo.id, 'Category_name': vo.Category_name, 'photocount': pc}
        countlist_cate.append(c)
    countlist_cate = sorted(countlist_cate, key=lambda x: x['id'], reverse=False)

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(countlist_cate, 5) #以每页5条数据分页
    maxpages = page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #获取当前页数据
    plist = page.page_range #获取页码列表信息

    checkcount = user.objects.filter(User_check=0).count()

    # 筛选出照片最多的五个分类存入countlist_cate中
    catelist = category.objects.all()
    countlist_cate = []
    for vo in catelist:
        photoob = photo.objects.filter(Category_id=vo.id)
        pc = photoob.count()
        c = {'id': vo.id, 'Category_name': vo.Category_name, 'photocount': pc}
        countlist_cate.append(c)
    countlist_cate = sorted(countlist_cate, key=lambda x: x['photocount'], reverse=True)
    countlist_cate = countlist_cate[0:5]


    context = {"categorylist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'checkcount':checkcount,'countlist_cate':countlist_cate}
    return render(request,"myadmin/category/index.html",context)

def add(request):
    '''加载信息添加表单'''
    checkcount = user.objects.filter(User_check=0).count()
    context = {'checkcount': checkcount}
    return render(request,"myadmin/category/add.html",context)

def insert(request):
    checkcount = user.objects.filter(User_check=0).count()
    '''执行信息添加'''
    try:
        ob = category()
        if request.POST['Category_name'] == '':
            context = {'info': '分类名称不得为空！','checkcount': checkcount}
        else:
            incate = category.objects.filter(Category_name=request.POST['Category_name'])
            if incate:
                context = {'info': '分类已存在！','checkcount': checkcount}
            else:
                ob.Category_name = request.POST['Category_name']
                ob.save()
                context = {'info':"添加成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "添加失败",'checkcount': checkcount}
    return  render(request,"myadmin/category/add.html",context)

def delete(request,cid=0):
    checkcount = user.objects.filter(User_check=0).count()
    '''执行信息删除'''
    try:
        ob = category.objects.get(id=cid)
        ob.delete();
        context = {'info':"删除成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "删除失败",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

def edit(request,cid=0):
    checkcount = user.objects.filter(User_check=0).count()
    '''加载信息编辑表单'''
    try:
        ob = category.objects.get(id=cid)
        context = {'category': ob,'checkcount': checkcount}
        return render(request, "myadmin/category/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

def update(request,cid=0):
    checkcount = user.objects.filter(User_check=0).count()
    '''执行信息编辑'''
    try:
        ob = category.objects.get(id=cid)
        ob.Category_name = request.POST['Category_name']
        ob.save()
        context = {'info': "修改成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "修改失败",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

