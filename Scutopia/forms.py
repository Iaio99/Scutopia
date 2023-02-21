from django.forms import CharField, ModelForm
from .models import Professors

class professor_form(ModelForm):
    class Meta:
        model = Professors
        fields = '__all__'