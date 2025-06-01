# store/publisher.py

import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

def publish_recommendation_message(message: dict):
    """RabbitMQ로 추천 요청 메시지를 발행"""
    credentials = pika.PlainCredentials('myuser', 'mypassword')
    parameters = pika.ConnectionParameters(
        host='34.47.116.44',  # RabbitMQ 외부 IP
        port=5672,
        virtual_host='/',
        credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # 익스체인지 선언
    channel.exchange_declare(exchange='recommendation.direct', exchange_type='direct')

    # 메시지 발행
    try:
        channel.basic_publish(
            exchange='recommendation.direct',
            routing_key='recommend',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)  # 메시지 영속화
        )

        print(f"📤 메시지 발행 완료: {message}")
        connection.close()
    except Exception as e:
        print("❌ 메시지 발행 실패:", str(e))
        