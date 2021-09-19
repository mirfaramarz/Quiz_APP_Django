from django.contrib import admin
from .models import *


admin.site.site_header = "Quiz App"
from django.contrib.auth.models import Group
admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    list_display = ("id","name","email")
admin.site.register(User,UserAdmin)


admin.site.register(Category)
# admin.site.register(Status)

admin.site.register(Language)
admin.site.register(Completed_Quiz)


@admin.register(Payment)
class HeroAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "date",]


class POSTQuestionAdmin(admin.StackedInline):
    model = Question

class QuizAdmin(admin.ModelAdmin):
    list_display = ("category","level","language","Win_Payment")
    inlines = [POSTQuestionAdmin]


admin.site.register(Quiz,QuizAdmin)