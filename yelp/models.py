# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class YelpUsers(models.Model):
    name = models.CharField(max_length=40)
    yelp_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class YelpCategories(models.Model):
    name = models.CharField(max_length=50)
    yelp_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Restaurants(models.Model):
    name = models.CharField(max_length=90)
    similar = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class YelpCombo(models.Model):
    userCat = models.CharField(max_length=90)
    names = models.ManyToManyField(Restaurants, through='Combine', blank=True)

    def __str__(self):
        return self.userCat


class Combine(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    combo = models.ForeignKey(YelpCombo, on_delete=models.CASCADE)
    rank = models.IntegerField()





