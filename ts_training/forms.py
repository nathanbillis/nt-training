# Import
# #Global
import datetime
# #Django
from django import forms 
from django.urls import reverse
# #DB
from .models import Icon, Training_spec, Person, Training_session


class DateInput(forms.DateInput):
		input_type = 'date'


class SessionForm(forms.ModelForm):
	# Model: Training_session. All of these fields are within this model.
	class Meta:
		model = Training_session
		fields = ['trainer', 'trainee', 'trainingId', 'date']
		labels = {
			'trainingId': 'Training Points',
			'trainee': 'People Trained',
			'trainer': 'Trainer'
		}
		widgets = {
			'date': DateInput(),
			'trainingId': forms.CheckboxSelectMultiple(),
			'trainee': forms.CheckboxSelectMultiple(),
		}

	def clean(self):
		trainee = self.cleaned_data.get('trainee')
		training_id = self.cleaned_data.get('training_id')
		trainer = self.cleaned_data.get('trainer')
		errors = {}
		# Can't submit without a valid trainer or date, so don't need to validate those.
		if trainee is None:
			errors['trainee'] = forms.ValidationError('Please select some trainees.')
		if training_id is None:
			errors['training_id'] = forms.ValidationError("You can't have a session without something to learn."
														  " Please select some training points.")
		if trainee is not None:
			if trainer in trainee.all():  # But the trainer should not be in the list of trainees.
				errors['trainer'] = forms.ValidationError("The trainer can't train themselves!")

		if errors:
			raise forms.ValidationError(errors)
			return self.cleaned_data
		
		# return self.cleaned_data

