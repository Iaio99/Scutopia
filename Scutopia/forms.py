from django.forms import ModelForm #CharField, ModelFom
from .models import Professors

class professor_form(ModelForm):
    class Meta:
        model = Professors
        fields = '__all__'