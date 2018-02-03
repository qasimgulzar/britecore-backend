from django.conf.urls import include, url
from rest_framework import routers

from api.views import InsurrersViewSet, FieldsViewSet, FieldValueViewSet

router = routers.DefaultRouter()
router.register(r'insurers', InsurrersViewSet)
router.register(r'fields', FieldsViewSet)
router.register(r'risks', FieldValueViewSet,base_name='risks')

urlpatterns=[
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls'))

]