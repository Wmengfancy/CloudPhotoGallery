from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
# Create your views here.
from mygallery.models import photo, album,category


def webindex(request,Aid):
    '''首页 '''
    paged_photos = photo.objects.filter(Album_id=Aid)
    albumlist = album.objects.filter(id=Aid)
    paginator = Paginator(paged_photos, 6)
    page_number = request.GET.get('page')
    photolist= paginator.get_page(page_number)
    context = {'albumlist': albumlist, 'photolist': photolist}
    return render(request, "mygallery/photo/list.html", context)

def fetch_photos(request):
    photos       = photo.objects.values()
    paginator    = Paginator(photos, 5)
    page_number  = int(request.GET.get('page'))
    data         = {}

    if page_number <= paginator.num_pages:
        paged_photos = paginator.get_page(page_number)
        data.update({'photos': list(paged_photos)})

    return JsonResponse(data)

def upload(request, Bid):
    '''加载上传表单页'''
    albumlist = album.objects.filter(id=Bid)
    request.session['albumid'] = Bid
    categorylist = category.objects.all()
    context = {"albumlist": albumlist, 'categorylist': categorylist}
    return render(request, 'mygallery/photo/upload_photo.html', context)


def doupload(request):
    # 执行是否选择相册判断
    image_valid = ['jpg', 'png', 'jpeg', 'tiff', 'gif', 'bmp']
    error_msg = ""
    if request.method == 'POST':
        album_id = int(request.session['albumid'])
        if request.POST.get('photo_category') == '':
            image_category = None
        else:
            image_category = request.POST.get('photo_category')
        image_name = request.POST.get('photo_name')
        image = request.FILES.get('photo_choosen')
        image_privacy = request.POST.get('flexRadioDefault')
        image_description = request.POST.get('photo_description')
        image_list = (str(image)).split(".")
        if len(image_list) == 1:
            error_msg = "上传图片不能为空!"
            xid = request.session['albumid']
            albumlist = album.objects.filter(id=xid)
            categorylist = category.objects.all()
            context = {"albumlist": albumlist, 'categorylist': categorylist, "error_msg": error_msg}
            return render(request, 'mygallery/photo/upload_photo.html', context)
        elif image_list[1] in image_valid:
            photo_upload = photo(Album_id=album_id, Photo_name=image_name, Photo_description=image_description,
                                 Category_id=image_category, thumb_count=0,
                                 Photo_addtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 Photo_visible=image_privacy,
                                 Photo_link=image)
            photo_upload.save()
            return redirect(reverse('mygallery_photo_webindex', kwargs={'Aid': album_id}))
        else:
            error_msg = "您上传的文件格式不受支持！请正确选择图片上传！"
            xid = request.session['albumid']
            albumlist = album.objects.filter(id=xid)
            categorylist = category.objects.all()
            context = {"albumlist": albumlist, 'categorylist': categorylist, "error_msg": error_msg}

            return render(request, 'mygallery/photo/upload_photo.html', context)


def do_delete_photo(request, Cid):
    photo_id = Cid
    photo_delete = photo.objects.get(id=photo_id)
    photo_ob = photo_delete.toDict()
    Albumid = photo_ob["Album_id"]
    photo_delete.delete()
    messages.success(request, '删除照片成功！')
    return redirect(reverse('mygallery_photo_webindex', kwargs={'Aid': Albumid}))

