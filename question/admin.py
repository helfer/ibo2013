from django.contrib import admin
from ibo2013.question.models import Question,Language,Exam,VersionNode,ExamQuestion

admin.site.register(Question)
admin.site.register(Language)
admin.site.register(Exam)
admin.site.register(VersionNode)
admin.site.register(ExamQuestion)
