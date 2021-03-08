from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from . models import (
		TotalSaving,
		IncomeType,
		Income,
		ExpenditureType,
		Expenditure,
		ToPay,
		YouLended,
		BuyingItemType,
		BuyingItemList,
		TripPlannedList,
		IncomeFrequency,
		CurrentIncomeSource,
		PossibleIncomeSource,
	)
from . forms import IncomeForm, ExpenditureForm



def index(request):
	amount = TotalSaving.objects.last()
	return render(request, 'main/index.html',{'amount':amount})


def income(request):
	if request.method == 'POST':
		form = IncomeForm(request.POST or None)
		if form.is_valid():
			income_amount = form.cleaned_data['amount']
			income_mode = form.cleaned_data['payment_mode']
			total_saving = TotalSaving.objects.last()
			new_total = total_saving.total_amount + income_amount

			if income_mode == 'CASH':
				new_cash = total_saving.in_cash + income_amount
				obj = TotalSaving.objects.create(total_amount=new_total, in_cash=new_cash, in_bank=total_saving.in_bank)
			elif income_mode == 'BANK':
				new_bank = total_saving.in_bank + income_amount
				obj = TotalSaving.objects.create(total_amount=new_total, in_cash=total_saving.in_cash, in_bank=new_bank)
			else:
				pass
			form.save()

	incomes = Income.objects.all().order_by('-pk')
	form = IncomeForm()
	return render(request, 'main/income.html', {'incomes':incomes,'form':form})


def income_update(request,pk):
	obj = get_object_or_404(Income, id=pk)
	form = IncomeForm(request.POST or None, instance=obj)

	old_source = obj.source
	old_income_type = obj.income_type
	old_amount = obj.amount
	old_payment_mode = obj.payment_mode

	if form.is_valid():
		new_amount = form.cleaned_data['amount']
		new_payment_mode = form.cleaned_data['payment_mode']
		if old_payment_mode != new_payment_mode:
			if new_amount == old_amount:
				savings = TotalSaving.objects.last()
				obj.payment_mode = new_payment_mode
				if new_payment_mode == 'CASH':
					savings.in_bank = savings.in_bank - new_amount
					savings.in_cash = savings.in_cash + new_amount
				elif new_payment_mode == 'BANK':
					savings.in_cash = savings.in_cash - new_amount
					savings.in_bank = savings.in_bank + new_amount
				else:
					pass
				savings.save()

		if new_amount != old_amount:
			print('new_amount', new_amount)
			print('old_amount', old_amount)
			print('old_payment_mode',old_payment_mode)
			print('new_payment_mode',new_payment_mode)
			savings = TotalSaving.objects.last()
			total_amount = savings.total_amount - old_amount
			if old_payment_mode == 'CASH':
				in_cash = savings.in_cash - old_amount
				print('in_cash', in_cash)
				TotalSaving.objects.filter(id=savings.id).update(in_cash=in_cash, total_amount=total_amount)

			if old_payment_mode == 'BANK':
				in_bank = savings.in_bank - old_amount
				TotalSaving.objects.filter(id=savings.id).update(in_bank=in_bank, total_amount=total_amount)

			savings = TotalSaving.objects.last()
			if new_payment_mode == 'CASH':
				total_amount = savings.total_amount + new_amount
				in_cash = savings.in_cash + new_amount
				TotalSaving.objects.filter(id=savings.id).update(in_cash=in_cash, total_amount=total_amount)

			if new_payment_mode == 'BANK':
				total_amount = savings.total_amount + new_amount
				in_bank = savings.in_bank + new_amount
				TotalSaving.objects.filter(id=savings.id).update(in_bank=in_bank, total_amount=total_amount)


		# if old_amount != new_amount:
		# 	print('-------OLD AMOUNT IS NOT EQUAL TO NEW---------')
		# 	savings = TotalSaving.objects.last()
		# 	difference = new_amount - old_amount
		# 	print(difference)
		# 	if new_payment_mode == 'CASH':
		# 		print('Inside New payment_mode CASH')
		# 		print(new_payment_mode)
		# 		if difference > 0:
		# 			print('cash difference grater than 0 ( >0 )')
		# 			print('savings in cash:' ,savings.in_cash)
		# 			in_cash = savings.in_cash + difference
		# 			print('in_cash', in_cash)
		# 			print('total amount savings', savings.total_amount)
		# 			total_amount = savings.total_amount + difference
		# 			print('total_amount', total_amount)
		# 			TotalSaving.objects.filter(id=savings.id).update(in_cash=in_cash, total_amount=total_amount)

		# 		if difference < 0:
		# 			print('cash difference less than 0 ( <0 )')
		# 			print('savings in cash:' ,savings.in_cash)
		# 			in_cash = savings.in_cash + difference
		# 			print('in_cash', in_cash)
		# 			print('total amount savings', savings.total_amount)
		# 			total_amount = savings.total_amount + difference
		# 			print('total_amount', total_amount)
		# 			TotalSaving.objects.filter(id=savings.id).update(in_cash=in_cash, total_amount=total_amount)

		# 	elif new_payment_mode == 'BANK':
		# 		print('Inside New payment_mode BANK')
		# 		print(new_payment_mode)
		# 		if difference > 0:
		# 			print('Bank difference grater than 0 ( >0 )')
		# 			print('savings in bank:' ,savings.in_bank)
		# 			in_bank = savings.in_bank + difference
		# 			print('in_bank', in_bank)
		# 			print('total amount savings', savings.total_amount)
		# 			total_amount = savings.total_amount + difference
		# 			print('total_amount', total_amount)
		# 			TotalSaving.objects.filter(id=savings.id).update(in_bank=in_bank, total_amount=total_amount)
		# 		if difference < 0:
		# 			print('Bank difference less than 0 ( <0 )')
		# 			print('savings in bank:' ,savings.in_bank)
		# 			in_bank = savings.in_bank + difference
		# 			print('in_bank', in_bank)
		# 			print('total amount savings', savings.total_amount)
		# 			total_amount = savings.in_bank + difference
		# 			print('total_amount', total_amount)
		# 			TotalSaving.objects.filter(id=savings.id).update(in_bank=in_bank, total_amount=total_amount)
		
		form.save()
		return redirect('/income/')
	return render(request, "main/update_income.html",{'form':form})


def expenditure(request):
	if request.method == 'POST':
		form = ExpenditureForm(request.POST or None)
		if form.is_valid():
			expenditure_amount = form.cleaned_data['amount']
			expenditure_mode = form.cleaned_data['payment_mode']
			total_saving = TotalSaving.objects.last()
			new_total = total_saving.total_amount - expenditure_amount

			if expenditure_mode == 'CASH':
				new_cash = total_saving.in_cash - expenditure_amount
				obj = TotalSaving.objects.create(total_amount=new_total, in_cash=new_cash, in_bank=total_saving.in_bank)
			elif income_mode == 'BANK':
				new_bank = total_saving.in_bank - expenditure_amount
				obj = TotalSaving.objects.create(total_amount=new_total, in_cash=total_saving.in_cash, in_bank=new_bank)
			else:
				pass
			form.save()

	expenditures = Expenditure.objects.all().order_by('-pk')
	form = ExpenditureForm()
	return render(request, 'main/expenditure.html', {'expenditures':expenditures,'form':form})


def lend_and_borrow(request):
	return render(request, 'main/lend_and_borrow.html')

def item_line(request):
	return render(request, 'main/item_line.html')

def trip_line(request):
	return render(request, 'main/trip_line.html')

def income_source(request):
	return render(request, 'main/income_source.html')