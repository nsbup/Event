from multiprocessing import Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django import forms
from django.utils.translation import gettext as _

from afl_events.models import Event

class DateInput(forms.DateInput):
    input_type = 'date'

class RegisterForm(UserCreationForm):
    # birthdate = forms.DateField()
    # discord_id = forms.CharField(max_length=100, help_text='Discord ID')
    # zoom_id = forms.CharField(max_length=100, help_text='Zoom ID')
    pass
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]    



class EventAddForm(forms.ModelForm):
    ## change the widget of the date field.
    
    def __init__(self, *args, **kwargs):
        super(EventAddForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
                'id':name
            })

    class Meta:
        model = Event
        fields = ("__all__")    
        widgets = {
            'name' : forms.TextInput(),
            'date' : DateInput(),
            'time' : forms.TextInput(),
            'duration' : forms.TextInput(),
        }
        labels 	= {
            'eid' : _("Event ID"),
            'name' : _("Event Name"),
            'date' :_("Event Date"),
            'time' :_("Event Time"),
            'duration' :_("Duration"),
        }