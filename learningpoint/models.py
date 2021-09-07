from django.db import models
from datetime import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s-%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)
    
class Newusers(models.Model):
    firstName = models.CharField(max_length=20,default='')
    lastName = models.CharField(max_length=20,default='')
    phoneNumber = models.CharField(max_length=15,default='')
    expert = models.CharField(max_length=15,default='')
    point = models.CharField(max_length=5,default='')
    Email = models.CharField(max_length=50,default='')
    Username= models.CharField(max_length=30,default='')
    password = models.CharField(max_length=1024,default='')
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now())
    

    class Meta:
        db_table='learningpoint_newusers'

    def isExists(self):
        if Newusers.objects.filter(Email=self.Email):
            return True
        return False 

class Userpost(models.Model):
    publisherId = models.CharField(max_length=20)
    publisherName = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=3072)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'users_post'  
