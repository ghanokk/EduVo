from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Skill, UserSkill
from .forms import UserSkillForm

class SkillListView(LoginRequiredMixin, ListView):
    model = UserSkill
    context_object_name = 'user_skills'
    
    def get_queryset(self):
        return UserSkill.objects.filter(
            student_profile=self.request.user.student_profile
        ).select_related('skill')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_skills'] = Skill.objects.exclude(
            student_proficiencies__student_profile=self.request.user.student_profile
        )
        return context

class AddSkillView(LoginRequiredMixin, CreateView):
    model = UserSkill
    form_class = UserSkillForm
    success_url = reverse_lazy('skills:list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student_profile'] = self.request.user.student_profile
        return kwargs
    
    def form_valid(self, form):
        form.instance.student_profile = self.request.user.student_profile
        return super().form_valid(form)

class UpdateSkillView(LoginRequiredMixin, UpdateView):
    model = UserSkill
    form_class = UserSkillForm
    success_url = reverse_lazy('skills:list')
    
    def get_queryset(self):
        return super().get_queryset().filter(
            student_profile=self.request.user.student_profile
        )
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student_profile'] = self.request.user.student_profile
        return kwargs

class DeleteSkillView(LoginRequiredMixin, DeleteView):
    model = UserSkill
    success_url = reverse_lazy('skills:list')
    
    def get_queryset(self):
        return super().get_queryset().filter(
            student_profile=self.request.user.student_profile
        )





# from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin #LoginRequiredMixin yani l-user khasu ykoun mdakhil bash ydir accés l-had la page.
# #ListView hna t3tin wa7ed la liste TA3 lES éléments (hnaya l-UserSkill).



# from .models import Skill, UserSkill
# from .forms import UserSkillForm

# class SkillListView(LoginRequiredMixin, ListView):
#     model = UserSkill
#     context_object_name = 'user_skills' #Hadchi kaydir lina l-variable f template li ghadi tn3rf skills dyal l-user.
    
#     def get_queryset(self):
#         return UserSkill.objects.filter(user=self.request.user).select_related('skill')
#     #get_queryset: Hadi katkhdm filter bash t3tina seulement skills dyal l-user li dakhl fi système.


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['available_skills'] = Skill.objects.exclude(
#             userskill__user=self.request.user
#         )
#         return context
#     #get_context_data: Hadi katzid lina chi données supplémentaire li f l-context, f had tariqa katban lina skills li m3andouch l-user d'adhira.

# class AddSkillView(LoginRequiredMixin, CreateView):   #CreateView kaykhdm bash ydir création dyal wahda men les objets (l-UserSkill hna).


#     model = UserSkill  #Hna ghadi n'ajoutiw wa7ed l-compétence jdida l-user.
#     form_class = UserSkillForm #Kaydkhl lina le form dyal UserSkillForm bash ydkhlo les données.
#     success_url = reverse_lazy('skills:list') #fonction f Django li katsift l-url dyal view b wa7ed tariqa "lazy" (ma kayt9adarch l-url daba, kaytsna l7in l-url b3d). Hadi kats3ed bach n7aydo moshkilat da5la f ay points li kayna fi urls.py, l-
    
#     def get_form_kwargs(self):  #Hadi katdkhl lina l'user li m7taja f form, b7al bghina ndir l'ajout m3a l-user li dakhl.
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
    
#     def form_valid(self, form):  # Hna katkhli form instance li nzid fih l-user li dakhl m3a skill
#         form.instance.user = self.request.user
#         return super().form_valid(form)

# class UpdateSkillView(LoginRequiredMixin, UpdateView):  #UpdateView t3tik l'update d'un objet (fi had tariqa, kaydir modification l'UserSkill).
#     model = UserSkill
#     form_class = UserSkillForm
#     success_url = reverse_lazy('skills:list')
    
#     def get_queryset(self):
#         return super().get_queryset().filter(user=self.request.user) #Hadi katzid l-filter bash t3rf wach l-user m3andoch l-accès l-modification skill dyalo.
    
#     def get_form_kwargs(self): # Kaydkhl lina user li bghina nupdatew l'UserSkill.
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

# class DeleteSkillView(LoginRequiredMixin, DeleteView):  #DeleteView katsift l-suppression de l'objet (f had tariqa, katsift la suppression de UserSkill).
#     model = UserSkill
#     success_url = reverse_lazy('skills:list')
    
#     def get_queryset(self): #get_queryset: Hadi katzid filter l-UserSkill li ykoun m3ayen l-user li dakhl bash ma n9adarch y7edf chi skill li ma3ndouch.
#         return super().get_queryset().filter(user=self.request.user)