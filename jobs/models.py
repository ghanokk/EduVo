from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

# Status choices
STATUS_CHOICES = [
    ('open', 'Open'),        # Job is open for applications
    ('closed', 'Closed'),    # Job is closed
    ('draft', 'Draft'),      # Job is in draft mode
]

# Application Status choices
APPLICATION_STATUS_CHOICES = [
    ('pending', 'Pending'),
    
    ('rejected', 'Rejected'),
    ('accepted', 'Accepted')
]

# Category choices
CATEGORY_CHOICES = [
    ('web', 'Web Development'),
    ('design', 'Graphic Design'),
    ('data', 'Data Entry'),
    ('writing', 'Content Writing'),
    ('marketing', 'Marketing'),
    ('other', 'Other'),
]

# Work mode choices
WORK_MODE_CHOICES = [
    ('REMOTE', 'Remote'),
    ('ONSITE', 'On-site'),
    ('HYBRID', 'Hybrid'),
]

# Experience level choices
EXPERIENCE_LEVEL_CHOICES = [
    ('junior', 'Junior'),        # Entry-level
    ('confirmed', 'Confirmed'),  # Mid-level
    ('expert', 'Expert'),        # Expert
]

# Contract type choices
CONTRACT_TYPE_CHOICES = [
    ('cdi', 'CDI'),              # Permanent contract
    ('cdd', 'CDD'),              # Fixed-term contract
    ('internship', 'Internship'),
    ('freelance', 'Freelance'),
]

# Sector choices
SECTOR_CHOICES = [
    ('it', 'IT'),
    ('telecoms', 'Telecoms'),
    ('internet', 'Internet'),
    ('finance', 'Finance'),
    ('other', 'Other'),
]

# Education level choices
EDUCATION_LEVEL_CHOICES = [
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('phd', 'PhD'),
    ('other', 'Other'),
]

# Job model
class Job(models.Model):
    # Basic job information
    title = models.CharField(max_length=255)  # Job title
    description = models.TextField()  # Job description
    posted_by = models.ForeignKey('users.User', on_delete=models.CASCADE)  # User who posted the job
    company_name = models.CharField(max_length=255)  # Company name
    company_industry = models.CharField(max_length=255)  # Company industry
    location = models.CharField(max_length=100)  # Work location
    city = models.CharField(max_length=100)  # City
    country = models.CharField(max_length=100, default='Algeria')  # Country
    work_mode = models.CharField(max_length=10, choices=WORK_MODE_CHOICES, default='ONSITE')  # Work mode
    remote_option = models.BooleanField(default=False)  # Is remote work possible?
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # Category
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES, default='other')  # Sector
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES, default='junior')  # Required experience level
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE_CHOICES, default='cdi')  # Contract type
    education_level = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES, default='other')  # Required education level
    number_of_positions = models.IntegerField(default=1)  # Number of positions
    created_at = models.DateTimeField(auto_now_add=True)  # Creation date
    expiration_date = models.DateField(blank=True, null=True)  # Expiration date
    applications_count = models.IntegerField(default=0)  # Number of applications
    accepted_applications = models.IntegerField(default=0)  # Number of accepted applications
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')  # Job status
    main_missions = models.TextField()  # Main missions
    commercial_support = models.TextField()  # Commercial support
    development_tasks = models.TextField()  # Development tasks
    requirements = models.TextField()  # Requirements
    additional_responsibilities = models.TextField()  # Additional responsibilities

    def __str__(self):
        return f"{self.title} - {self.company_name}"  # Show job title and company name

    def get_absolute_url(self):
        return reverse('jobs:job_detail', args=[self.id])  # Direct link to the job

    class Meta:
        ordering = ['-created_at']  # Order by creation date (newest first)

# Job application model
class JobApplication(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    preferred_contact = models.CharField(max_length=20, blank=True)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)
    experience = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    availability = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    status=models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending')
    
    def get_status_display(self):
        return dict(APPLICATION_STATUS_CHOICES).get(self.status, 'Unknown')

    def __str__(self):
        applicant_name = getattr(self.applicant, 'username', None) if self.applicant else self.full_name or "WITHOUT NAME"
        return f"Applied to {self.job.title} from {applicant_name}" 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        applicant_name = getattr(self.applicant, 'username', None) if self.applicant else self.full_name or "WITHOUT NAME"
        return f"Applied to {self.job.title} from {applicant_name}" 

    class Meta:
        ordering = ['-created_at']

# Job Offer model
class JobOffer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    contract_type = models.CharField(max_length=50)
    expiration_date = models.DateField()
    location = models.CharField(max_length=255)
    required_skills = models.CharField(max_length=255)
    industry_sector = models.CharField(max_length=255)
    education_level = models.CharField(max_length=255)
    job_level = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    introduction = models.TextField()
    contact_email = models.EmailField()
    attachment = models.FileField(upload_to='job_attachments/', blank=True, null=True)
    posted_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
