from django import forms
from .models import UserSkill, Skill

class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['skill', 'proficiency_level']
    
    def __init__(self, student_profile=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if student_profile:
            self.fields['skill'].queryset = Skill.objects.exclude(
                student_proficiencies__student_profile=student_profile
            )



# from django import forms
# from .models import UserSkill, Skill

# class UserSkillForm(forms.ModelForm): #يرث من forms.ModelForm: هذه هي الطريقة التي تقوم Django بها بإنشاء نموذج يعتمد على نموذج قاعدة البيانات (Model)
#     class Meta:
#         model = UserSkill   #يعني أن هذا النموذج يعتمد على موديل UserSkill في قاعدة البيانات.
#         fields = ['skill', 'proficiency_level'] #fields = ['skill', 'proficiency_level']: حددنا الحقول التي سيتم استخدامها في النموذج وهما:


    
#     def __init__(self, user=None, *args, **kwargs):   #هذه هي الطريقة التي تقوم بتهيئة النموذج,اذا تم تمرير مستخدم عند إنشاء النموذج,سيتم تعديل عقل المهارة ليعرض فقط المهارات التي لم يتم إضافتها بعد للمستخدم المحدد
#             self.fields['skill'].queryset = Skill.objects.exclude(    #هذا يعني أن المستخدم لن يستطيع اختيار مهارات سبق له إضافتها.
#                 userskill__user=user
#             )

            #يتم استخدام هذا النموذج لإضافة مهارة جديدة للمستخدم، ولكن مع ضمان أن المستخدم لا يستطيع إضافة نفس المهارة التي قد أضافها بالفعل.

#هذا النموذج مفيد إذا كنت ترغب في تمكين المستخدم من إضافة مهارات جديدة وتحديد مستوى إتقانهم لها دون تكرار المهارات التي تم إضافتها مسبقًا