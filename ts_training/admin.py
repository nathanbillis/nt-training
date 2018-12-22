from django.contrib import admin
from django.db import models 
from django.forms import CheckboxSelectMultiple

# Register your models here.

from .models import Icon, Person, Training_session, Training_spec


class PersonAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name','slug','email','status','grad_year', 'committee']
	prepopulated_fields = {"slug": ("first_name", "last_name",)}
	list_display = ('slug', 'first_name', 'last_name', 'email','status', 'grad_year', 'committee')
	search_fields = ['first_name', 'last_name', 'grad_year', 'email']
	list_filter = ['status', 'grad_year', 'committee']

	def make_graduated(modeladmin, request, queryset):
		queryset.update(status='GRAD')

	def make_student(modeladmin, request, queryset):
		queryset.update(status='STU')

	def make_unknown(modeladmin, request, queryset):
		queryset.update(status='UNKNOWN')

	def toggle_committee(modeladmin, request, queryset):
		for person in queryset:
			if not person.committee:
				# If not on committee
				setattr(person, 'committee', True)
			elif person.committee:
				# if on Committee
				setattr(person, 'committee', False)
			person.save() 

	actions = [make_graduated,make_student,make_unknown, toggle_committee]


class TrainingSpecAdmin(admin.ModelAdmin):
	list_filter = ['category']
	list_display = ['trainingId', 'category', 'trainingTitle', 'description', 'safety']

	def toggle_safety(modeladmin, request, queryset):
		for item in queryset:
			if not item.safety:
				# item.update(safety=True)
				setattr(item, 'safety', True)
				item.save()  
			elif item.safety:
				# item.update(safety=False)
				setattr(item, 'safety', False)
				item.save()

	actions = [toggle_safety]


class TrainingSessionAdmin(admin.ModelAdmin):
	list_display = ['pk','trainer', '__str__', 'date',]
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	}
	list_filter = ['date','trainee','trainer']


class IconAdmin(admin.ModelAdmin):
	prepopulated_fields = {"description": ("iconName",)}
	list_display = ['itemType', 'weight', 'iconName', 'iconRef']
	list_filter = ['itemType']


admin.site.register(Person, PersonAdmin)
admin.site.register(Training_session, TrainingSessionAdmin)
admin.site.register(Training_spec, TrainingSpecAdmin)
admin.site.register(Icon, IconAdmin)