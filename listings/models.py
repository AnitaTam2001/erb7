from django.db import models
from datetime import datetime
from doctors.models import Doctor
# Create your models here.
class Listing(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    services = models.CharField(max_length=200)
    service = models.IntegerField()
    screens = models.CharField(max_length=200)
    screen = models.IntegerField()
    professionals = models.CharField(max_length=200)
    professional = models.IntegerField()
    rooms = models.IntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-list_date',) # - = descending order
        indexes = [models.Index(fields=['list_date'])]

    def __str__(self):
        return self.title
