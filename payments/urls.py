from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:course_id>/', views.payment_checkout, name='checkout'),  # (Afficher formulaire)
    path('process/<int:course_id>/', views.payment_process, name='process'),      # (Traiter paiement)
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),  # (Afficher succès)
    path('history/', views.payment_history, name='payment_history'),  # (Afficher historique)
]