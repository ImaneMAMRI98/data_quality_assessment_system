from django import forms
from django.forms import ModelForm
from .models import Services,Int,Float,String,Date


#this
class ServiceForm(forms.ModelForm):
	
	class Meta:
		model = Services
		fields = ['nom', 'domaine', 'fichier']
		
#this
class IntForm(forms.ModelForm):
     class Meta:
        model= Int
        fields = ['IVal_Min','IVal_Max']
        exclude = ['MetaData']
        

#this
class FloatForm(forms.ModelForm):
    class Meta:
        model=Float
        fields =['FVal_Min','FVal_Max']
#this
class StringForm(forms.ModelForm):
    class Meta:
        model=String
        fields =['Expression_Reguliere','longeur_min','longeur_max']

class DateForm(forms.ModelForm):
    class Meta:
        model=Date
        fields =['format','date_min','date_max']



