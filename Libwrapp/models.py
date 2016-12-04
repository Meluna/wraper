from django.db import models

class HDD(models.Model):
    name = models.TextField()
    image = models.TextField()
    brand = models.ForeignKey('Brand')
    description = models.TextField()
    interface = models.ForeignKey('Interface')
    volume = models.ForeignKey('Volume')
    speed = models.ForeignKey('Speed')
    page = models.TextField()
    price = models.IntegerField()

class Brand(models.Model):
    name = models.TextField()

class Interface(models.Model):
    name = models.TextField()

class Volume(models.Model):
    name = models.TextField()

class Speed(models.Model):
    name = models.TextField()