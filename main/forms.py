from . models import Income, Expenditure, MoneyBorrowed, MoneyLended, BuyingItemList
from .widgets import FengyuanChenDatePickerInput
from django import forms


class IncomeForm(forms.ModelForm):
	class Meta:
		model = Income
		fields = '__all__'


class ExpenditureForm(forms.ModelForm):
	class Meta:
		model = Expenditure
		fields = '__all__'


class MoneyLendedForm(forms.ModelForm):
	date_lended = forms.DateField(input_formats=['%d/%m/%Y'], widget=FengyuanChenDatePickerInput())
	collection_date = forms.DateField(input_formats=['%d/%m/%Y'], widget=FengyuanChenDatePickerInput())
	class Meta:
		model = MoneyLended
		fields = '__all__'


class MoneyBorrowedForm(forms.ModelForm):
	date_borrowed = forms.DateField(input_formats=['%d/%m/%Y'], widget=FengyuanChenDatePickerInput())
	return_date = forms.DateField(input_formats=['%d/%m/%Y'], widget=FengyuanChenDatePickerInput())
	class Meta:
		model = MoneyBorrowed
		fields = '__all__'


class BuyingItemListForm(forms.ModelForm):
	class Meta:
		model = BuyingItemList
		exclude = ('date_status_changed',)

