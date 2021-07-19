#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

from rest_framework import serializers
from rest_framework.fields import IntegerField, CharField

from app.models import DocumentModel
from business.serializers import UserSerializer


class DocumentModelSerializer(serializers.ModelSerializer):
    creator_name = serializers.StringRelatedField(source='creator', read_only=True)
    editor_name = serializers.StringRelatedField(source='editor', read_only=True)
    creator_obj = UserSerializer(read_only=True)
    editor_obj = UserSerializer(read_only=True)
    document_code = CharField(read_only=True)
    document_status = CharField(read_only=True)

    # def save(self, **kwargs):

    class Meta:
        model = DocumentModel
        fields = ('creator_obj', 'editor_obj')
        abstract = True
