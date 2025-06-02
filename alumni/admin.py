from django.contrib import admin
from .models import User,Events,ProposedEvents,Blog
# Register your models here.
admin.site.register(User)
admin.site.register(Events)
admin.site.register(ProposedEvents)
admin.site.register(Blog)