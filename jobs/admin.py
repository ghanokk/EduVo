from django.contrib import admin
from .models import Job, Proposal,JobApplication

admin.site.register(Job)
admin.site.register(Proposal)
admin.site.register(JobApplication)