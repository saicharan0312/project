from django.contrib import admin

# Register your models here.

from .models import  User,Individual,Corporate,event_contrib,event_creation,demo
admin.site.register(User)
admin.site.register(Corporate)
admin.site.register(Individual)
admin.site.register(event_creation)
admin.site.register(event_contrib)
admin.site.register(demo)
#admin.site.register(Room)

