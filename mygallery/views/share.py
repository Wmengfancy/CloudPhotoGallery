from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from datetime import datetime

# Create your views here.
from mygallery.models import photo, album, user, comment, category

def index(request,pIndex=1):
    '''浏览信息'''
    user1 = request.session.get("userinfo", {})
    ulist = category.objects.all()
    mywhere=[]
    #获取并判断搜索条件
    kw = request.GET.get("keyword1",None)
    if kw:
        ulist = ulist.filter(Category_name__contains=kw)
        for u in ulist:
            paged_photos = photo.objects.filter(Category_id=u.id)
        userlist = user.objects.all()
        albumlist = album.objects.all()
        commentlist = comment.objects.all()
        paginator = Paginator(paged_photos, 5)
        page_number = request.GET.get('page')
        photolist = paginator.get_page(page_number)
        context = {'photolist': photolist, 'userlist': userlist, 'user1': user1, 'albumlist': albumlist,
                   'commentlist': commentlist}
        return render(request, "mygallery/share/list.html", context)

def webindex(request):
    '''首页 '''
    user1 = request.session.get("userinfo", {})
    paged_photos = photo.objects.filter(Photo_visible=1)
    userlist = user.objects.all()
    albumlist = album.objects.all()
    commentlist = comment.objects.all()
    paginator = Paginator(paged_photos, 5)
    page_number = request.GET.get('page')
    photolist = paginator.get_page(page_number)
    context = {'photolist': photolist,'userlist':userlist,'user1':user1,'albumlist':albumlist,'commentlist':commentlist}
    return render(request, "mygallery/share/list.html", context)

def fetch_albums(request):
    albums       = album.objects.values()
    paginator    = Paginator(albums, 5)
    page_number  = int(request.GET.get('page'))
    data         = {}

    if page_number <= paginator.num_pages:
        paged_photos = paginator.get_page(page_number)
        data.update({'photos': list(paged_photos)})

    return JsonResponse(data)
#
# def upload(request,eid):
#     '''加载上传表单页'''
#     albumlist=album.objects.all()
#     request.session['photoid']=eid
#     context={"albumlist":albumlist}
#     return render(request,'mygallery/share/list.html',context)

def comment_upload(request,eid):
    # referer = request.META.get('HTTP_REFERER',reverse('home'))
    if request.method=='POST':
        # Comment_content = request.POST.get('Comment_content')
        # if Comment_content =='':
        #     return render(request,)
        comment1_content = request.POST.get('Comment_content')
        user=request.session.get("userinfo",{})
        img_id=eid
        print(img_id)
        comment_up=comment(Comment_content=comment1_content,Comment_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),Photo_id=img_id,Commentators_id=user['id'])
        comment_up.save()
    return redirect(reverse('mygallery_share_webindex'))

