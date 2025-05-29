from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Skill, UserSkill
from .forms import UserSkillForm

# Cette view t'affiche la liste des compétences (skills) li 3andek enta (li li user connecté)
class SkillListView(LoginRequiredMixin, ListView):
    model = UserSkill
    context_object_name = 'user_skills'
    
    def get_queryset(self):
        # Rani nfetchi juste les skills li 3and user connecté
        return UserSkill.objects.filter(
            student_profile=self.request.user.student_profile
        ).select_related('skill')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Hna jibna les skills li mazal user ma zadhomch (donc disponibles à ajouter)
        context['available_skills'] = Skill.objects.exclude(
            student_proficiencies__student_profile=self.request.user.student_profile
        )
        return context

# Cette view hiya pour ajouter une compétence jdida (skill jdida)
class AddSkillView(LoginRequiredMixin, CreateView):
    model = UserSkill
    form_class = UserSkillForm
    success_url = reverse_lazy('skills:list')  # ba3d l'ajout, yrj3ni l'list
    
    def get_form_kwargs(self):
        # Passer le profil du user li form, bach yfiltri les skills
        kwargs = super().get_form_kwargs()
        kwargs['student_profile'] = self.request.user.student_profile
        return kwargs
    
    def form_valid(self, form):
        # Assigni le profil du user connecté li l'objet skill
        form.instance.student_profile = self.request.user.student_profile
        return super().form_valid(form)

# Cette view pour modifier compétence deja 3andek
class UpdateSkillView(LoginRequiredMixin, UpdateView):
    model = UserSkill
    form_class = UserSkillForm
    success_url = reverse_lazy('skills:list')  # ba3d update, ydir redirect l'list
    
    def get_queryset(self):
        # Juste les skills li 3and user li yqder ymodifiha
        return super().get_queryset().filter(
            student_profile=self.request.user.student_profile
        )
    
    def get_form_kwargs(self):
        # Même logique comme dans CreateView
        kwargs = super().get_form_kwargs()
        kwargs['student_profile'] = self.request.user.student_profile
        return kwargs

# Cette view pour supprimer compétence men list nta3k
class DeleteSkillView(LoginRequiredMixin, DeleteView):
    model = UserSkill
    success_url = reverse_lazy('skills:list')  # ba3d suppression, ydir redirect l'list
    
    def get_queryset(self):
        # Tqdr tmas7 juste les skills li nta 3andek
        return super().get_queryset().filter(
            student_profile=self.request.user.student_profile
        )



