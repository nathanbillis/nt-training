# Tags relating to planned sessions primarily.

from django import template
from ..models import Icon, Person, Training_spec, Planned_session

register = template.Library() 

def ordered_set(seq):
	# From https://stackoverflow.com/a/480227 - remove duplicates and maintain order
  seen = set()
  seen_add = seen.add
  return [x for x in seq if not (x in seen or seen_add(x))]

@register.simple_tag
def person_trained(person):
	# Returns a list of training sessions in which the person is a trainer
	trained = Planned_session.objects.filter(trainer=person).order_by('date').prefetch_related('trainingId').prefetch_related('signed_up')
	return trained

@register.simple_tag
def session_cats(session):
	# Returns the list of categories covered in a given training session
	ids = session.trainingId.order_by('trainingId').select_related('category') #Get points
	session_cat_list = [] #For population later
	for trainingid in ids:
		session_cat_list.append(trainingid.category.iconRef)

	session_cat_list = ordered_set(session_cat_list) #Preserve numerical order
	allcats = Icon.objects.filter(itemType = 'CAT')
	session_cat_dict = {} #Dictionary for use in templates
	for cat in session_cat_list:
		this_cat_icon = allcats.get(iconRef = cat)
		session_cat_dict[cat] = this_cat_icon

	return session_cat_dict

@register.inclusion_tag('ts_training/template_tags/planned-card.html')
def session_cards(sessions=None):
	# Display training sessions as panels
	# (also uses session_cats, above, in the inclusion tag)
	if sessions == None:
		# If no sessions are given, default to use all of them
		sessions = Planned_session.objects.all().prefetch_related('trainingId')

	return {'sessions': sessions}