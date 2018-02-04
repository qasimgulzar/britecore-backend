# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Max
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

# {
#     "id": 1,
#     "name": "ABC",
#     "address": "ABC",
#     "insurer":1
# }
class FieldValueViewSet(viewsets.ViewSet):
    def create(self, request,*args, **kwargs):
        response={}
        insurer=request.data.get("insurer",None)
        entity_id=int(FieldValues.objects.all().aggregate(Max("entity_id"))["entity_id__max"] or 0)+1
        if not insurer:
            response["insurer"]="insurer field is required"
            return Response(response)
        insurer=Insurers.objects.filter(pk=insurer).first()
        if not insurer:
            response["insurer"]="invalid does not exist"
            return Response(response)
        fields=Fields.objects.filter(insurres=insurer)
        for field in fields:
            value=request.data.get(field.field_name,None)
            FieldValues.objects.create(entity_id=entity_id,field=field,insurres=insurer,dtype=field.dtype,value=value)
        return Response(request.data)

    def list(self,request):
        insurer = Insurers.objects.all()
        entities={}
        for ins in insurer:
            fields=FieldValues.objects.filter(insurres=ins)
            for field in fields:
                if str(field.entity_id) not in entities:
                    entities[str(field.entity_id)]={'id':field.entity_id,'insurer':field.insurres.id}
                entities[str(field.entity_id)][field.field.field_name]=field.value
        list = []
        for ent in entities:
            list.append(entities[ent])
        return Response(list)

    def retrieve(self, request, pk=None):
        fields=FieldValues.objects.filter(entity_id=int(pk))
        entity={'id':int(pk)}
        for field in fields:
            if 'insurer' not in entity:
                entity['insurer']=field.insurres.id
            entity[field.field.field_name]=field.value
        return Response(entity)


    def destroy(self, request, pk=None):
        FieldValues.objects.filter(entity_id=int(pk)).delete()
        return Response()