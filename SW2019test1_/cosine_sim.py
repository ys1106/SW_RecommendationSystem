# 코사인유사도 행렬 구하기 위한 코드
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SW2019test1_.settings')
django.setup()
from users.models import Score
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# 평점 DB에서 가져오기
total_scores = list(Score.objects.all().values())
total_scores = pd.DataFrame(total_scores)  # ???
total_scores.sort_values('title', inplace=True)
total_scores.reset_index(drop=True, inplace=True)
print('total_scores', total_scores)  # total_scores에서 id 삭제해야??
total_scores

# # db 넣기 전_파일로 데이터 가져오기
# scores_data = []
# for i in range(63):
#     scores_data.append(pd.read_csv(
#         join('C:\\', 'Users', 'yousu', 'Documents', 'DataScience', 'SW201909', 'edit_users_scores1119',
#              'edit1119_scores' + str(i) + '.csv'), encoding='utf-8'))
# 영화 평점수 다 합치기
# total_scores = pd.concat(scores_data).drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], axis=1)
# total_scores.reset_index(drop=True, inplace=True)
# # 영화 평점들 데이터 제목순으로 정렬
# total_scores.sort_values('movie_title').reset_index(drop=True, inplace=True)
# total_scores

## pivot -> groupby
groupby_scores = total_scores.groupby(['nickname', 'title'])['score'].max().unstack()
groupby_scores.fillna(0, inplace=True)
groupby_scores = groupby_scores.astype('float32')
print('groupby_scores', groupby_scores)
groupby_scores.to_csv('groupby_scores.csv', encoding='utf-8-sig')


# index -movie title / score열- 0인 df 만들어서 csv저장 (예측행렬 구할 때 쓰임)
scores_for_user = pd.DataFrame(data=np.zeros(groupby_scores.shape[1]), index=groupby_scores.columns, columns=['score'])
scores_for_user.to_csv('scores_for_user.csv', index=True, encoding='utf-8-sig')

groupby_scores.columns
# 코사인 유사도

groupby_score_T = groupby_scores.transpose()
cos_array = cosine_similarity(groupby_score_T, groupby_score_T)
cos_matrix = pd.DataFrame(data=cos_array, index=groupby_scores.columns, columns=groupby_scores.columns)
cos_matrix.to_csv('cos_matrix.csv', encoding='utf-8-sig')
