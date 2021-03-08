from django.forms import ModelForm
from . models import Income, Expenditure


class IncomeForm(ModelForm):
	class Meta:
		model = Income
		fields = '__all__'

class ExpenditureForm(ModelForm):
	class Meta:
		model = Expenditure
		fields = '__all__'