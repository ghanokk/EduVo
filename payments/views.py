from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from courses.models import Course, Enrollment
from .models import Payment
from django.contrib import messages

# (Afficher la page de paiement — formulaire manuel)
@login_required
def payment_checkout(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # (yji l'utilisateur ychoisi méthode de paiement w ykhdem paiement)
    return render(request, 'payments/checkout.html', {'course': course})


# (Après que user yvalide formulaire, ndirou le traitement)
@login_required
def payment_process(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # (Exemple: simuler succès de paiement - en vrai tkoun logique de validation ici)
    payment = Payment.objects.create(
        user=request.user,
        course=course,
        amount=course.price,
        status='completed',
        payment_method='edahabia',  # (par exemple, tu peux rendre ça dynamique via formulaire)
        payment_date=timezone.now(),
        transaction_id=f"SIMU-{timezone.now().timestamp()}"
    )

    # (Auto-inscription de l'utilisateur au cours)
    Enrollment.objects.get_or_create(student=request.user, course=course)

    messages.success(request, "✅ Le paiement a été effectué avec succès!")
    return redirect('payments:payment_success', payment_id=payment.id)


# (Afficher message succès avec infos du paiement)
@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payments/success.html', {'payment': payment})


# (Afficher historique mta3 l’utilisateur)
@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-payment_date')
    return render(request, 'payments/history.html', {'payments': payments})
