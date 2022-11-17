#相册信息管理视图文件
import random

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from mygallery.models import user,album,photo
from django.db.models import Q
from datetime import datetime

# Create your views here.

def index(request,pIndex=1):
    '''浏览信息'''
    alist = album.objects.all()
    mywhere=[]
    alblist = []
    aalist = []

    #获取Owner_id对应的用户名并封装成新的list
    for vo in alist:
        name = user.objects.get(id=vo.Owner_id).User_name
        pc = photo.objects.filter(Album_id=vo.id).count()
        a = {'id':vo.id, 'Album_name':vo.Album_name,'Album_description':vo.Album_description,
            'Album_addtime':vo.Album_addtime,'Album_visible':vo.Album_visible,
            'photo_count':pc,'cover':vo.cover,'Owner_name':name}
        alblist.append(a)
    finallist = alblist

    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        ulist = user.objects.all().filter(User_name__contains=kw)
        for vo in ulist:
            albumlist = alist.filter(Owner_id=vo.id)
            name = vo.User_name
            for va in albumlist:
                pc = photo.objects.filter(Album_id=va.id).count()
                a = {'id':va.id, 'Album_name':va.Album_name,'Album_description':va.Album_description,
                     'Album_addtime':va.Album_addtime,'Album_visible':va.Album_visible,
                     'photo_count':pc,'cover':va.cover,'Owner_name':name}
                aalist.append(a)
        finallist = aalist
        mywhere.append('keyword='+kw)



    # alist = alist.order_by("id")#对id排序 暂时注释掉，因为会影响搜索功能
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(finallist,4) #以每页5条数据分页
    maxpages = page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #获取当前页数据
    plist = page.page_range #获取页码列表信息

    checkcount = user.objects.filter(User_check=0).count()

    context = {"albumlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'checkcount':checkcount}
    return render(request,"myadmin/album/index.html",context)

def add(request):
    '''加载信息添加表单'''
    checkcount = user.objects.filter(User_check=0).count()
    context = {'checkcount':checkcount}
    return render(request,"myadmin/album/add.html",context)

def insert(request):
    checkcount = user.objects.filter(User_check=0).count()
    '''执行信息添加'''
    try:
        ob = album()
        if request.POST['Album_name'] == '':
            context = {'info': '相册名称不得为空！','checkcount': checkcount}
        else:
            if request.POST['Owner_id'] == '':
                context = {'info': '请选择一名执行添加的用户！', 'checkcount': checkcount}
            else:
                inalbum = album.objects.filter(Q(Album_name=request.POST['Album_name']) & Q(Owner_id=request.POST['']))
                if inalbum:
                    context = {'info': '相册名称已被该用户占用！','checkcount': checkcount}
                else:
                    ob.Album_name = request.POST['Album_name']
                    if request.POST['Album_description'] == '':
                        ob.Album_description = None
                    else:
                        ob.Album_description = request.POST['Album_description']
                    ob.Album_addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ob.Album_visible = 0
                    ob.photo_count = 0
                    ob.cover = request.FILES.get('cover')
                    ob.save()
                    context = {'info':"添加成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "添加失败",'checkcount': checkcount}
    return render(request,"myadmin/album/add.html",context)

def delete(request,cid=0):
    '''执行信息删除'''
    checkcount = user.objects.filter(User_check=0).count()
    try:
        ob = album.objects.get(id=cid)
        ob.delete();
        context = {'info':"删除成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "删除失败",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

def edit(request,uid=0):
    '''加载信息编辑表单'''
    checkcount = user.objects.filter(User_check=0).count()
    try:
        ob = album.objects.get(id=uid)
        context = {'album': ob,'checkcount': checkcount}
        return render(request, "myadmin/album/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

def update(request,uid=0):
    checkcount = user.objects.filter(User_check=0).count()
    '''执行信息编辑'''
    try:
        ob = album.objects.get(id=uid)
        inalbum = album.objects.filter(Q(Album_name=request.POST['Album_name']) & Q(Owner_id=request.POST['']))
        if inalbum:
            context = {'info': '相册名称已被该用户占用！', 'checkcount': checkcount}
        else:
            ob.Album_name = request.POST['Album_name']
            if request.POST['Album_description'] == '':
                ob.Album_description = None
            else:
                ob.Album_description = request.POST['Album_description']
            ob.save()
            context = {'info': "修改成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "修改失败",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

