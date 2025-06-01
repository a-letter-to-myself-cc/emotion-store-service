import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class RemoteJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            response = requests.post(
                "http://accounts:8000/accounts/internal/verify/",  # 도커 환경이라면 accounts는 서비스명
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise AuthenticationFailed("유효하지 않은 토큰입니다.")

            user_data = response.json()
            return (user_data, None)

        except requests.exceptions.RequestException:
            raise AuthenticationFailed("인증 서버와의 연결 실패")
