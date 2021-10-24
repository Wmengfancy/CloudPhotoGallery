# Create your models here.
from datetime import datetime

from django.db import models


class photo(models.Model):

    Album_id = models.IntegerField(default=0)
    Photo_name = models.CharField(max_length=50)
    Photo_description = models.CharField(max_length=50)
    Category_id = models.IntegerField(default=0)
    Photo_addtime = models.DateTimeField(default=datetime.now)
    Photo_height = models.IntegerField(default=0)
    Photo_width = models.IntegerField(default=0)
    Photo_link = models.ImageField(upload_to='static/pics')
    thumb_count = models.IntegerField(default=0)
    Photo_visible = models.IntegerField(default=0)

    # class Meta:
    #     ordering = ('-created',)

    def toDict(self):
        return {'id': self.id, 'Album_id': self.Album_id, 'Photo_name': self.Photo_name,
                'Photo_description': self.Photo_description, 'Category_id': self.Category_id, 'Photo_addtime': self.Photo_addtime.strftime('%Y-%m-%d %H:%M:%S'),
                'Photo_height': self.Photo_height, 'Photo_width': self.Photo_width, 'Photo_link': self.Photo_link,
                'thumb_count': self.thumb_count,'Photo_visible':self.Photo_visible}

    class Meta:
        db_table = "photo"  # 更改表名


class album(models.Model):

    Album_name = models.CharField(max_length=50)
    Album_description = models.CharField(max_length=50)
    Owner_id = models.IntegerField(default=0)
    Album_addtime = models.DateTimeField(default=datetime.now)
    Album_password = models.CharField(max_length=50)
    Album_visible = models.IntegerField(default=0)
    photo_count = models.IntegerField(default=0)
    cover = models.CharField(max_length=50)

    def toDict(self):
        return {'id':self.id,'Album_name':self.Album_name,'Album_description':self.Album_description,
                'Album_addtime':self.Album_addtime.strftime('%Y-%m-%d %H:%M:%S'),'Owner_id':self.Owner_id,
                'Album_password':self.Album_password,'Album_visible':self.Album_visible,'photo_count':self.photo_count,
                'cover':self.cover}

    class Meta:
        db_table = "album"  # 更改表名


class category(models.Model):

    Category_name = models.CharField(max_length=50)

    def toDict(self):
        return{'Category_name':self.Category_name}

    class Meta:
        db_table = "category"  # 更改表名


class comment(models.Model):

    Comment_content = models.CharField(max_length=255)
    Owner_id = models.IntegerField(default=0)
    Comment_time = models.DateTimeField(default=datetime.now)
    Photo_id = models.IntegerField(default=0)
    Commentators_id = models.IntegerField(default=0)

    class Meta:
        db_table = "comment"  # 更改表名


class favorites(models.Model):

    Collect_id = models.IntegerField(default=0)
    Collect_data = models.DateTimeField(default=datetime.now)
    Collector_id = models.IntegerField(default=0)
    Photo_id = models.IntegerField(default=0)

    class Meta:
        db_table = "favorites"  # 更改表名
