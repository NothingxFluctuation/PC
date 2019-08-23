from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.html import mark_safe
# Create your models here.
ROLE_CHOICES = (
    ('student','Student'),
    ('teacher','Teacher'),
)
class Role(models.Model):
    u = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roly')
    my_role = models.CharField(max_length=50, choices=ROLE_CHOICES, null = True, blank = True)

    def __str__(self):
        return self.u.get_full_name()
    


class Student(models.Model):
    u = models.ForeignKey(User,related_name="stdnt_info",on_delete=models.CASCADE)
    code_count = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)    

    def __str__(self):
        return self.u.get_full_name()
    
    def total_ratings(self):
        attnt = 0
        prfrm = 0
        punct = 0
        coop = 0
        count = 0
        ratings = Rating.objects.filter(u = self.u, active = True)
        for r in ratings:
            if r.attention:
                attnt += r.attention
                prfrm += r.performance
                punct += r.punctuality
                coop += r.cooperation
                count +=1
        total = attnt + prfrm + punct + coop
        return total
    
    def inactive_search_codes(self):
        srch_codes = self.u.my_srch_code.filter(active=False)
        l = []
        for s in srch_codes:
            l.append(s.code)
        return l

    def active_search_codes(self):
        srch_codes = self.u.my_srch_code.filter(active=True)
    
        link = "http://127.0.0.1:8000/admin_student/?code="
        d = {}
        for s in srch_codes:
            new_link = link + str(s.code)
            d["m{0}".format(s.id)] = '<p><a href="{}">{}</a><p>'.format(new_link, s.code)

        keys = d.keys()
        for k in keys:
            k = d[k]
        a = d.values()
        l  = ' '
        l = l.join(a)
        return mark_safe(l)
    active_search_codes.short_description = ('Codes')
         


    def this_link(self):
        return mark_safe('<a href="https://www.google.com">visit google</a>')
    this_link.short_description = ('GOOGLE')



class Teacher(models.Model):
    u = models.ForeignKey(User, related_name="tchr_info",on_delete=models.CASCADE)
    search_count = models.IntegerField(blank=True, null = True)
    rating_count = models.IntegerField(blank = True, null = True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.u.get_full_name()
    
    def search_code_used(self):
        s = Search_Code.objects.filter(accessed_by=self.u)
        return len(s)
    
    def search_code_usage_time(self):
        s = Search_Code.objects.filter(accessed_by=self.u)
        usage_time = ''
        for t in s:
            b = str(t.accessed_date.time())
            b = b.split('.')
            b = b[0]
            usage_time =  usage_time + b + ' '
        usage_time = '[' + usage_time + ']'
        return usage_time  
    def search_codes_used(self):
        s = Search_Code.objects.filter(accessed_by=self.u)
        codes = ''
        b = None
        for ss in s:
            b = str(ss.code)
            codes += b + ' '
        return codes






class Search_Code(models.Model):
    u = models.ForeignKey(User, related_name="my_srch_code", on_delete=models.CASCADE)
    code = models.CharField(max_length = 200)
    accessed_by = models.ManyToManyField(User, related_name='accessed_code',blank = True)
    accessed_date = models.DateTimeField(null = True, blank = True)
    active = models.BooleanField(default = True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.u.get_full_name()




class Rating(models.Model):
    code = models.CharField(max_length = 200, blank = True, null = True)
    u = models.ForeignKey(User, related_name="my_rating", on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, related_name="given_rating", on_delete=models.CASCADE, null = True, blank = True)
    rating = models.IntegerField(null = True, blank = True)
    attention = models.IntegerField(null = True, blank = True)
    performance = models.IntegerField(null = True, blank = True)
    punctuality = models.IntegerField(null = True, blank = True)
    cooperation = models.IntegerField(null = True, blank = True)
    active = models.BooleanField(default=True)
    rated = models.CharField(max_length = 200, null = True, blank = True)
    created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.u.get_full_name()


class check(models.Model):
    cd = models.CharField(max_length = 15)
