from rest_framework import serializers

from api.api_serializers.Fields_Serializer import FieldSerializer
from data.models import Insurers


class InsurerSerializer(serializers.ModelSerializer):
    fields=serializers.SerializerMethodField('_get_fields')
    def _get_fields(self,current_object):
        serializer=FieldSerializer(current_object.get_fields(),many=True)
        return serializer.data
    class Meta:
        model = Insurers
        fields='__all__'