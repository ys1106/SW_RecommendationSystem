from django.urls import path

from users import views as users_views

app_name = 'users'

urlpatterns = [
    # html (page)
    path('login/', users_views.login_page, name='login'),
    path('logout/', users_views.logout_page, name='logout'),
    path('signup/', users_views.signup_page, name='signup'),

    # api (data)
    path('recommend_movies/', users_views.edit_recommend_movies, name='recommendmovies'),  # 마이페이지에서 추천받기 클릭하면 실행
    path('addmymovies/', users_views.add_my_movies, name='addmymovies'),  # 추가하기 페이지에서 영화들 선택 후 실행
    path('sendrating/', users_views.send_rating, name='evaluate_recom/'),  # 추천받은 영화 평가 후 실행
    path('evaluatepage/', users_views.evaluate_page, name='evaluatepage'),  # 페이지에 대한 평가 후 실행

    path('randommovies/', users_views.random_movies, name='randommovies'),  # 영화정보
    path('mymovies/', users_views.get_my_movies, name='getmymovies'),  # 로그인 유저의 mylist
    path('recommovies/', users_views.edit_get_recom_movies, name='recommovies'),  # 로그인 유저의 recommended list

    ###TEST
    # path('editrecommendmovies/', users_views.edit_recommend_movies, name='editrecommendmovies'),
    # path('editgetrecommovies/', users_views.edit_get_recom_movies, name='editgetrecommovies'),
    # path('testaddmymovies/', users_views.test_add_my_movies, name='testaddmymovies'),
]