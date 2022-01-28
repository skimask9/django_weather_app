from xml.dom.minidom import CharacterData
from django.db import models


# Create your models here.


class City (models.Model):
    name = models.CharField('City Name' ,max_length=25)


    def __str__(self):
        return self.name
