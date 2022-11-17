#相片信息管理视图文件
import random

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from mygallery.models import user, album, photo, category, comment
from django.db.models import Q
from datetime import datetime

# Create your views here.

def index(request,pIndex=1):
    '''浏览信息'''
    comlist = comment.objects.all()
    mywhere=[]
    commlist = []
    commelist = []

    #获取Commentators_id和Photo_id对应的用户名、照片、以及被评论者的用户名，封装成新的list
    for vo in comlist:
        photoob = photo.objects.get(id=vo.Photo_id)  #获取被评论的照片
        albumob = album.objects.get(id=photoob.Album_id)
        photolink = photoob.Photo_link  #相片链接
        comname = user.objects.get(id=vo.Commentators_id).User_name  #评论者用户名
        usname = user.objects.get(id=albumob.Owner_id).User_name  #被评论照片发布者用户名
        cc = {'id':vo.id, 'Comment_content':vo.Comment_content,'Photo_link':photolink,
                'Comment_time':vo.Comment_time,'Commentators_name':comname,'Owner_name':usname}
        commlist.append(cc)
    finallist = commlist

    # 获取、判断并封装Photo_id搜索条件，用于Photo管理表点击查看评论，直接跳转并查看对应的评论
    Photo_id = request.GET.get('Photo_id', '')
    if Photo_id != '':
        commentlist = comment.objects.filter(Photo_id=Photo_id)
        for vo in commentlist:
            photoob = photo.objects.get(id=vo.Photo_id)  # 获取被评论的照片
            albumob = album.objects.get(id=photoob.Album_id)
            photolink = photoob.Photo_link  # 相片链接
            comname = user.objects.get(id=vo.Commentators_id).User_name  # 评论者用户名
            usname = user.objects.get(id=albumob.Owner_id).User_name  # 被评论照片发布者用户名
            cc = {'id': vo.id, 'Comment_content': vo.Comment_content, 'Photo_link': photolink,
                  'Comment_time': vo.Comment_time, 'Commentators_name': comname, 'Owner_name': usname}
            commelist.append(cc)
        finallist = commelist
        mywhere.append("Photo_id" + Photo_id)

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

    context = {"commentlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'checkcount':checkcount}
    return render(request,"myadmin/comment/index.html",context)

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
        ob = comment.objects.get(id=cid)
        ob.Comment_content = '* 该评论涉嫌违规已被管理员清除'
        ob.save()
        context = {'info':"删除成功",'checkcount': checkcount}
    except Exception as err:
        print(err)
        context = {'info': "删除失败",'checkcount': checkcount}
    return render(request, "myadmin/info.html", context)

def edit(request,uid=0):
    '''加载信息编辑表单'''
    pass

def update(request,uid=0):
    '''执行信息编辑'''
    pass



