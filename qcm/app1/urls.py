from django.urls import path
from .views import ShowQuestion,ShowResult,ReviewAnswers,ScoreView,FB


urlpatterns = [
    path('<int:sub_id>/', ShowQuestion.as_view(), name='subcategory_questions'),
    path('home/<int:sub_id>/', ShowQuestion.as_view(), name='show_questions_by_subcategory'),
    path('category/<int:category_id>/', ShowQuestion.as_view(), name='show_questions_by_category'),
    path('domain/<int:domain_id>/', ShowQuestion.as_view(), name='show_questions_by_domain'),
    path('home/result/>', ShowResult.as_view(), name='result'),
    path('result/', ShowResult.as_view(), name='result'),  # you can add the sub_id if need it 
    path('home/<int:sub_id>/', ShowQuestion.as_view(), name='subcategory_questions'),
    path('review/',ReviewAnswers.as_view(),name='review'),
    path('score/',ScoreView.as_view(),name="save_score"),
    path('leaderboard/',ScoreView.as_view(),name="leaderboard"),
    path('feedback/',FB.as_view(),name="feedback")

]


    

#  path('home/<int:sub_id>/result/', ShowQuestion.as_view(), name='result'),
#  path('<int:sub_id>/result/', ShowQuestion.as_view(), name='result'), """