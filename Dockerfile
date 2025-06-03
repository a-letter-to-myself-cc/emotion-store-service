# 1. Python 기반 이미지 사용
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 시스템 패키지 설치 (Django + psycopg2 설치를 위한 PostgreSQL 헤더 필요)
RUN apt-get update && apt-get install -y gcc libpq-dev

# 4. requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libpq-dev gcc


# 5. 전체 프로젝트 복사
COPY . .

# 6. 포트 설정 (Django 기본: 8000 → 이 컨테이너는 8000에서 열리고, 외부와는 8009로 매핑)
EXPOSE 8000

# 7. 실행 명령 (개발용)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
