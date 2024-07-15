from django.contrib import admin

from .models import Question, Quiz, Topic, Sub_Topic, Student

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Topic)
admin.site.register(Sub_Topic)
admin.site.register(Student)
admin.site.register(Question)

