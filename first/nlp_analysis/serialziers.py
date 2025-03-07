from rest_framework import serializers


# common
class StringListField(serializers.ListField):
    child = serializers.CharField()


# NLPAnlysMorph
class CheckedNLPAnlysMorphSerializer(serializers.Serializer):
    texts = StringListField()
