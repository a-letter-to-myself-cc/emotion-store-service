FROM python:3.10-slim

# 1. 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y gcc libpq-dev

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 복사
COPY requirements.txt ./

# 4. 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스 복사
COPY . .

# 6. 기본 커맨드
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
