from django.contrib import admin
from mystays.models import Stay, Review, UserProfile

class StayAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Stay, StayAdmin)
admin.site.register(Review)
admin.site.register(UserProfile)
