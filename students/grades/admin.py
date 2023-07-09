from django.contrib import admin

# Register your models here.
from .models import Student, Test
#from .models import Student
admin.site.register([Student, Test])
