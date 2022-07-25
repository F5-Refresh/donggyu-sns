## Intro

원티드에서 진행하는 4주차 개인과제 레파지토리입니다.

본 과제에서 요구하는 서비스는 SNS(Social Networking Service)입니다.<br>
사용자는 SNS 서비스에 접속하여, 게시글을 업로드하고 관리(수정/삭제/복구)할 수 있습니다. 또한 다른 사람의 게시글을 확인하고, 좋아요를 누를 수 있습니다.

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
- ```📌 22.07.19 ~ 22.07.25```

<br>

> **Analysis**
- #### 필수 구현사항
  - 유저관리: 
    - 유저 회원가입: 이메일을 ID로 사용합니다.
    - 유저 로그인 및 인증: 로그인 성공 시 JWT토큰을 발급받으며, 추후 사용자 인증으로 사용합니다.
  - 게시글:
    - 게시글 생성
      - 제목, 내용, 해시태그 등을 입력하여 게시글을 생성합니다.
      - 제목, 내용, 해시태그는 필수사항이며, 작성자 정보는 request body에 존재하지 않고 해당 API를 요청한 인증정보에서 추출하여 사용합니다.
      - 참고로 해시태그는 #으로 시작합니다. (해시태그 입력 형태는 자유롭게 설정가능)
    - 게시글 목록
      - 모든 사용자(인증/인가에 통과한 유저)는 모든 게시물에 보기 권한이 있습니다.
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

          사용자는 입력한 키워드로 해당 키워드를 포함한 게시물을 조회할 수 있습니다.
          
          ex1) some-url?search=후기 >> "후기"가 제목에 포함된 게시글 목록
          ex2) "후기" 검색 시 >> 00 방문후기 입니다. (검색 됨)
        
        * Filtering(필터링)
          
          사용자는 지정한 키워드로 해당 키워드를 포함한 게시물을 필터링할 수 있습니다.

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
      
 - #### 선택 구현사항     
   - 댓글 기능
   - 싫어요/공감 기능
   - 조회수가 1인당 1번만 오르도록 제한
   - 유저 로그아웃 기능
 
 - #### 참고사항
   - 본 요구사항에 명시되지 않은 내용은 모두 자유롭게 구상하여 진행해주세요.
   - 필수 구현사항에 따라 진행하되, 개인별 완료 가능한 목표만큼 진행해보세요.
 

