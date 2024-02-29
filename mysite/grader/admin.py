from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Question)
admin.site.register(models.Essay)
admin.site.register(models.Form_Question)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Profile)

