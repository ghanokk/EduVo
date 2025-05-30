from django.urls import path
from .views import SkillListView, AddSkillView, UpdateSkillView, DeleteSkillView

app_name = 'skills'

urlpatterns = [
    # List all skills for the current user (student or teacher only)
    path('', SkillListView.as_view(), name='list'),

    # Add a new skill (student or teacher only)
    path('add/', AddSkillView.as_view(), name='add'),

    # Update a user's skill (student or teacher only)
    path('<int:pk>/update/', UpdateSkillView.as_view(), name='update'),

    # Delete a user's skill (student or teacher only)
    path('<int:pk>/delete/', DeleteSkillView.as_view(), name='delete'),
    
]
