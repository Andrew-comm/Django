from curses import meta
from pyexpat import model
from django.forms import ModelForm
from .models import Room



class RoomForm(ModelForm):
   class Meta:
    model = Room
    fields = '__all__'

    exclude =['host','participants']

