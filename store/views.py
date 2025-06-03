from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import EmotionResult
from .serializers import EmotionResultSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from store.publisher import publish_recommendation_message
import traceback
from rest_framework.permissions import IsAuthenticated
import pika
import json

User = get_user_model()

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_emotion_result(request):
    user = request.user
    data = request.data.copy()
    data["user"] = user.id  # ✅ 객체로 변경된 인증 클래스에 맞게 수정

    serializer = EmotionResultSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmotionResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user  # ✅ 객체 그대로 사용
            result = EmotionResult.objects.create(
                user=user,
                letter_id=request.data["letter_id"],
                dominant_emotion=request.data["dominant_emotion"],
                detailed_emotion=request.data.get("detailed_emotion"),
                emotion_scores=request.data.get("emotion_scores", {}),
            )

            publish_recommendation_message({
                "user": user.id,
                "mood": result.dominant_emotion
            })

            return Response({"id": result.id}, status=201)

        except Exception as e:
            return Response({
                "error": str(e),
                "trace": traceback.format_exc()
            }, status=400)


def publish_to_recommendation_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='recommendation.direct', exchange_type='direct')

    channel.basic_publish(
        exchange='recommendation.direct',
        routing_key='recommend',
        body=json.dumps(data)
    )
    connection.close()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_emotion_result_api(request):
    user_id = request.user.id  # ✅ 수정
    try:
        results = EmotionResult.objects.filter(user_id=user_id).order_by('-analyzed_at')
        data = [
            {
                "most_frequent_mood": r.most_frequent_mood,
                "most_frequent_detailed_mood": r.most_frequent_detailed_mood,
                "emotions": r.emotions,
                "comfort_message": r.comfort_message,
            }
            for r in results
        ]
        return JsonResponse({"results": data})
    except EmotionResult.DoesNotExist:
        return JsonResponse({"error": "분석 결과 없음"}, status=404)


# from django.http import JsonResponse
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from .models import EmotionResult
# from .serializers import EmotionResultSerializer
# from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
# from store.publisher import publish_recommendation_message
# import traceback
# from rest_framework.permissions import IsAuthenticated

# User = get_user_model()

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def save_emotion_result(request):
#     user_id = getattr(request.user, "id", None)
#     data = request.data.copy()
#     data["user"] = user_id

#     serializer = EmotionResultSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class EmotionResultView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             user_id = getattr(request.user, "id", None)
#             user = User.objects.get(id=user_id)

#             result = EmotionResult.objects.create(
#                 user=user,
#                 letter_id=request.data["letter_id"],
#                 dominant_emotion=request.data["dominant_emotion"],
#                 detailed_emotion=request.data.get("detailed_emotion"),
#                 emotion_scores=request.data.get("emotion_scores", {}),
#             )

#             publish_recommendation_message({
#                 "user": user.id,
#                 "mood": result.dominant_emotion
#             })

#             return Response({"id": result.id}, status=201)

#         except Exception as e:
#             return Response({
#                 "error": str(e),
#                 "trace": traceback.format_exc()
#             }, status=400)


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_emotion_result_api(request):
#     user_id = getattr(request.user, "id", None)
#     try:
#         results = EmotionResult.objects.filter(user_id=user_id).order_by('-analyzed_at')
#         data = [
#             {
#                 "most_frequent_mood": r.most_frequent_mood,
#                 "most_frequent_detailed_mood": r.most_frequent_detailed_mood,
#                 "emotions": r.emotions,
#                 "comfort_message": r.comfort_message,
#             }
#             for r in results
#         ]
#         return JsonResponse({"results": data})
#     except EmotionResult.DoesNotExist:
#         return JsonResponse({"error": "분석 결과 없음"}, status=404)
