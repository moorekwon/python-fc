# Django란 무엇인가요

## 장고란 무엇인가요?

Django(쟁고/장고)

- 파이썬으로 만들어진 무료 오픈소스 웹 애플리케이션 프레임워크(web application framework)
- 쉽고 빠르게 웹사이트를 개발할 수 있도록 돕는 구성요소로 이루어진 웹 프레임워크

- 중요한 것들을 찾을 수 있게 특정한 구조를 유지해야 함
  - 디렉토리와 파일명이 매우 중요
  - 마음대로 변경하거나 옮기면 안됨
- 모든 작업은 가상환경(virtualenv) 안에서 해야 함



## 왜 프레임워크가 필요한가요?

웹 서버

- 포트(port)를 통해 요청(request)이 도착했는지 확인하고 응답

장고

- 웹 서버가 응답할 내용을 특정 콘텐츠로 만들어줌



## 누군가가 서버에 웹 사이트를 요청하면 어떤 일이 벌어질까요?

웹 서버에 요청이 오면 장고로 전달



urlresolver

- 집배원 역할
- 웹 페이지의 주소를 가져와 무엇을 할지 확인
- 웹 사이트 주소인 URL을 통해 이해
- 패턴 목록을 가져와 URL과 맞는지 처음부터 하나씩 대조해 식별
- 일치하는 패턴이 있으면 해당 요청을 관련된 view 함수에 넘겨줌



view 함수

- 특정 정보를 데이터베이스에서 찾을 수 있음
- 수정할 수 있는 권한이 있는지 확인한 후 수정 및 답장 생성
- 장고는 view 답장을 사용자의 웹 브라우저에 보내줌



# Django 설치하기

## 가상환경(virtual environment)

virtualenv

- 프로젝트 기초 전부를 Python/Django와 분리해줌
- 웹사이트가 변경돼도 개발 중인 것에 영향을 미치지 않음



```bash
# virtualenv 생성
# myvenv: 가상환경의 이름(자신이 정함)
python3 -m venv myvenv
```

- `myvenv` 디렉토리가 만들어짐

- 우리가 사용할 가상환경(디렉토리와 파일들)이 들어있음



## 가상환경 사용하기

```bash
# 가상환경 실행
source myvenv/bin/activate
```

- 콘솔 프롬프트 앞에 (myvenv)가 붙어있으면 virtualenv가 시작됨



## 장고 설치하기

```bash
# pip가 최신 버전인지 확인
python3 -m pip install --upgrade pip
# 장고 설치
pip install django~=2.0.0
```



# Django 프로젝트

간단한 블로그 사이트 만들기



장고의 기본 골격을 만들어주는 스크립트 실행

```bash
django-admin startproject mysite .
```

- .: 현재 디렉토리에 장고를 설치하라고 스크립트에 알려줌
- django-admin.py: 스크립트로 디렉토리와 파일들을 생성



mysite

- settings.py
  - 웹사이트 설정이 있는 파일

- urls.py
  - urlresolver가 사용하는 패턴 목록을 포함

manage.py

- 사이트 관리를 도와주는 역할
- 다른 설치 작업 없이 컴퓨터에서 웹 서버를 시작할 수 있는 스크립트
- 프로젝트 디렉토리(djangogirls) 안에 있어야 함



## 설정 변경

mysite/settings.py

- 웹사이트에 정확한 현재 시간 넣기

  ```python
  # '위키피디어 타임존 리스트'에서 해당 시간대 복사
  TIME_ZONE = 'Asia/Seoul'
  ```

- 정적파일 경로 추가

  - STATIC_URL 항목 바로 아래에 STATIC_ROOT 추가

    ```python
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    ```

- ALLOWED_HOSTS 설정

  - DEBUG가 True이고 ALLOWED_HOSTS가 비어 있으면, 호스트는 `['localhost', '127.0.0.1', '[::1]'`]에 대해 유효

  - 애플리케이션을 배포할 때 PythonAnywhere의 호스트 이름과 일치하지 않으므로 설정 변경

    ```python
    ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']
    ```

  

## 데이터베이스 설정하기

데이터베이스

- 데이터의 집합 (데이터들이 모여 있는 곳)
- 사용자에 대한 정보나 블로그 글 등이 저장됨



sqlite3

- 사이트 내 데이터를 저장하기 위한 데이터베이스 소프트웨어

- 이미 mysite/settings.py 파일 안에 설치 되어있음

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
      }
  }
  ```



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



## 객체(Object)

객체 지향 프로그래밍(object oriented programming)

- 모델을 만들어 그 모델이 어떤 역할을 가지고 어떻게 행동해야 하는지 정의하여 서로 알아서 상호작용할 수 있도록 만든 개발 방법

객체(object)

- 모델은 객체

- 속성(객체 속성(properties))과 행동(메소드(methods))을 모아놓은 것



## 장고 모델

장고 안의 모델은 객체의 특별한 종류

모델을 저장하면 그 내용이 데이터베이스에 저장

데이터베이스 안의 모델은 엑셀 스프레드시트처럼 열(필드)과 행(데이터)으로 구성되어 있음



SQLite 데이터베이스

- 기본 장고 데이터베이스 어댑터



## 어플리케이션 만들기

프로젝트 내부에 별도의 애플리케이션 만들기

```bash
# blog 디렉토리 생성
python manage.py startapp blog
```



mysite

- settings.py

  - 애플리케이션을 생성한 후 장고에 사용해야 한다고 알려줘야 함

    ```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # blog 추가
        'blog'
    ]
    ```



## 블로그 글 모델 만들기

blog

- models.py

  - 모든 Model 객체를 선언하여 모델을 정의(만듦)

    ```python
    # 안에 모든 내용 삭제 후 아래 코드 추가
    # 다른 파일에 있는 것을 추가
    from django.conf import settings
    from django.db import models
    from django.utils import timezone
    
    # 모델 정의
    # class: 특별한 키워드. 객체를 정의한다는 것을 알려줌
    # Post: 모델 이름. 항상 클래스 이름의 첫 글자는 대문자
    # models: Post가 장고 모델임을 의미. 장고는 Post가 데이터베이스에 저장되어야 한다고 알게 됨
    class Post(models.Model):
        # 속성 정의
        # 다른 모델에 대한 링크
        author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        # 글자 수가 제한된 텍스트를 정의 (짧은 문자열 정보를 저장할 때 사용)
        title = models.CharField(max_length=200)
        # 글자 수에 제한이 없는 긴 텍스트를 정의
        text = models.TextField()
        # 날짜와 시간
        created_date = models.DateTimeField(default=timezone.now)
        published_date = models.DateTimeField(blank=True, null=True)
        
        # publish 메소드
        # def: 함수/메소드
        # publish: 메소드 이름
        def publish(self):
            self.published_date = timezone.now()
            self.save()
            
        # 던더(dunder): 더블-언더스코어의 준말
        # __str__ 메소드를 호출하면 Post 모델의 제목 텍스트(string)를 얻음
        def __str__(self):
            return self.title
    ```

    - 속성을 정의하기 위해 필드마다 어떤 종류의 데이터 타입을 가지는지 정해야 함
      - 데이터 타입: 텍스트, 숫자, 날짜, 다른 객체 참조 등
    - 메소드: 자주 무언가를 되돌려줌(return)



## 데이터베이스에 모델을 위한 테이블 만들기

데이터베이스에 Post 모델 추가

```bash
# 장고 모델에 변화가 생겼다는 걸 알게 해줘야 함
python manage.py makemigrations blog

# 실제 데이터베이스에 모델 추가를 반영
# 모델이 데이터베이스에 저장
python manage.py migrate blog
```



# Django 관리자

장고 관리자

- 모델링 한 글들을 장고 관리자에서 추가, 수정, 삭제할 수 있음



mysite

- settings.py
  - `LANGUAGE_CODE = 'ko'`: 관리자 화면을 한국어로 변경

blog

- admin.py

  ```python
  from django.contrib import admin
  # Post 모델을 가져옴
  from .models import Post
  
  # 관리자 페이지에서 만든 보델을 보기 위해 모델 등록
  admin.site.register(Post)
  ```



웹 서버 실행

- `python manage.py runserver`

- 브라우저를 열고 주소창에 `http://127.0.0.1:8000/admin/`을 입력하여 로그인 페이지 보기



로그인

- 모든 권한을 갖는 슈퍼 사용자(superuser)를 생성해야 함
- `python manage.py createsuperuser`을 입력하고 엔터
- 사용자 이름, 이메일 주소, 암호를 입력하고 엔터 (본인 계정 사용)
- 브라우저 장고 관리자 페이지에서 슈퍼 사용자로 로그인한 후 대시보드 확인



# 배포하기

웹 사이트 개발의 가장 중요한 부분

배포(deployment)

- 애플리케이션을 인터넷에 올려놓아 다른 사람들도 볼 수 있게 해주는 것



로컬컴퓨터

- 개발 및 테스트를 수행하는 곳

PythonAnywhere

- 인터넷 상에 서버를 제공 (웹사이트가 있는 곳)

- 비교적 배포 과정이 간단
- 방문자가 아주 많지 않은 소규모 애플리케이션을 위한 무료 서비스를 제공
- 웹

GitHub

- 코드 호스팅 서비스
- (개발 완료 후) 프로그램 복사본을 저장 (코드 사본 업데이트)



## Git 설치하기

Git

- "버전 관리 시스템(version control system)"
- 시간 경과에 따른 파일 변경을 추적할 수 있어, 나중에라도 특정 버전을 다시 불러올 수 있음
- Microsoft Word의 "변경 사항 추적" 기능과 비슷하나 훨씬 강력

```bash
# Git 설치
sudo apt install git
```



[DjangoGirls/ 배포하기!]([https://tutorial.djangogirls.org/ko/deploy/#git-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0](https://tutorial.djangogirls.org/ko/deploy/#git-설치하기))

### Git 저장소 만들기



### GitHub에 코드 배포하기



## PythonAnywhere에 블로그 설정하기

### GitHub에서 PythonAnywhere로 코드 가져오기

### PythonAnywhere에서 가상환경(virtualenv) 생성하기

### PythonAnywhere에서 데이터베이스 생성하기



## web app으로 블로그 배포하기

### 가상환경(virtualenv) 설정하기

### WSGI 파일 설정하기



## 디버깅 팁



# Django urls

## URL이란 무엇인가요?

URL

- 웹 주소
- 웹 사이트를 방문할 때마다 브라우저의 주소창에 URL을 볼 수 있음
- 인터넷의 모든 페이지는 고유한 URL을 가지고 있어야 함
- 애플리케이션은 사용자가 URL을 입력하면 어떤 내용을 보여줘야 하는지 알고 있음
- 장고는 `URLconf(URL configuration)`을 사용
  - 장고에서 URL과 일치하는 뷰를 찾기 위한 패턴들의 집합



## 장고 URL은 어떻게 작동할까요?

mysite

- urls.py

  ```python
  # 독스트링(docstring)
  # 파일 제일 첫 부분, 클래스 또는 메소드 윗 부분에 작성해 어떤 일을 수행하는지 알려줌
  """mysite URL Configuration
  
  [...]
  """
  from django.contrib import admin
  from django.urls import path
  
  urlpatterns = [
      # 관리자 URL
      # 장고는 admin/로 시작하는 모든 URL을 view와 대조해 찾아냄
      # 무수히 많은 URL이 admin URL에 포함될 수 있어 일일이 모두 쓰지 않고, 정규표현식을 사용
      path('admin/', admin.site.urls)
  ]
  ```



## Django url

mysite

- urls.py

  - blog 애플리케이션에서 url들을 가져옴

  ```python
  from django.contrib import admin
  # blog.urls를 가져오는 행 추가
  # blog.urls를 가져오기 위해 include 함수 추가
  from django.urls import path, include
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      # 장고는 http://127.0.0.1:8000/로 들어오는 모든 접속 요청을 blog.urls로 전송해 추가 명령을 찾음
      path('', include('blog.urls'))
  ]
  ```



## blog.urls

blog

- urls.py (파일 생성)

  ```python
  # 장고 함수인 path를 가져옴
  from django.urls import path
  # blog 애플리케이션에서 사용할 모든 views를 가져옴
  from . import views
  ```

  ```python
  # URL 패턴 추가
  urlpatterns = [
      # 빈 문자열에 매칭이 됨
      # 장고 URL 확인자(resolver)는 전체 URL 경로에서 접두어(prefix)에 포함되는 도메인 이름(i.e. http://127.0.0.1:8000/)을 무시하고 받아들임
      path('', views.post_list, name='post_list')
  ]
  ```

  - `post_list`라는 `view`가 루트 URL에 할당됨
  - 장고에게 누군가 웹사이트에 'http://127.0.0.1:8000/' 주소로 들어왔을 때 `views.post_list`를 보여주라고 말해줌
  - `name='post_list'`
    - URL에 이름을 붙인 것
    - 뷰를 식별 (뷰의 이름과 같을 수도 다를 수도 있음)



# Django 뷰 만들기

버그 잡기



뷰(view)

- 애플리케이션의 "로직"을 넣는 곳
- 만들었던 모델에서 필요한 정보를 받아와 템플릿에 전달하는 역할
- 어려워 보이지만, 파이썬 함수일 뿐
- views.py 파일 안에 있음



## blog/views.py

blog

- views.py

  ```python
  from django.shortcuts import render
  
  # view 만들기
  def post_list(request):
      # 요청(request)을 넘겨받아 render 메소드를 호출
      # 메소드를 호출하여 받은(return) blog/post_list.html 템플릿을 보여줌
      return render(request, 'blog/post_list.html', {})
  ```

  - TemplateDoesNotExist 에러 발생
    - 버그를 해결하기 위해 템플릿 파일(post_list.html)을 만듦



# HTML 시작하기

템플릿

- 서로 다른 정보를 일정한 형태로 표시하기 위해 재사용 가능한 파일
- 장고 템플릿 양식은 HTML을 사용



## HTML 이란 무엇일까요?

HTML

- "HyperText Markup Language"의 줄임말
  - HyperText: 페이지 간 하이퍼링크가 포함된 텍스트
  - Markup: 브라우저가 문서를 해석하도록 표시(mark)

- 웹 브라우저가 해석할 수 있는 코드
- 사용자에게 웹 페이지를 표시할 때 사용
- 태그(tag)들로 이루어져 있음
  - 마크업 요소(elements): <(여는 태그)로 시작, >(닫는 태그)로 끝남



## 템플릿

템플릿 파일을 만듦

템플릿 파일에 모든 내용이 저장될 것임

blog/templates/blog 디렉토리에 저장

- blog 디렉토리를 하나 더 만드는 것은 나중에 폴더 구조가 복잡해 질 때 좀 더 쉽게 찾기 위해 사용하는 관습적인 방법



blog

- templates

  - blog

    - post_list.html (파일 생성)

      ```html
      <!-- 내용 생성 -->
      <html>
          <p>Hi there!</p>
          <p>It works!</p>
      </html>
      ```



[DjangoGirls/ HTML 시작하기](https://tutorial.djangogirls.org/ko/html/)

### Head & body



## 맞춤형 템플릿 만들기



## 하나 더: 배포하기

### GitHub에 코드를 커밋, 푸시

### PythonAnywhere에서 새 코드를 가져와, 웹 앱을 다시 불러옵니다.



# Django ORM(Querysets)

장고를 데이터베이스에 연결하고 데이터 저장하기



## 쿼리셋이란 무엇인가요?

전달받은 모델의 객체 목록

데이터베이스로부터 데이터를 읽고, 필터를 걸거나 정렬을 할 수 있음



## 장고 쉘(shell)

```bash
python manage.py shell
# (InteractiveConsole)
# >>>
```

- 장고 인터랙티브 콘솔(interactive console)로 들어옴
- 장고만의 마법을 부릴 수 있는 곳 (파이썬의 모든 명령어 사용 가능)



### 모든 객체 조회하기

```bash
# Post 모델을 blog.models에서 불러옴
>>> from blog.models import Post

# 입력했던 모든 글들을 출력
>>> Post.objects.all()
```



### 객체 생성하기

파이썬으로 새 글 포스팅하기

```bash
# User 모델을 불러옴
>>> from django.contrib.auth.models import User

# 데이터베이스에서 user 확인
>>> User.objects.all()
# <QuerySet [<User: ola>]> -> 슈퍼유저로 등록했었던 사용자

# 사용자이름이 'ola'인 User 인스턴스 가져오기
>>> me = User.objects.get(username='ola')

# 데이터베이스에 새 글 객체 저장
Post.objects.create(author=me, title='Sample title', text='Test')

# 제대로 작동했는지 확인
>>> Post.objects.all()
# <QuerySet [<Post: my post title>, <Post: another post title>, <Post: Sample title>]>
```



### 필터링하기

데이터를 필터링

- 쿼리셋의 중요한 기능
- `fileter` 사용

```bash
# 괄호 안에 원하는 조건(작성자가 나인 조건)을 넣어줌
>>> Post.objects.filter(author=me)

# 모든 글들 중 제목(title)에 'title' 글자가 들어간 글들만 뽑아냄
# 필드 이름("title")과 연산자과 필터("contains")를 __로 구분
>>> Post.objects.filter(title__contains='title')

# 게시일(published_date)로 과거에 작성한 글 필터링
>>> from django.utils import timezone
>>> Post.objects.filter(published_date__lte=timezone.now())
# []

# 파이썬 콘솔에서 추가한 게시물이 보이지 않으므로, 먼저 게시하려는 게시물의 인스턴스를 얻음
>>> post = Post.objects.get(title="Sample title")

# publish 메소드를 사용해 게시
>>> post.publish()

# 다시 게시된 글의 목록 가져옴
>>> Post.objects.filter(published_date__lte=timezone.now())
# [<Post: Sample title>]
```



### 정렬하기

쿼리셋은 객체 목록을 정렬할 수 있음

```bash
# created_date 필드를 정렬
>>> Post.objects.order_by('created_date')

# 내림차순 정렬 (-)
>>> Post.objects.order_by('-craeted_date')
```



### 쿼리셋 연결하기

쿼리셋들을 함께 연결(chaining)

```bash
>>> Post.objects.filter(published_Date__lte=timezone.now()).order_by('published_date')
```



쉘 종료

```bash
>>> exit()
```



# 템플릿 동적 데이터

Post 모델은 models.py 파일에, post_list 모델은 views.py 파일에 있음 (각각 다른 장소에 나눠져있음)

데이터베이스 안에 저장되어 있는 모델(콘텐츠)을 가져와 템플릿에 넣어 보여주기



뷰(view)

- 모델과 템플릿을 연결하는 역할
- post_list를 뷰에서 보여주고 이를 템플릿에 전달하기 위해 모델을 가져와야 함
- 일반적으로 뷰가 템플릿에서 모델을 선택하도록 만들어야 함



blog

- views.py

  ```python
  from django.shortcuts import render
  # models.py 파일에 정의된 모델 가져옴
  # .은 현재 디렉토리 또는 애플리케이션을 의미
  from .models import Post
  
  # post_list 뷰 내용
  def post_list(request):
      return render(request, 'blog/post_list.html', {})
  ```

- models.py



## 쿼리셋(QuerySet)

Post 모델에서 글을 가져오기 위해 쿼리셋(QuerySet)이 필요



blog

- views.py

  ```python
  # 게시일 published_date 기준으로 정렬
  Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
  ```

  ```python
  from django.shortcuts import render
  # timezone 모듈을 불러오기 위해 추가
  from django.utils import timezone
  from .models import Post
  
  def post_list(request):
      # posts 변수를 만듦
      # 이 변수는 쿼리셋의 이름
      posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
      # posts 쿼리셋을 템플릿에 보냄
      return render(request, 'blog/post_list.html', {'posts': posts})
  ```

  - render 함수
    - `request`: 매개변수(사용자가 요청하는 모든 것)
    - `'blog/post_list.html'`: 템플릿
    - `{'posts': posts}`: {} 안에 템플릿을 사용하기 위한 매개변수를 추가



# Django 템플릿

장고는 데이터를 보여주기 위해 내장된 템플릿 태그(template tags) 기능을 제공



## 템플릿 태그는 무엇인가요?

브라우저는 파이썬 코드를 이해할 수 없기 때문에 HTML에 파이썬 코드를 바로 넣을 수 없음



템플릿 태그

- 파이썬을 HTML로 바꿔줌
- 동적인 웹 사이트를 만들 수 있게 함



## post 목록 템플릿 보여주기

blog

- templates

  - blog

    - post_list.html (템플릿)

      ```html
      <!-- 템플릿에 넘겨진 posts 변수를 받아 HTML에 나타나도록 함 -->
      {{ posts }}
      ```

      - 변수 이름 안에 중괄호를 넣어 표시
      - 장고 템플릿 안에 있는 값을 출력

      ```html
      <!-- for loop를 이용해 목록을 보여줌 -->
      {% for post in posts %}
      	{{ post }}
      {% endfor %}
      ```

      ```html
      <!-- HTML과 템플릿 태그를 섞어 사용 -->
      <div>
          <h1><a href="/">Django Girls Blog</a></h1>
      </div>
      
      <!-- 목록의 모든 객체를 반복함 -->
      {% for post in posts %}
      	<div>
              <!-- Post 모델에서 정의한 각 필드의 데이터에 접근하기 위한 표기법 -->
              <p>published: {{ post.published_date }}</p>
              <h1><a href="">{{ post.title }}</a></h1>
              <!-- |linebreaksbr: 글 텍스트에서 행이 바뀌면 문단으로 변환 -->
              <p>{{ post.text|linebreaksbr }}</p>
      	</div>
      {% endfor %}
      ```



[DjangoGirls/ Django 템플릿](https://tutorial.djangogirls.org/ko/django_templates/)

## 한 가지 더



[DjangoGirls/ CSS - 예쁘게 만들기](https://tutorial.djangogirls.org/ko/css/)

# CSS - 예쁘게 만들기





# 템플릿 확장하기

# 애플리케이션 확장하기

# Django 폼