from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from mygallery.models import photo,album,user



def webindex(request):
    '''首页 '''

    #context = {'albumlist': paged_albums}
    user=request.session.get("userinfo",{})
    albumlist = album.objects.filter(Owner_id=user['id'])
    context = {'albumlist': albumlist,'user':user}
    # context = {'albumlist': request.session.get("albumlist",{}).items()}
    return render(request, "mygallery/album/list.html", context)

def oss_home(request):

    albums = album.objects.all()
    photolist = photo.objects.all()
    paginator    = Paginator(albums, 6)
    page_number  = request.GET.get('page')
    paged_albums = paginator.get_page(page_number)
    context      = {'albums': paged_albums, 'photolist':photolist}

    return render(request, 'album/oss_list.html', context)

def fetch_albums(request):
    albums       = album.objects.values()
    paginator    = Paginator(albums, 4)
    page_number  = int(request.GET.get('page'))
    data         = {}

    if page_number <= paginator.num_pages:
        paged_photos = paginator.get_page(page_number)
        data.update({'photos': list(paged_photos)})

    return JsonResponse(data)

def newalbum(request):
    return render(request, "mygallery/album/new_album.html")


def do_add_album(request):
    image_valid = ['jpg', 'png', 'jpeg', 'tiff', 'gif', 'bmp']
    error_msg = ""
    if request.method == 'POST':
        AlbumId = (request.session.get('userinfo'))["id"]
        AlbumId = user.objects.get(id=AlbumId)
        AlbumName = request.POST.get('album_name')
        AlbumCover = request.FILES.get('album_cover')
        AlbumDescription = str(request.POST.get('album_description'))
        if AlbumCover == None:
            AlbumCover = 'static/pics/cover.jpg'
        image_list = (str(AlbumCover)).split(".")
        if image_list[1] not in image_valid:
            error_msg = "您上传的格式不受支持，请正确选择相册封面!"
            return render(request, 'mygallery/album/new_album.html', {"error_msg": error_msg})
        else:
            album_new = album(Owner=AlbumId, Album_name=AlbumName, Album_description=AlbumDescription,
                              Album_addtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cover=AlbumCover)
            album_new.save()
            return redirect(reverse('mygallery_album_webindex'))

def editalbum(request, Did):
    request.session['albumid_edit'] = Did
    albumob = album.objects.filter(id=Did)
    error_msg=""
    album_data = {'albumob': albumob,"error_msg": error_msg}
    return render(request, 'mygallery/album/edit_album.html',  album_data)


def do_edit_album(request):
    image_valid = ['jpg', 'png', 'jpeg', 'tiff', 'gif', 'bmp','webp']
    error_msg = ""
    if request.method == 'POST':
        userId = (request.session.get('userinfo'))["id"]
        userId = user.objects.get(id=userId)
        Albumid = request.session['albumid_edit']
        AlbumName = request.POST.get('album_name')
        AlbumCover = request.FILES.get('album_cover')
        AlbumDescription = request.POST.get('album_description')
        '''获取原相册数据'''
        origin_album = album.objects.get(id=Albumid)
        origin_ob = origin_album.toDict()
        origin_cover = origin_ob["cover"]

        if AlbumCover == None:
            album_new = album(id=Albumid, Owner=userId, Album_name=AlbumName, Album_description=AlbumDescription,
                              cover=origin_cover)
            album_new.save()
            return redirect(reverse('mygallery_album_webindex'))
        else:
            image_list = (str(AlbumCover)).split(".")
            if image_list[1] not in image_valid:
                error_msg = "您上传的格式不受支持，请正确选择相册封面!"
                albumob = album.objects.filter(id=request.session['albumid_edit'])
                album_data = {'albumob': albumob,"error_msg": error_msg}
                return render(request, 'mygallery/album/edit_album.html', album_data)
            else:
                album_new = album(id=Albumid, Owner=userId, Album_name=AlbumName, Album_description=AlbumDescription,
                                  cover=AlbumCover)
                album_new.save()
                return redirect(reverse('mygallery_album_webindex'))


def do_delete_album(request, Eid):
    album_id = Eid
    album_delete = album.objects.get(id=album_id)
    album_delete.delete()
    messages.success(request, '删除相册成功')
    return redirect(reverse('mygallery_album_webindex'))

