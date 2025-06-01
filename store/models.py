from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class EmotionResult(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # letter_id = models.IntegerField()
    # dominant_emotion = models.CharField(max_length=20)
    # detailed_emotion = models.CharField(max_length=30, null=True, blank=True)  # 추가
    # emotion_scores = models.JSONField(null=True, blank=True)  # 예: {"joy": 0.8, ...}
    # created_at = models.DateTimeField(auto_now_add=True)
    # analyzed_at = models.DateTimeField(blank=True, null=True)
    # most_frequent_mood = models.CharField(max_length=100)
    # most_frequent_detailed_mood = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # ✅ emotions 필드 추가 (JSON 형태 추천)
    emotions = models.JSONField(null=True, blank=True)

    most_frequent_mood = models.CharField(max_length=100)
    most_frequent_detailed_mood = models.CharField(max_length=100, null=True, blank=True)
    comfort_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    analyzed_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.dominant_emotion}"
