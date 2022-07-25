## Intro

> **원티드X프리온보딩 4주차 개인과제 레포지토리(repository)입니다.**

<br>

본 과제에서 요구하는 서비스는 SNS(Social Networking Service)입니다.<br>
사용자는 SNS 서비스에 접속하여, 게시글을 업로드하고 관리(수정/삭제/복구)할 수 있습니다. 또한 다른 사람의 게시글을 확인하고, 좋아요를 누를 수 있습니다.

<br>

> **목차**

- [Environments](#environments)
- [Project](#project)
- [Etc](#etc)

<br>


<br>
<hr>

## Environments

<br>
<div align="center">
<img src="https://img.shields.io/badge/Python-blue?style=plastic&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/Django-092E20?style=plastic&logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django Rest Framework-EE350F?style=plastic&logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-00979D?style=plastic&logo=MySQL&logoColor=white"/>
</div>

<br>
<div align="center">
<img src="https://img.shields.io/badge/AWS EC2-FF9900?style=plastic&logo=Amazon AWS&logoColor=white"/>
<img src="https://img.shields.io/badge/AWS RDS-527FFF?style=plastic&logo=Amazon RDS&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-%230db7ed.svg?style=plastic&logo=Docker&logoColor=white"/>
<img src="https://img.shields.io/badge/nginx-%23009639.svg?style=plastic&logo=NGINX&logoColor=white"/>
<img src="https://img.shields.io/badge/gunicorn-EF2D5E?style=plastic&logo=Gunicorn&logoColor=white"/>
<img src="https://img.shields.io/badge/Swagger-%23Clojure?style=plastic&logo=swagger&logoColor=white"/>
</div>

<br>
<hr>

## Project

> **Period**
- #### ⚡️ 22.07.19 ~ 22.07.25

<br>

> **Analysis**
- #### 📌 필수 구현사항
  - 유저관리: 
    - 유저 회원가입: 이메일을 ID로 사용합니다.
    - 유저 로그인 및 인증: 로그인 성공 시 JWT토큰을 발급받으며, 추후 사용자 인증으로 사용합니다.
  - 게시글:
    - 게시글 생성
      - 제목, 내용, 해시태그 등을 입력하여 게시글을 생성합니다.
      - 제목, 내용, 해시태그는 필수사항입니다.
      - 작성자 정보는 request body에 존재하지 않고 해당 API를 요청한 인증정보에서 추출하여 사용합니다.
      - 참고로 해시태그는 #으로 시작합니다. (해시태그 입력 형태는 자유롭게 설정가능)
    - 게시글 목록
      - 모든 사용자(인증/인가에 통과한 유저)는 모든 게시글에 보기 권한이 있습니다.
      - 게시글 목록에는 제목, 작성자, 해시태그, 작성일, 좋아요 수, 조회수 등이 포함됩니다.
      - 검색/정렬/필터링/페이지 기능은 각각 동작할 뿐만 아니라, 동시에 적용될 수 있어야 합니다.
        <br><br>
        ```
        ex) some-url?search=..&order_by=.. (이는 예시이며, 해당변수는 직접 설정할 것)
        
        * Ordering(Sorting, 정렬)
          사용자는 게시글 목록을 원하는 값으로 정렬할 수 있습니다.
          단, 오름차순/내림차순을 모두 선택할 수 있습니다.
          
          ex) default: 생성일 //생성일, 좋아요 수, 조회수 중 1개만 선택가능
          
        * Searching(검색)

          사용자는 입력한 키워드로 해당 키워드를 포함한 게시글을 조회할 수 있습니다.
          
          ex1) some-url?search=후기 >> "후기"가 제목에 포함된 게시글 목록
          ex2) "후기" 검색 시 >> 00 방문후기 입니다. (검색 됨)
        
        * Filtering(필터링)
          
          사용자는 지정한 키워드로 해당 키워드를 포함한 게시글을 필터링할 수 있습니다.

          ex1) some-url?hastags=서울 >> “서울" 해시태그를 가진 게시글 목록.
          ex2) some-url?hastags=서울,맛집 >> “서울" 과 “맛집” 해시태그를 모두 가진 게시글 목록. 
          
        * Pagination(페이지 기능)

          사용자는 1 페이지 당 게시글 수를 조정할 수 있습니다.
          단, default 설정은 10개의 게시글로 합니다.
          
          ex) some-url?offset=0&limit=10 >> 0번 인덱스 게시글부터 10개의 게시글을 가져옵니다.
        
        ```
    - 게시글 상세
      - 모든 사용자는 모든 게시글에 보기권한이 있습니다.
      - 작성자를 포함한 사용자는 본 게시글에 좋아요를 누를 수 있습니다.
      - 좋아요를 누른 게시글에 다시 좋아요를 누르면, 좋아요는 취소됩니다.
      - 작성자를 포함한 특정 사용자가 게시글을 상세보기 하면 조회수 1이 증가합니다. (횟수 제한 없음)
    - 게시글 수정
      - 게시글은 작성자만 수정할 수 있습니다.
    - 게시글 삭제
      - 게시글은 작성자만 삭제할 수 있습니다.
      
- #### 📌 선택 구현사항     
  - 댓글 기능
  - 싫어요/공감 기능
  - 조회수가 1인당 1번만 오르도록 제한
  - 유저 로그아웃 기능
 
- #### 📌 참고사항
  - 본 요구사항에 명시되지 않은 내용은 모두 자유롭게 구상하여 진행해주세요.
  - 필수 구현사항에 따라 진행하되, 개인별 완료 가능한 목표만큼 진행해보세요.
 
<br>

> **Development**
- #### 🔥 프로젝트 구현기능
  ```
  - 유저관리:
    > 회원가입: 유저 회원가입 기능입니다. 
      * 이메일, 닉네임, 패스워드는 필수값입니다.
      * 전화번호, 프로필 이미지는 선택값입니다.
      * 이메일, 닉네임, 패스워드는 필수값입니다.
      * 이메일, 닉네임, 패스워드는 필수값입니다.
      * 이메일, 닉네임, 패스워드는 필수값입니다.
      * 이메일, 닉네임은 중복되지 않습니다.
      * 패스워드는 반드시 8~20자리의 최소 1개의 소문자, 대문자, 숫자, (숫자키)특수문자로 구성됩니다.
      * 패스워드는 해싱 후 DB에 저장됩니다.
      
    > 로그인: 유저 로그인 기능입니다. (DRF-SimpleJwt 활용)
      * 이메일, 패스워드는 필수값입니다.
      * 입력받은 이메일과 패스워드가 유저 정보와 일치하는지 확인합니다.
      * 모든 유효성 검사에 통과하면 액세스토큰과 리프레시 토큰을 발급합니다.
      
    > 로그아웃
      * 추후 구현예정
      
    > 토큰 재발급
      * 추후 구현예정
  
  - 게시글:
    > 게시글 목록: 인증/인가에 통과한 유저는 모든 게시글의 리스트 정보를 조회할 수 있습니다.
      # 부가기능:
        * 키워드 검색기능(게시글 제목/내용/태그에 해당 키워드가 검색조건으로 사용)
        * 해시태그 검색기능(다수의 해시태그를 검색조건으로 사용 가능)
        * 정렬기능(게시글 생성일자/좋아요 수/조회수를 기준으로 오름차순, 내림차순 정렬)
        * 필터링 기능(현재 게시중인 게시글/삭제된 게시글)
        * 페이지네이션 기능(사용자가 원하는 게시글 개수를 지정할 수 있음 >> default: 10개)
    
    > 게시글 상세: 인증/인가에 통과한 유저는 모든 게시글의 상세 정보를 조회할 수 있습니다.
      # 부가기능:
        * 특정 유저가 게시글을 상세 조회하면 조회수 1이 증가합니다.
        * 단, 조회수는 ip당 1회만 증가하도록 제한됩니다.
        * 여기서 클라이언트의 요청이 reverse proxy 서버를 거쳐서 오더라도 클라이언트의 실제 ip를 추출합니다.
        * 해당 게시글이 존재하는지 확인합니다.
    
    > 게시글 생성: 인증/인가에 통과한 유저는 게시글을 생성(업로드)할 수 있습니다.
     * 게시글과 여러개의 해시태그를 함께 생성할 수 있습니다.
     
    > 게시글 수정: 인증/인가에 통과한 유저는 본인의 게시글을 수정할 수 있습니다.
      * 해당 게시글이 존재하는지, 본인의 게시글인지를 확인합니다.
      * 게시글의 제목/내용/태그만 수정할 수 있습니다.
      * 게시글 수정 시, 다수의 태그를 수정할 수 있습니다.
    
    > 게시글 삭제: 인증/인가에 통과한 유저는 본인의 게시글을 삭제할 수 있습니다.
      * 해당 게시글이 존재하는지, 본인의 게시글인지를 확인합니다.
      * 이미 삭제된 게시글은 다시 삭제할 수 없습니다.
      
    > 게시글 복구: 인증/인가에 통과한 유저는 본인의 게시글을 복구할 수 있습니다.
      * 해당 게시글이 존재하는지, 본인의 게시글인지를 확인합니다.
      * 이미 복구된 게시글은 다시 복구할 수 없습니다.
      
    > 게시글 좋아요: 인증/인가에 통과한 유저는 모든 게시글에 좋아요를 누르거나 취소할 수 있습니다.
      * 해당 게시글이 존재하는지 확인합니다.
  ```

<br>

> **Modeling**
- #### 🚀 ERD 구조
  <img width="1000px" height="550px" alt="스크린샷 2022-07-25 08 53 14" src="https://user-images.githubusercontent.com/89829943/180696903-a4715663-3bcd-41b6-89cf-9f2dcc34966d.png">

<br> 

> **API Docs**
- #### 🌈 API 명세서
  |ID|Feature|Method|URL|Description|
  |---|-----|----|----|----|
  |1|유저 회원가입|POST|api/users/signup|유저 회원가입 기능입니다.|
  |2|유저 로그인|POST|api/users/signin|유저 로그인 기능입니다.|
  |3|게시글 생성|POST|api/posts|본인의 게시글을 생성합니다.|
  |4|게시글 리스트|GET|api/posts|모든 게시글 리스트 정보를 조회합니다.|
  |5|게시글 상세|GET|api/posts/\<int:post_id\>|모든 게시글 상세 정보를 조회합니다.|
  |6|게시글 수정|PATCH|api/posts/\<int:post_id\>|본인의 게시글을 수정합니다.|
  |7|게시글 삭제|DELETE|api/posts/\<int:post_id\>|본인의 게시글을 삭제합니다.|
  |8|게시글 복구|PATCH|api/posts/\<int:post_id\>/restore|본인의 게시글을 복구합니다.|
  |9|게시글 좋아요(생성/취소)|POST|api/posts/\<int:post_id\>/like|본인 게시글 포함, 모든 게시글의 좋아요 기능을 사용합니다.|
  
- #### ✨ Swagger UI
  #### ```✔️ 유저 회원가입``` 
  <img width="1000px" alt="스크린샷 2022-07-25 14 06 34" src="https://user-images.githubusercontent.com/89829943/180702579-5f394884-a7a6-4db7-9658-fe32022c9ced.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 07 09" src="https://user-images.githubusercontent.com/89829943/180702609-1b2c200c-0f8b-467e-ae44-a3af311a2640.png">
  
  #### ```✔️ 유저 로그인```
  <img width="1000px" alt="스크린샷 2022-07-25 14 14 37" src="https://user-images.githubusercontent.com/89829943/180703475-55f6b39e-1d12-4a0d-bfc8-83182b418fb9.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 15 16" src="https://user-images.githubusercontent.com/89829943/180703483-651ff118-7495-467d-b205-eadc8db1ad9d.png">
  
  #### ```✔️ 게시글 생성```
  <img width="1000px" alt="스크린샷 2022-07-25 14 19 09" src="https://user-images.githubusercontent.com/89829943/180703881-f7836fb0-edc6-4e39-a34b-5f63487df411.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 19 34" src="https://user-images.githubusercontent.com/89829943/180703903-9c6a98b3-7e60-49f2-b072-3157285403f1.png">
  
  #### ```✔️ 게시글 리스트```
  <img width="1000px" height="500px" alt="스크린샷 2022-07-25 14 23 14" src="https://user-images.githubusercontent.com/89829943/180704506-2666460f-9303-437f-a097-57c1d0c4d5ac.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 24 07" src="https://user-images.githubusercontent.com/89829943/180704527-8a644faa-6240-4007-b77e-c19559d0c0b9.png">
  
  #### ```✔️ 게시글 상세```
  <img width="1000px" alt="스크린샷 2022-07-25 14 29 31" src="https://user-images.githubusercontent.com/89829943/180704936-a1bd6f7e-334c-4406-bee6-5351e3d7401d.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 29 51" src="https://user-images.githubusercontent.com/89829943/180704952-a4015272-ebfb-44c7-9b40-3691fce2e3e4.png">
  
  #### ```✔️ 게시글 수정```
  <img width="1000px" alt="스크린샷 2022-07-25 14 35 05" src="https://user-images.githubusercontent.com/89829943/180705721-ee0dad11-9766-4f89-8c86-dc490501d399.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 38 21" src="https://user-images.githubusercontent.com/89829943/180705749-6c7b698d-5e85-4e2e-875f-2d6810888b70.png">

  #### ```✔️ 게시글 삭제```
  <img width="1000px" alt="스크린샷 2022-07-25 14 41 00" src="https://user-images.githubusercontent.com/89829943/180706062-927f16bc-a39c-47e8-bcb8-1bb8bf02fd4f.png">
  <img width="1000" alt="스크린샷 2022-07-25 14 41 16" src="https://user-images.githubusercontent.com/89829943/180706079-da15b387-3e39-4fb3-b4a7-fe680a0b947a.png">

  #### ```✔️ 게시글 복구```
  <img width="1000px" alt="스크린샷 2022-07-25 14 43 04" src="https://user-images.githubusercontent.com/89829943/180706335-55c841bb-1f46-4f6d-a76c-0271a89f8499.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 43 19" src="https://user-images.githubusercontent.com/89829943/180706359-821c846a-0be1-4843-9ccd-bc2f67d3d4bf.png">

  #### ```✔️ 게시글 좋아요```
  <img width="1000px" alt="스크린샷 2022-07-25 14 45 39" src="https://user-images.githubusercontent.com/89829943/180706665-af18609d-e02f-4b42-81c7-265160689360.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 45 55" src="https://user-images.githubusercontent.com/89829943/180706681-de52c19c-df98-4d68-b220-5cbf11d43c74.png">
  <img width="1000px" alt="스크린샷 2022-07-25 14 46 09" src="https://user-images.githubusercontent.com/89829943/180706695-fb6b4b03-cfbd-4499-9699-f61421e266d6.png">

<br> 

> **Deploy**
- #### 🏖 프로젝트 배포
  #### Docker, Nginx, Gunicorn을 사용하여 AWS EC2 서버에 배포하였습니다.

<br> 

> **Test**
- #### 🚦 테스트코드 작성
  #### 총 테스트코드: 59 case
  
  |ID|Feature|Method|Success cases|Fail cases|
  |---|----|----|----|----|
  |1|유저 회원가입|POST|1 case|14 case|
  |2|유저 로그인|POST|1 case|4 case|
  |3|게시글 생성|POST|1 case|4 case|
  |4|게시글 리스트|GET|12 case|1 case|
  |5|게시글 상세|GET|1 case|2 case|
  |6|게시글 수정|PATCH|1 case|3 case|
  |7|게시글 삭제|DELETE|1 case|4 case|
  |8|게시글 복구|PATCH|1 case|4 case|
  |9|게시글 좋아요(생성/취소)|POST|2 case|2 case|
  <img width="1000px" alt="스크린샷 2022-07-25 15 17 55" src="https://user-images.githubusercontent.com/89829943/180710823-fbafab97-6779-40e2-a227-778a848afbca.png">
  <img width="1000px" alt="스크린샷 2022-07-25 15 16 29" src="https://user-images.githubusercontent.com/89829943/180710671-915389ab-6f83-4bc5-ab69-27e4e697bac6.png">

<br>
<hr>

## Etc

> **Guides**
- #### ⚙️ 프로젝트 설치방법
  #### ```✔️ 로컬 개발 및 테스트용```
  
  1. 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
  ```
  git clone https://github.com/F5-Refresh/donggyu-sns.git
  cd project directory
  ```
  
  2. 가상환경을 만들고, 프로젝트에 필요한 python package를 다운받습니다.
  <br>
  
  ```
  conda create --name project-name python=3.9
  conda activate project-name
  pip install -r requirements.txt
  ```
  
  3. manage.py 파일과 동일한 위치에서 환경설정 파일을 만듭니다.
  <br>
  
  ```
  ex) .env file 
  
  ## general ##
  DEBUG         = True
  ALLOWED_HOSTS = ALLOWED_HOSTS
  SECRET_KEY    = SECRET_KEY

  ## Docker DB ##
  MYSQL_TCP_PORT      = '3306'
  MYSQL_DATABASE      = MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD = MYSQL_ROOT_PASSWORD
  MYSQL_USER          = MYSQL_USER
  MYSQL_PASSWORD      = MYSQL_PASSWORD

  ## AWS RDS ##
  RDS_HOSTNAME = RDS_HOSTNAME
  RDS_DB_NAME  = RDS_DB_NAME
  RDS_USERNAME = RDS_USERNAME
  RDS_PASSWORD = RDS_PASSWORD
  RDS_PORT     = '3306'
  ```
  
  4. project-name/settings.py에서 DB설정을 적절하게 변경합니다.
  <br>
  
  ```
  Docker로 DB를 구축하는 경우 or AWS RDS로 DB를 구축하는 경우 등
  다양한 방법으로 DB를 구축하는 경우에 맞게 DB 설정을 변경합니다.
  
  '''
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('MYSQL_DATABASE'),
          'USER'    : 'root',
          'PASSWORD': get_env_variable('MYSQL_ROOT_PASSWORD'),
          'HOST'    : 'localhost',
          'PORT'    : get_env_variable('MYSQL_TCP_PORT'),
      }
  }
  '''

  ## AWS RDS ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('RDS_DB_NAME'),
          'USER'    : get_env_variable('RDS_USERNAME'),
          'PASSWORD': get_env_variable('RDS_PASSWORD'),
          'HOST'    : get_env_variable('RDS_HOSTNAME'),
          'PORT'    : get_env_variable('RDS_PORT'),
          'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
  }
  ```
  
  5. DB의 Table 구조를 최신 modeling에 맞게 설정합니다.
  <br>
  
  ```
  python manage.py migrate
  ```
  
  6. 개발용 서버를 실행합니다.
  <br>
  
  ```
  python manage.py runserver 0:8000
  ```

  #### ```✔️ 배포용```
  1. 배포용 서버에서 해당 프로젝트를 clone하고, 프로젝트 폴더로 이동합니다.
  <br>
  
  ```
  git clone https://github.com/F5-Refresh/donggyu-sns.git
  cd project directory
  ```
  
  2. manage.py 파일과 동일한 위치에서 도커 환경설정 파일을 만듭니다.
  <br>
  
  ```
  ex) .env file 
  
  ## general ##
  DEBUG         = True
  ALLOWED_HOSTS = ALLOWED_HOSTS
  SECRET_KEY    = SECRET_KEY

  ## Docker DB ##
  MYSQL_TCP_PORT      = '3306'
  MYSQL_DATABASE      = MYSQL_DATABASE
  MYSQL_ROOT_PASSWORD = MYSQL_ROOT_PASSWORD
  MYSQL_USER          = MYSQL_USER
  MYSQL_PASSWORD      = MYSQL_PASSWORD

  ## AWS RDS ##
  RDS_HOSTNAME = RDS_HOSTNAME
  RDS_DB_NAME  = RDS_DB_NAME
  RDS_USERNAME = RDS_USERNAME
  RDS_PASSWORD = RDS_PASSWORD
  RDS_PORT     = '3306'
  ```
  
  3. project-name/settings.py에서 DB설정을 적절하게 변경합니다.
  <br>
  
  ```
  Docker로 DB를 구축하는 경우 or AWS RDS로 DB를 구축하는 경우 등
  다양한 방법으로 DB를 구축하는 경우에 맞게 DB 설정을 변경합니다.
  
  '''
  DATABASES = {
      'default': {
          'ENGINE'  : 'django.db.backends.mysql',
          'NAME'    : get_env_variable('MYSQL_DATABASE'),
          'USER'    : 'root',
          'PASSWORD': get_env_variable('MYSQL_ROOT_PASSWORD'),
          'HOST'    : 'db',
          'PORT'    : get_env_variable('MYSQL_TCP_PORT'),
      }
  }
  '''

  ## AWS RDS ##
  DATABASES = {
      'default': {
          'ENGINE'  : 'django..backends.mysql',
          'NAME'    : get_env_variable('RDS_DB_NAME'),
          'USER'    : get_env_variable('RDS_USERNAME'),
          'PASSWORD': get_env_variable('RDS_PASSWORD'),
          'HOST'    : get_env_variable('RDS_HOSTNAME'),
          'PORT'    : get_env_variable('RDS_PORT'),
          'OPTIONS' : {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
      }
  }
  ```
  
  4. docker-compose 명령을 사용하여 DB와 Django 서버 컨테이너를 실행시킵니다.
  <br>
  
  ```
  docker-compose -f ./docker-compose.yml up (-d)
  ```
  
> **Structure**
- #### 🛠 프로젝트 폴더구조

  ```
  📦.github
   ┣ 📂ISSUE_TEMPLATE
   ┃ ┣ 📜issue-template.md
   ┃ ┗ 📜issue_template.md
   ┗ 📜pull_request_template.md
  📦config
   ┗ 📂nginx
   ┃ ┗ 📜nginx.conf
  📦core
   ┣ 📂migrations
   ┃ ┗ 📜__init__.py
   ┣ 📂utils
   ┃ ┣ 📜decorator.py
   ┃ ┗ 📜get_obj_n_check_err.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜tests.py
   ┗ 📜views.py
  📦posts
   ┣ 📂migrations
   ┃ ┣ 📜0001_initial.py
   ┃ ┣ 📜0002_initial.py
   ┃ ┣ 📜0003_remove_post_tags_post_tags.py
   ┃ ┣ 📜0004_accessip.py
   ┃ ┗ 📜__init__.py
   ┣ 📂tests
   ┃ ┣ 📜__init__.py
   ┃ ┣ 📜tests_post_create.py
   ┃ ┣ 📜tests_post_delete.py
   ┃ ┣ 📜tests_post_detail.py
   ┃ ┣ 📜tests_post_like.py
   ┃ ┣ 📜tests_post_list.py
   ┃ ┣ 📜tests_post_restore.py
   ┃ ┗ 📜tests_post_update.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜serializers.py
   ┣ 📜urls.py
   ┗ 📜views.py
  📦sns
   ┣ 📜__init__.py
   ┣ 📜asgi.py
   ┣ 📜settings.py
   ┣ 📜urls.py
   ┗ 📜wsgi.py
  📦users
   ┣ 📂migrations
   ┃ ┣ 📜0001_initial.py
   ┃ ┗ 📜__init__.py
   ┣ 📂tests
   ┃ ┣ 📜__init__.py
   ┃ ┣ 📜tests_signin.py
   ┃ ┗ 📜tests_signup.py
   ┣ 📜__init__.py
   ┣ 📜admin.py
   ┣ 📜apps.py
   ┣ 📜models.py
   ┣ 📜serializers.py
   ┣ 📜urls.py
   ┗ 📜views.py
   ┣ 📜.env
   ┣ 📜.gitignore
   ┣ 📜docker-compose.yml
   ┣ 📜Dockerfile
   ┣ 📜manage.py
   ┣ 📜README.md
   ┗ 📜requirements.txt
  ```
