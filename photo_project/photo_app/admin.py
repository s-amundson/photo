from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Gallery, Images, LinkCategory, Links, Release, ReleaseTemplate, Talent, User

admin.site.register(Gallery)
admin.site.register(Images)
admin.site.register(LinkCategory)
admin.site.register(Links)
admin.site.register(Release)
admin.site.register(ReleaseTemplate)
admin.site.register(User, UserAdmin)
admin.site.register(Talent)