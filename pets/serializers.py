from rest_framework import serializers
from .models import PetSex
from groups.serializer import GroupSerializer
from traits.serializer import TraintSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=PetSex.choices, default=PetSex.Default)
    group = GroupSerializer()
    traits = TraintSerializer(many=True)
