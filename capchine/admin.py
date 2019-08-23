from django.contrib import admin
from .models import Student, Teacher, Search_Code, Rating, Role
# Register your models here.

def view_link():
    return u"www.google.com"


class StudentAdmin(admin.ModelAdmin): 

    list_display = ('u','total_ratings','inactive_search_codes','this_link','active_search_codes','created')
    

admin.site.register(Student, StudentAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('u','my_role')
admin.site.register(Role,RoleAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('u','search_count','rating_count','search_code_used','search_code_usage_time','search_codes_used','created')
    ordering = ['-search_count',]

admin.site.register(Teacher, TeacherAdmin)

class Search_CodeAdmin(admin.ModelAdmin):
    list_display = ('u','code','created')
admin.site.register(Search_Code, Search_CodeAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('code','u','teacher','rating','rated','created')
admin.site.register(Rating, RatingAdmin)