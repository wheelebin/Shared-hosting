from django.contrib import admin
from rango.models import Category, Page, UserProfile, Plan

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category')
	prepopulated_fields = {'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Plan)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)