# -*- coding: utf-8 -*-
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=200, default=None)
    status = models.IntegerField(default=0)
