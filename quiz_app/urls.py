from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    
    path('sign_in_up_form/', views.sign_in_up_form, name='sign_in_up_form'),  
    path('sign_in/',views.sign_in, name='sign_in'),
    path('register/',views.register, name='register'),   
    path('signout/', views.signout, name='signout'),
    
    path('admin-home/', views.admin_home, name='admin-home'),
    
    path('admin-users/', views.admin_users, name='admin-users'),    
    path('user-add-form/', views.user_add_form, name='user-add-form'),
    path('save-user/', views.save_user, name='save-user'),    
    path('user-update-form/<str:pk>/',views.user_update_form, name='users-update-form'),
    path('user-update/<str:pk>/',views.user_update, name='user-update'),
    path('user-delete/<str:pk>/',views.user_delete, name='user-delete'),
    
    
    path('admin-topics/', views.admin_topics, name='admin-topics'),
    path('subtopic-add-form/', views.subtopic_add_form, name='subtopic-add-form'),
    path('admin-add-subtopic/', views.admin_add_subtopic, name='admin-add-subtopic'),
    path('subtopic-update-form/<str:pk>/',views.subtopic_update_form, name='subtopic-update-form'),
    path('subtopic-update/<str:pk>/',views.subtopic_update, name='subtopic-update'),
    path('subtopic-delete/<str:pk>/',views.subtopic_delete, name='subtopic-delete'),
    
    path('admin-questions/', views.admin_questions, name='admin-questions'),
    path('question-add-form/', views.question_add_form, name='question-add-form'),
    path('admin-add-question/', views.admin_add_question, name='admin-add-questions' ),
    path('question-update-form/<str:pk>/',views.question_update_form, name='question-update-form'),
    path('question-update/<str:pk>/',views.question_update, name='question-update'),
    path('question-delete/<str:pk>/',views.question_delete, name='question-delete'),
    
    
    path('admin-stats/',views.admin_stats, name='admin-stats'),
    
    path('quiz/',views.quiz, name='quiz'),  
    path('quiz/<int:pk>/',views.quiz_sub_topics, name='quiz_sub_topics'),  
    path('quiz/<int:pk>/<int:id>/',views.quiz_sub_topic_questions, name='quiz_sub_topic_questions'),  
    
    path('quiz-marked/<int:pk>/', views.quiz_marked, name='quiz_marked'),
    
]
