# -*- coding: utf-8 -*-
import os

from django.db import models



class Document(models.Model):
    #docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    docfile = models.FileField(upload_to='documents')

    def filename(self):
        return os.path.basename(self.docfile.name)
    def pathfilename(self):
        return self.docfile.name
