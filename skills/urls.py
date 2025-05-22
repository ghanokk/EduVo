from django.urls import path
from .views import SkillListView, AddSkillView, UpdateSkillView, DeleteSkillView

app_name = 'skills'

urlpatterns = [
    path('', SkillListView.as_view(), name='list'),  #Had smiya dyal l-view ghadi tst3mlha f l-templates w fi l-redirects.
    #Chno kaydir: Katban l-liste dyal skills dyal l-user m3a skills li ma zadu hachouma.
    path('add/', AddSkillView.as_view(), name='add'), # L-7isab f templates w f l-redirect.
    #Chno kaydir: Kay7ell lina formulaire bash nzido wa7ed l-compétence jdida l-user.

    path('<int:pk>/update/', UpdateSkillView.as_view(), name='update'), #URL: /pk/update/ (binan pk t3tik li l-id dyal l-UserSkill).
    #Chno kaydir: Kay7ell formulaire bach ydir l-update l-skill li 3andu l-user, b ghayr ma yzid id.


    path('<int:pk>/delete/', DeleteSkillView.as_view(), name='delete'),
    #Chno kaydir: Katb9a l-user ysuprimmi l-skill dyalhu men system.


]