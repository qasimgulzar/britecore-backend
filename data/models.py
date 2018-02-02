# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.

class Insurers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False, null=False, unique=True)


class Fields(models.Model):
    id = models.AutoField(primary_key=True)
    field_name = models.CharField(max_length=100, blank=False, null=False)
    dtype = models.CharField(max_length=50, blank=False, null=False)
    insurres = models.ForeignKey(Insurers, to_field='id')
    default = models.TextField()
    options = ArrayField(
        models.Field(models.TextField()), blank=True
    )

    class Meta:
        unique_together = (('field_name', 'dtype', 'insurres'),)


class FieldValues(models.Model):
    entity_id = models.IntegerField(blank=False, null=False)
    field = models.ForeignKey(Fields, to_field='id')
    insurres = models.ForeignKey(Insurers, to_field='id')
    dtype = models.CharField(max_length=50, blank=False, null=False)
    value = models.TextField()

    def __str__(self):
        return self.value

    def get_value(self):
        return self.value
