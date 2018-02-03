# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from api.api_serializers.Fields_Serializer import FieldSerializer
from api.api_serializers.Insurers_Serializer import InsurerSerializer
from data.models import Insurers, Fields, FieldValues


class InsurrersViewSet(viewsets.ModelViewSet):
    queryset = Insurers.objects.all()
    serializer_class = InsurerSerializer

class FieldsViewSet(viewsets.ModelViewSet):
    queryset = Fields.objects.all()
    serializer_class = FieldSerializer


class FieldValueViewSet(viewsets.ViewSet):
    def list(self,request):
        insurer = Insurers.objects.all()
        entities={}
        for ins in insurer:
            fields=FieldValues.objects.filter(insurres=ins)
            for field in fields:
                if str(field.entity_id) not in entities:
                    entities[str(field.entity_id)]={'id':field.entity_id}
                entities[str(field.entity_id)][field.field.field_name]=field.value
        list = []
        for ent in entities:
            list.append(entities[ent])
        return Response(list)

    def retrieve(self, request, pk=None):
        fields=FieldValues.objects.filter(insurres=pk)
        entity={'id':int(pk)}
        for field in fields:
            entity[field.field.field_name]=field.value
        return Response(entity)