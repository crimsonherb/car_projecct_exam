from django.forms import ModelForm

from .models import CarModel


class CarForm(ModelForm):
    class Meta:
        model = CarModel
        fields = ['name', 'color']
