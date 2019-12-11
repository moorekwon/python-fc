# Django란 무엇인가요

## 장고란 무엇인가요?

[DjangoGirls](https://tutorial.djangogirls.org/ko/django/)

장고

- 중요한 것들을 찾을 수 있게 특정한 구조를 유지해야 함
  - 디렉토리와 파일명이 매우 중요
  - 마음대로 변경하거나 옮기면 안됨
- 모든 작업은 가상환경(virtualenv) 안에서 해야 함



## 왜 프레임워크가 필요한가요?

## 누군가가 서버에 웹 사이트를 요청하면 어떤 일이 벌어질까요?

웹 서버에 요청이 오면 장고로 전달

urlresolver

- 집배원 역할

- 웹 페이지의 주소를 가져와 무엇을 할지 확인

- 웹 사이트 주소인 URL을 통해 이해
- 패턴 목록을 가져와 URL과 맞는지 처음부터 하나씩 대조해 식별
- 일치하는 패턴이 있으면 해당 요청을 관련된 함수 view에 넘겨줌
  - 특정 정보를 데이터베이스에서 찾을 수 있음
  - 수정할 수 있는 권한이 있는지 확인한 후 답장 생성
  - 장고는 view 답장을 사용자의 웹 브라우저에 보내줌



# Django 설치하기

## 가상환경(virtual environment)

virtualenv

- 프로젝트 기초 전부를 Python/Django와 분리해줌 (웹사이트가 변경돼도 개발 중인 것에 영향을 미치지 않음)

```bash
# myvenv: 가상환경의 이름(자신이 정함)
python3 -m venv myvenv
```



## 가상환경 사용하기

```bash
# 가상환경 실행
source myvenv/bin/activate
```



## 장고 설치하기

```bash
# pip가 최신 버전인지 확인
python3 -m pip install --upgrade pip
# 장고 설치
pip install django~=2.0.0
```



# Django 프로젝트

장고의 기본 골격을 만들어주는 스크립트 실행

```bash
# .: 현재 디렉토리에 장고를 설치하라고 스크립트에 알려줌
# django-admin.py: 스크립트로 디렉토리와 파일들을 생성
django-admin startproject mysite .
```



manage.py

- 사이트 관리를 도와주는 역할
- 다른 설치 작업 없이 컴퓨터에서 웹 서버를 시작할 수 있는 스크립트
- 프로젝트 디렉토리(djangogirls) 안에 있어야 함

mysite

- settings.py
  - 웹사이트 설정이 있는 파일

- urls.py
  - urlresolver가 사용하는 패턴 목록을 포함



## 설정 변경

mysite/settings.py

- 정적파일 경로 추가

  - STATIC_URL 항목 바로 아래에 STATIC_ROOT 추가

    ```python
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    ```



## 데이터베이스 설정하기

데이터베이스

- 데이터의 집합 (데이터들이 모여 있는 곳)
- 사용자에 대한 정보나 블로그 글 등이 저장됨



sqlite3

- 사이트 내 데이터를 저장하기 위한 데이터베이스 소프트웨어



```bash
# 블로그에 데이터베이스를 생성
python manage.py migrate
# 웹 서버 시작
python manage.py runserver
```



사용하는 브라우저를 열어서 주소 입력

- `http://127.0.0.1:8000/`

- 웹 사이트가 모두 잘 작동하는지 확인



# Django 모델

블로그 내 모든 포스트를 저장하는 부분 만들기



[DjangoGirls/ Django 모델](https://tutorial.djangogirls.org/ko/django_models/)

## 객체(Object)



## 장고 모델

장고 안의 모델은 객체의 특별한 종류

모델을 저장하면 그 내용이 데이터베이스에 저장

데이터베이스 안의 모델은 엑셀 스프레드시트처럼 열(필드)과 행(데이터)으로 구성되어 있음



SQLite 데이터베이스

- 기본 장고 데이터베이스 어댑터



## 어플리케이션 만들기

## 블로그 글 모델 만들기

## 데이터베이스에 모델을 위한 테이블 만들기



# Django 관리자

# 배포하기

# Django urls

# Django 뷰 만들기

# HTML 시작하기

# Django ORM(Querysets)

# 템플릿 동적 데이터

# Django 템플릿

# CSS - 예쁘게 만들기

# 템플릿 확장하기

# 애플리케이션 확장하기

# Django 폼