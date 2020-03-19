import datetime
# Django includes
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.views import login 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.functions import Lower
from django.forms.models import modelformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

# DB Includes
from .models import Icon, Person, Training_session, Training_spec

# Forms
from .forms import SessionForm

# NNT Training Views


class PageNotFoundView(generic.ListView):
	template_name = "ts_training/404.html"


class HomeView(generic.ListView):
	model = Icon
	template_name = "ts_training/index.html"
	context_object_name = "page_list"

	def get_queryset(self):
		# Exclude training categories
		return Icon.objects.filter(itemType='PAGE')


class AboutView(generic.TemplateView):
	model = Icon
	template_name = "ts_training/about.html"


class PeopleView(generic.ListView):
	template_name = "ts_training/people.html"
	model = Person
	context_object_name = "context"

	def get_context_data(self):
		context = {}
		# Get all the people. Lower required to allow for mixed-case in DB
		context['people'] = Person.objects.all()
		# Get the training categories
		context['cats'] = Icon.objects.filter(itemType='CAT').order_by('weight').only('iconName')
		return context


class PersonView(generic.DetailView):
	template_name = "ts_training/people-single.html"
	model = Person


class TrainingView(generic.ListView):
	model = Training_spec
	template_name = "ts_training/training.html"
	context_object_name = "training"


class TrainingDetailView(generic.DetailView):
	template_name = "ts_training/training-detail.html"
	model = Training_spec
	context_object_name = "item"


class SessionView(generic.ListView):
	template_name = "ts_training/session.html"
	model = Training_session

	def get_queryset(self):
		today = datetime.date.today()
		sessions = Training_session.objects.filter(date__gte=today).order_by('-date')
		return sessions 
	context_object_name = "sessions"


class SessionSingleView(generic.DetailView):
	model = Training_session
	template_name = "ts_training/session-single.html"


def is_nt_staff(user):
	return user.is_staff


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_nt_staff), name='dispatch')
class SessionNewView(SuccessMessageMixin, CreateView):
	model = Training_session
	form_class = SessionForm
	template_name = "ts_training/session-form.html"
	success_message = "Session created successfully."

	def get_success_url(self):
		return reverse_lazy('ts_training:ntSessionSingle', kwargs={'pk': self.object.pk })


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_nt_staff), name='dispatch')
class SessionEditView(SuccessMessageMixin, UpdateView):
	model = Training_session
	form_class = SessionForm
	template_name = "ts_training/session-form.html"
	success_message = "Session edited successfully."

	def get_success_url(self):
		return reverse_lazy('ts_training:ntSessionSingle', kwargs={'pk': self.object.pk})

class allSessionView(generic.ListView):
	model = Training_session
	template_name = "ts_training/all-session.html"
	def get_queryset(self):
		today = datetime.date.today()
		sessions = Training_session.objects.order_by('-date')
		return sessions 
	context_object_name = "sessions"


# Auth Views

class NTLoginView(auth_views.LoginView):
	template_name = "ts_training/login.html"


class NTLogoutView(auth_views.LogoutView):
	extra_context = {'logged_out': True }
	template_name = "ts_training/index.html"


# Already have login_required inherently
class NTUserEdit(auth_views.PasswordChangeView):
	template_name = "ts_training/user-edit.html"

	def get_success_url(self):
		return reverse_lazy('ts_training:ntUserEditDone')


class NTUserEditDone(auth_views.PasswordChangeDoneView):
	template_name = "ts_training/user-edit-done.html"

# Flash Messages


def logged_in_message(sender, user, request, **kwargs):
	# Add a welcome message when the user logs in
	messages.success(request, "Login successful!")


def logged_out_message(sender, user, request, **kwargs):
	# Add a welcome message when the user logs in
	messages.info(request, "You have logged out.")


user_logged_in.connect(logged_in_message)
user_logged_out.connect(logged_out_message)