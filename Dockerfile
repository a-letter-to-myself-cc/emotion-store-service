# 1. 베이스 이미지 설정
FROM python:3.10-slim

# 2. 작업 디렉토리 생성
WORKDIR /app

# 3. 종속성 설치를 위한 requirements.txt 복사
COPY requirements.txt ./

# 4. pip 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 프로젝트 소스 복사
COPY . .

# 6. 환경 변수 설정 (선택)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 7. 포트 지정 (외부에서 열 포트)
EXPOSE 8009

# 8. 실행 명령 (포트는 docker-compose에서 override 가능)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8009"]
