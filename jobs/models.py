from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# خيارات الحالة
STATUS_CHOICES = [
    ('open', 'Open'),  # الوظيفة مفتوحة للتقديم
    ('closed', 'Closed'),  # الوظيفة مغلقة
    ('draft', 'Draft'),  # الوظيفة في طور المسودة
]

# خيارات التصنيف
CATEGORY_CHOICES = [
    ('web', 'Web Development'),  # تطوير مواقع ويب
    ('design', 'Graphic Design'),  # تصميم
    ('data', 'Data Entry'),  # إدخال وتنظيم البيانات
    ('writing', 'Content Writing'),  # كتابة المحتوى
    ('marketing', 'Marketing'),  # تسويق
    ('other', 'Other'),  # تصنيفات أخرى
]

# خيارات نمط العمل
WORK_MODE_CHOICES = [
    ('REMOTE', 'Remote'),  # العمل عن بعد
    ('ONSITE', 'On-site'),  # العمل في المكتب
    ('HYBRID', 'Hybrid'),  # مزيج بين العمل في المكتب والعمل عن بعد
]

# خيارات مستوى الخبرة
EXPERIENCE_LEVEL_CHOICES = [
    ('junior', 'Junior'),  # متدرب جديد
    ('confirmed', 'Confirmed'),  # لديه خبرة متوسطة
    ('expert', 'Expert'),  # خبير
]

# خيارات نوع العقد
CONTRACT_TYPE_CHOICES = [
    ('cdi', 'CDI'),  # عقد دائم (CDI)
    ('cdd', 'CDD'),  # عقد مؤقت (CDD)
    ('internship', 'Internship'),  # فترة تدريب
    ('freelance', 'Freelance'),  # عمل حر
]

# خيارات القطاع
SECTOR_CHOICES = [
    ('it', 'IT'),  # تكنولوجيا المعلومات
    ('telecoms', 'Telecoms'),  # قطاع الاتصالات
    ('internet', 'Internet'),  # خدمات الإنترنت
    ('finance', 'Finance'),  # قطاع المالي
    ('other', 'Other'),  # قطاعات أخرى
]

# خيارات المستوى الدراسي
EDUCATION_LEVEL_CHOICES = [
    ('bachelor', 'Bachelor'),  # شهادة الليسانس
    ('master', 'Master'),  # شهادة الماجستير
    ('phd', 'PhD'),  # شهادة الدكتوراه
    ('other', 'Other'),  # شهادات أخرى
]

# نموذج الوظيفة
class Job(models.Model):
    # معلومات الوظيفة الأساسية
    title = models.CharField(max_length=255)  # عنوان الوظيفة
    description = models.TextField()  # وصف الوظيفة
    posted_by = models.ForeignKey('users.User', on_delete=models.CASCADE)  # الشركة اللي ناضت الوظيفة
    company_name = models.CharField(max_length=255)  # اسم الشركة
    company_industry = models.CharField(max_length=255)  # قطاع الشركة
    location = models.CharField(max_length=100)  # موقع العمل
    city = models.CharField(max_length=100)  # المدينة
    country = models.CharField(max_length=100, default='Algeria')  # الدولة
    work_mode = models.CharField(max_length=10, choices=WORK_MODE_CHOICES, default='ONSITE')  # نمط العمل
    remote_option = models.BooleanField(default=False)  # هل العمل عن بعد ممكن؟
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # التصنيف
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES, default='other')  # القطاع
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES, default='junior')  # مستوى الخبرة المطلوب
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE_CHOICES, default='cdi')  # نوع العقد
    education_level = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES, default='other')  # المستوى الدراسي المطلوب
    number_of_positions = models.IntegerField(default=1)  # عدد الشواغر
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ إنشاء الوظيفة
    expiration_date = models.DateField(blank=True, null=True)  # تاريخ انتهاء صلاحية الوظيفة
    applications_count = models.IntegerField(default=0)  # عدد الطلبات
    accepted_applications = models.IntegerField(default=0)  # عدد الطلبات المقبولة
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')  # حالة الوظيفة
    main_missions = models.TextField()  # المهام الرئيسية
    commercial_support = models.TextField()  # دعم تجاري
    development_tasks = models.TextField()  # مهام التطوير
    requirements = models.TextField()  # المتطلبات
    additional_responsibilities = models.TextField()  # المسؤوليات الإضافية

    def __str__(self):
        return f"{self.title} - {self.company_name}"  # عرض عنوان الوظيفة واسم الشركة

    def get_absolute_url(self):
        return reverse('jobs:job_detail', args=[self.id])  # الرابط المباشر للوظيفة

    class Meta:
        ordering = ['-created_at']  # ترتيب حسب التاريخ (الأحدث أولاً)

# نموذج التقديم
class JobApplication(models.Model):
    applicant = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    class Meta:
        unique_together = ('applicant', 'job')
        ordering = ['-application_date']
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"

# نموذج التقديم
class Proposal(models.Model):
    # معلومات التقديم
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  # الوظيفة اللي تقدم عليها
    applicant = models.ForeignKey('users.User', on_delete=models.CASCADE)  # الشخص اللي تقدم
    full_name = models.CharField(max_length=255)  # الاسم الكامل
    email = models.EmailField()  # البريد الإلكتروني
    phone = models.CharField(max_length=20, blank=True, null=True)  # رقم الهاتف (اختياري)
    preferred_contact = models.CharField(
        max_length=10,
        choices=[
            ('email', 'email'),
            ('phone', 'phone'),
            ('both', 'both')
        ],
        default='email'  # طريقة التواصل المفضلة
    )
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)  # الشهادات والشهادات
    cover_letter = models.TextField()  # رسالة التقديم
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)  # السيرة الذاتية
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'pending'),  # في انتظار المراجعة
            ('reviewed', 'reviewed'),  # تم مراجعة الطلب
            ('accepted', 'accepted'),  # تم قبول الطلب
            ('rejected', 'rejected')  # تم رفض الطلب
        ],
        default='pending'  # الحالة الافتراضية
    )
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ التقديم
    updated_at = models.DateTimeField(auto_now=True)  # آخر تحديث للحالة

    def __str__(self):
        return f"تقديم على {self.job.title} من {self.applicant.username}"  # عرض اسم الوظيفة والمستخدم

    class Meta:
        ordering = ['-created_at']  # ترتيب حسب تاريخ التقديم (الأحدث أولاً)
