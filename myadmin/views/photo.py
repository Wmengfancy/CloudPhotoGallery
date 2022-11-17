#相片信息管理视图文件
import random

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from mygallery.models import user, album, photo, category
from django.db.models import Q
from datetime import datetime

# Create your views here.

def index(request,pIndex=1):
    '''浏览信息'''
    phlist = photo.objects.all()
    mywhere=[]
    pholist = []
    photlist = []
    phottlist = []

    #获取Owner_id对应的用户名并封装成新的list
    for vo in phlist:
        alname = album.objects.get(id=vo.Album_id).Album_name  #相册名称
        alob = album.objects.get(id=vo.Album_id)
        caname = category.objects.get(id=vo.Category_id).Category_name  #分类名称
        usname = user.objects.get(id = alob.Owner_id).User_name  #上传用户
        p = {'id':vo.id, 'Photo_name':vo.Photo_name,'Photo_description':vo.Photo_description,
                'Photo_addtime':vo.Photo_addtime,'Photo_visible':vo.Photo_visible,
                'Photo_link':vo.Photo_link,'Album_name':alname,'Owner_name':usname,'Category_name':caname}
        pholist.append(p)
    finallist = pholist

    # #获取并判断搜索条件
    # kw = request.GET.get("keyword",None)
    # if kw:
    #     ulist = user.objects.all().filter(User_name__contains=kw)
    #     for vo in ulist:
    #         usname = vo.User_name
    #         albumlist = album.objects.filter(Owner_id=vo.id)
    #         for va in albumlist:
    #             alname = va.Album_name
    #             photolist = photo.objects.filter(Album_id=va.id)
    #             for vp in photolist:
    #                 caname = category.objects.get(id=vo.Category_id).Category_name  # 分类名称
    #                 p = {'id':vp.id,'Photo_name':vp.Photo_name,'Photo_description':vp.Photo_description,
    #                 'Photo_addtime':vp.Photo_addtime,'Photo_visible':vp.Photo_visible,
    #                 'Photo_link':vp.Photo_link,'Album_name':alname,'Owner_name':usname,'Category_name':caname}
    #                 photlist.append(p)
    #     finallist = photlist
    #     mywhere.append('keyword='+kw)

    # 获取、判断并封装Album_name+User_name搜索条件，用于Album管理表点击相册名称，直接跳转并查看对应的照片
    Album_name = request.GET.get('Album_name', '')
    User_name = request.GET.get('User_name', '')
    if Album_name != '' and User_name != '':
        uob = user.objects.all().get(User_name=User_name)
        aob = album.objects.all().get(Q(Album_name=Album_name) & Q(Owner_id=uob.id))
        photolist = photo.objects.filter(Album_id=aob.id)
        for vo in photolist:
            caname = category.objects.get(id=vo.Category_id).Category_name  # 分类名称
            p = {'id': vo.id, 'Photo_name': vo.Photo_name, 'Photo_description': vo.Photo_description,
                 'Photo_addtime': vo.Photo_addtime, 'Photo_visible': vo.Photo_visible,
                 'Photo_link': vo.Photo_link, 'Album_name': Album_name, 'Owner_name': User_name, 'Category_name': caname}
            phottlist.append(p)
        finallist = phottlist
        mywhere.append("User_name=" + User_name)
        mywhere.append('Album_name=' + Album_name)

    # alist = alist.order_by("id")#对id排序 暂时注释掉，因为会影响搜索功能
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(finallist,4) #以每页4条数据分页
    maxpages = page.num_pages
    #判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #获取当前页数据
    plist = page.page_range #获取页码列表信息

    checkcount = user.objects.filter(User_check=0).count()

    context = {"photolist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'checkcount':checkcount}
    return render(request,"myadmin/photo/index.html",context)

def add(request):
    '''加载信息添加表单'''
    pass

def insert(request):
    '''执行信息添加'''
    pass

def delete(request,cid=0):
    '''执行信息删除'''
    checkcount = user.objects.filter(User_check=0).count()
    try:
        ob = photo.objects.get(id=cid)
        ob.Photo_visible = -1
        ob.save()
        context = {'info':"打回成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "打回失败",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

def recover(request,cid=0):
    '''执行照片恢复'''
    checkcount = user.objects.filter(User_check=0).count()
    try:
        ob = photo.objects.get(id=cid)
        ob.Photo_visible = 0
        ob.save()
        context = {'info':"恢复成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "恢复失败",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

def edit(request,uid=0):
    '''加载信息编辑表单'''
    pass

def update(request,uid=0):
    '''执行信息编辑'''
    pass

