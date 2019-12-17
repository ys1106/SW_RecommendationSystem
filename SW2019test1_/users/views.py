import json
import random
import numpy as np
import pandas as pd
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from sklearn.metrics.pairwise import cosine_similarity

from users.forms import LoginForm, SignupForm
from users.models import UserInfo, Movie, Score, UserMovie, RecommendedMovie, EvaluatePage, RecommendedMoviePlus


# 로그인 페이지
def login_page(request):  # post 방식이면
    if request.user.is_authenticated:  # 로그인 되어 있다면
        return redirect('http://13.125.139.101/mypage')  # mypage

    if request.method == 'POST':
        form = LoginForm(request.POST)  # 로그인 폼
        if form.is_valid():  # 유효성 검사
            user_id = form.cleaned_data.get('userid')  # 입력받은 아이디
            user_password = form.cleaned_data.get('password')  # 입력받은 비밀번호

            try:  # 입력한 아이디를 가진 사용자가 있는지 확인
                User.objects.get(username=user_id)
            except:
                err = '아이디 또는 비밀번호를 다시 확인하세요.'
                return render(request, 'registration/login.html', locals())

            login_user = authenticate(username=user_id, password=user_password)  # 로그인 하려는 사용자 가져옴

            if login_user is not None:  # 로그인 하려는 사용자가 이미 존재하지 않는다면
                login(request, login_user)  # 로그인 실행
                return redirect('http://13.125.139.101/mypage')
            else:  # 없으면 에러메시지
                err = '아이디 또는 비밀번호를 다시 확인하세요.'
        return render(request, 'registration/login.html', locals())

    form = LoginForm()
    return render(request, 'registration/login.html', locals())


# 회원가입 페이지
def signup_page(request):
    if request.user.is_authenticated:  # 이미 로그인이 되어 있으면
        # return redirect(reverse('index'))
        redirect('http://13.125.139.101/mypage')  # mypage로

    if request.method == 'POST':
        form = SignupForm(request.POST)  # 회원가입폼 가져옴
        if form.is_valid():  # 유효성 검사
            try:
                user_password = form.password_check()  # 입력한 password 두 개가 일치하는지 확인하는 함수 -> 일치하면 그 비밀번호 저장
            except:  # 입력한 두 비밀번호가 다르면
                err = '두 비밀번호가 다릅니다.'
                return render(request, 'registration/signup.html', locals())  # 회원가입 페이지로 다시 이동

            user_id = form.cleaned_data.get('userid')
            try:
                User.objects.get(username=user_id)
                err = '있는 아이디입니다 ^0^'
                return render(request, 'registration/signup.html', locals())
            except:
                pass

            user_name = form.cleaned_data.get('name')
            user_email = form.cleaned_data.get('email')
            user_birth = form.cleaned_data.get('birth')

            try:
                signup_user = User.objects.create_user(username=user_id, email=user_email, password=user_password)
                UserInfo.objects.create(user=signup_user, name=user_name, birth=user_birth)
                return redirect(reverse('index'))
            except:
                err = '에러?'
                return render(request, 'registration/signup.html', locals())

        err = '회원가입이 실패하였습니다.'
        return render(request, 'registration/signup.html', locals())

    form = SignupForm()
    return render(request, 'registration/signup.html', locals())


# 로그아웃
def logout_page(request):
    logout(request)  # 로그아웃 함수
    return redirect(reverse('index'))


def index(request):  ## django 에서의 index (실제로는 필요 X - Vue의 메인페이지로 넘어갈 것)
    return render(request, 'index.html', locals())


def get_movies(ids):
    ids = [str(x) for x in ids]
    movies = Movie.objects.filter(id__in=ids)
    li = []
    for movie in movies:
        dictionary = {
            'id': movie.id,
            'title': movie.title,
            'director': movie.director,
            'genre': movie.genre,
        }
        li.append(dictionary)
    return li


def random_movies(request):
    # 사용자 영화 목록에 있는 목록은 선호페이지 영화목록에서 제외하기 위해
    user_ids = []
    try:
        user_movies = list(UserMovie.objects.get(user=request.user).movie_list.all())
        user_ids = [user_movies[i].id for i in range(len(user_movies))]  # 사용자 영화 목록에 있는 id 리스트
    except:
        pass

    # 전체 영화 id 리스트
    id_list = list(Movie.objects.values_list('id'))
    id_list = [id_list[i][0] for i in range(len(id_list))]

    # 사용자 영화목록에 있는 id들 제외
    s1 = set(user_ids)
    id_list = [x for x in id_list if x not in s1]

    ids = [random.choice(id_list) for x in range(20)]
    return HttpResponse(get_movies(ids), content_type=u"application/json; charset=utf-8")


def get_my_movies(request):  # 로그인유저의 마이리스트
    li = []
    try:
        user_movies = UserMovie.objects.get(user=request.user)
        print(user_movies.movie_list)
        for movie in user_movies.movie_list.all():
            dictionary = {
                'id': movie.id,
                'title': movie.title,
                'director': movie.director,
                'genre': movie.genre,
                # 'img': {% static 'media/' %}{{ movie.id }}.jpg,
            }
            li.append(dictionary)
    except:  # 마이리스트가 없으면 (추가 전)
        pass
    return HttpResponse(li, content_type=u"application/json; charset=utf-8")

#
# def get_recom_movies(request):  # 로그인유저의 추천리스트
#     li = []
#     try:
#         recom_movies = RecommendedMovie.objects.get(user=request.user)
#         print(recom_movies.recommend_list)
#         for movie in recom_movies.recommend_list.all():
#             dictionary = {
#                 'id': movie.id,
#                 'title': movie.title,
#                 'director': movie.director,
#                 'genre': movie.genre,
#             }
#             li.append(dictionary)
#     except:  # 추천 리스트가 없으면(추가하기 전)
#         pass
#
#     return HttpResponse(li, content_type=u"application/json; charset=utf-8")


@csrf_exempt
def add_my_movies(request):  # 추가하기 페이지에서 넘어오는 데이터 받아서 실행
    if request.method == 'POST':
        movie_list = json.loads(request.body.decode('utf-8'))
        movie_list = movie_list['addmovies']
        try:
            login_movies = UserMovie.objects.get(user=request.user)
        except:
            login_movies = UserMovie.objects.create(user=request.user)

        for movie in movie_list:
            movie_id = movie['id']
            movie_score = int(movie['score']) * 10  # 1~5 -> 10~100

            try:
                movie_ob = Movie.objects.get(id=movie_id)
                login_movies.movie_list.add(movie_ob)
                Score.objects.create(nickname=request.user.username, title=movie_ob.title, score=movie_score)
                # print(login_movies.user, login_movies.movie_list)
            except:
                pass

        # 추천받기 알고리즘 실행
        edit_recommend_movies(request)
        return HttpResponse([movie_list, movie_list[0]['id']], content_type=u"application/json; charset=utf-8")
    return HttpResponse('success')


# 추천받기

def predict_scores_one(request):  # 사용자 한 명에 대한 예측평점 행렬 구하기
    cos_matrix = pd.read_csv(r'C:\Users\yousu\PycharmProjects\SW2019test1_\cos_matrix.csv', encoding='utf-8')  # 코사인 유사도 행렬
    cos_matrix.set_index('title', inplace=True)
    print('cos_matrix', cos_matrix)

    scores_login = pd.read_csv(r'C:\Users\yousu\PycharmProjects\SW2019test1_\scores_for_user.csv', encoding='utf-8')  # 로그인한 사용자의 예측평점 Series 틀
    scores_login.set_index('title', inplace=True)
    print('scores_login', scores_login)
    # 로그인 유저의 평점데이터
    scores = list(Score.objects.filter(nickname=request.user.username))  # try?
    for score in scores:
        scores_login.loc[score.title]['score'] = float(score.score)

    cos_arr = cos_matrix.values
    score_arr = scores_login.values.ravel()
    num = 20

    predict_matrix = pd.DataFrame(np.zeros(score_arr.shape), index=scores_login.index)
    predict_matrix = predict_matrix.astype('float32')

    for ind in range(score_arr.shape[0]):
        top_n = np.argsort(cos_arr[:, ind])[:-num - 1:-1]
        predict_matrix.iloc[ind] = cos_arr[ind, :][top_n].dot(np.transpose(score_arr[top_n]))
        predict_matrix.iloc[ind] /= np.sum(np.abs(cos_arr[ind, :][top_n]))

    # 유저가 안 본 리스트
    already_seen = scores_login[scores_login['score'] > 0].index.tolist()
    movie_list = scores_login.index.tolist()  # 모든 영화명
    unseen_list = [movie for movie in movie_list if movie not in already_seen]
    return predict_matrix, unseen_list

#
# def recommend_movies(request):  # 영화 추천_예측평점 행렬에서 topn개 가져오기
#     predict_matrix_one_user, unseen_list_one_user = predict_scores_one(request)  # 로그인된 유저의 예측평점 행렬 & 안 본 영화리스트
#     # unseen_list_one_user = get_unseen_movies(request)
#     # topn = 5
#
#     # 로그인 유저의 평가한 영화 개수에 따라 추천해줄 영화 수 결정
#     if UserMovie.objects.get(user=request.user).movie_list.count() < 5:
#         topn = 5
#     elif UserMovie.objects.get(user=request.user).movie_list.count() < 10:
#         topn = 10
#     elif UserMovie.objects.get(user=request.user).movie_list.count() < 15:
#         topn = 15
#     else:
#         topn = 20
#
#     recom_movies = predict_matrix_one_user.loc[unseen_list_one_user].sort_values([0], ascending=False)[:topn]
#     # print(recom_movies)
#     # 추천된 영화리스트 RecommendedMovie DB에 넣기
#     try:  # 현재 로그인 되어있는 사용자 RecommendedMovie 객체 가져옴
#         user_recom = RecommendedMovie.objects.get(user=request.user)
#     except:  # 없으면 생성 (처음 추천받는 경우)
#         user_recom = RecommendedMovie.objects.create(user=request.user)
#
#     for movie_title in list(recom_movies.index):  # 추천영화리스트에 있는 영화제목
#         try:
#             recom_movie = Movie.objects.get(title=movie_title)  # 영화 객체 가져옴
#             user_recom.recommend_list.add(recom_movie)
#         except:
#             pass
#         # print(recom_movie)
#     return HttpResponse([UserMovie.objects.get(user=request.user).movie_list.count(),list(RecommendedMovie.objects.get(user=request.user).recommend_list.all()), len(list(RecommendedMovie.objects.get(user=request.user).recommend_list.all()))], content_type=u"application/json; charset=utf-8")
#

@csrf_exempt
def send_rating(request):  # 추천받은 영화 리스트에서 평가한 정보 받음
    if request.method == 'POST':
        movie_list = json.loads(request.body.decode('utf-8'))
        movie_list = movie_list['addmovies']
        try:
            login_movies = UserMovie.objects.get(user=request.user)
        except:
            login_movies = UserMovie.objects.create(user=request.user)

        # login_recom = RecommendedMoviePlus.objects.get(user=request.user)

        for movie in movie_list:
            movie_id = movie['id']
            movie_score = movie['score'] * 10  # 1~5 -> 10~100

            try:
                movie_ob = Movie.objects.get(id=movie_id)
                Score.objects.create(nickname=request.user.username, title=movie_ob.title, score=movie_score)
                login_movies.movie_list.add(movie_ob)
                # login_recom.recommend_list.remove(movie_ob)
                RecommendedMoviePlus.objects.filter(user=request.user.username, recommend_movie=movie_ob).delete()
                # print(login_movies.user, login_movies.movie_list)
            except:
                pass
        return HttpResponse([movie_list, movie_list[0]['id']], content_type=u"application/json; charset=utf-8")
    return HttpResponse('success')


@csrf_exempt
def evaluate_page(request):  # 웹페이지에 대한 평가 정보 받음
    if request.method == 'POST':
        evaluation = json.loads(request.body.decode('utf-8'))
        evaluation = evaluation['evaluate']
        evalute_value = int(evaluation)

        EvaluatePage.objects.create(user=request.user.username, evaluation=evalute_value)

        return HttpResponse([evalute_value], content_type=u"application/json; charset=utf-8")
    return HttpResponse('success')


def edit_recommend_movies(request):
    predict_matrix_one_user, unseen_list_one_user = predict_scores_one(request)  # 로그인된 유저의 예측평점 행렬 & 안 본 영화리스트

    # 로그인 유저의 평가한 영화 개수에 따라 추천해줄 영화 수 결정
    if UserMovie.objects.get(user=request.user).movie_list.count() < 5:
        topn = 5
    elif UserMovie.objects.get(user=request.user).movie_list.count() < 10:
        topn = 10
    elif UserMovie.objects.get(user=request.user).movie_list.count() < 15:
        topn = 15
    else:
        topn = 20

    recom_movies = predict_matrix_one_user.loc[unseen_list_one_user].sort_values([0], ascending=False)[:topn]
    print(recom_movies)

    for movie_title in list(recom_movies.index):  # 추천영화리스트에 있는 영화제목
        # 추천 영화의 예측평점 크기에 따라 추천 강도 설정
        if recom_movies.loc[movie_title].values > 8.5:
            predict_value = '상'
        elif recom_movies.loc[movie_title].values > 5:
            predict_value = '중'
        else:
            predict_value = '하'
        # 추천영화 객체 추가
        try:
            recom_movie = Movie.objects.get(title=movie_title)  # 영화 객체 가져옴
            RecommendedMoviePlus.objects.create(user=request.user.username, recommend_movie=recom_movie, predict=predict_value)
        except:
            pass
        print(recom_movie, predict_value)

    return HttpResponse([list(RecommendedMoviePlus.objects.filter(user=request.user.username))[0].recommend_movie,list(RecommendedMoviePlus.objects.filter(user=request.user.username))[0].predict, RecommendedMoviePlus.objects.filter(user=request.user).count()], content_type=u"application/json; charset=utf-8")


def edit_get_recom_movies(request):  # 로그인유저의 추천리스트
    li = []
    try:
        recom_movies = RecommendedMoviePlus.objects.filter(user=request.user.username)
        # print(recom_movies.recommend_list)
        for movie in recom_movies:
            dictionary = {
                'id': movie.recommend_movie.id,
                'title': movie.recommend_movie.title,
                'director': movie.recommend_movie.director,
                'genre': movie.recommend_movie.genre,
                'predict': movie.predict,
            }
            li.append(dictionary)
    except:  # 추천 리스트가 없으면(추가하기 전)
        pass
    return HttpResponse(li, content_type=u"application/json; charset=utf-8")


# def test_add_my_movies(request):  # 추가하기 페이지에서 넘어오는 데이터 받아서 실행
#
#     movie_list = [{'id': 2986, 'score':10},
#                   {'id': 2211, 'score':3}]
#     try:
#         login_movies = UserMovie.objects.get(user=request.user)
#     except:
#         login_movies = UserMovie.objects.create(user=request.user)
#
#     for movie in movie_list:
#         movie_id = movie['id']
#         movie_score = int(movie['score']) * 10  # 1~5 -> 10~100
#
#         try:
#             movie_ob = Movie.objects.get(id=movie_id)
#             login_movies.movie_list.add(movie_ob)
#             Score.objects.create(nickname=request.user.username, title=movie_ob.title, score=movie_score)
#             # print(login_movies.user, login_movies.movie_list)
#         except:
#             pass
#
#     # 추천받기 알고리즘 실행
#     edit_recommend_movies(request)
#     return HttpResponse([movie_list, movie_list[0]['id']], content_type=u"application/json; charset=utf-8")
