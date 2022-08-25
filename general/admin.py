from django.contrib import admin

from general.models import *

# Register your models here.

class GuidelineAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() > 2:
            return False
        return True

admin.site.register(Guidelines, GuidelineAdmin)
admin.site.register(Feedback)
admin.site.register(Notice)
admin.site.register(AadharAddress)