from rest_framework import serializers
from .models import EmotionResult

class EmotionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionResult
        fields = '__all__'
