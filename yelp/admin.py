# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import YelpUsers, YelpCategories, Restaurants, YelpCombo, Combine


admin.site.register(YelpUsers)
admin.site.register(YelpCategories)
admin.site.register(Restaurants)
admin.site.register(YelpCombo)
admin.site.register(Combine)


# Register your models here.
