from django.urls import path
from .views import get_emotion_result_api, save_emotion_result

urlpatterns = [
    path('api/emotion-results/', save_emotion_result),
    path('api/emotions/<int:user_id>/', get_emotion_result_api), 
]
