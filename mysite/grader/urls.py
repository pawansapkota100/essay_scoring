from django.urls import path


from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('essay-prediction/', views.essay_prediction, name='essay_prediction'),
    path('essay-writing-forum/', views.essay_writing_forum, name='essay_writing_forum'),
    path('<int:question_id>/', views.question, name='question'),
    path('<int:question_id>/essay<int:essay_id>/', views.essay, name='essay'),
    path('view_answer/<int:content_id>/', views.view_answers, name='view_answer'),
    path('ask_essay/', views.ask_essay, name='ask_essay'),
    path('ask_essay/success/', views.success, name='success'),
    path('login/', views.signin, name='login'),
    path('register/', views.register, name='register'),
    path('fail',views.fail, name='fail'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('update_profile/', views.update_profile, name='update_profile'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)