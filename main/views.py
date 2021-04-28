from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from . models import (
		TotalSaving,
		IncomeType,
		Income,
		ExpenditureType,
		Expenditure,
		MoneyBorrowed,
		MoneyLended,
		BuyingItemType,
		BuyingItemList,
		TripPlannedList,
		IncomeFrequency,
		CurrentIncomeSource,
		PossibleIncomeSource,
	)
from . forms import IncomeForm, ExpenditureForm, MoneyLendedForm, MoneyBorrowedForm, BuyingItemListForm, TripPlannedListForm
from user_profile.models import User


@login_required
def index(request):
	user = User.objects.get(username=request.user)
	amount = TotalSaving.objects.filter(user=user).last()
	return render(request, 'main/index.html',{'amount':amount})

@login_required
def income(request):
	if request.method == 'POST':
		form = IncomeForm(request.POST or None)
		if form.is_valid():
			income_amount = form.cleaned_data['amount']
			income_mode = form.cleaned_data['payment_mode']

			total_saving = TotalSaving.objects.filter(user=request.user).last()
			if total_saving:
				new_total = total_saving.total_amount + income_amount
			else:
				TotalSaving.objects.create(total_amount=0, in_cash=0, in_bank=0,user=request.user)
				total_saving = TotalSaving.objects.filter(user=request.user).last()
				new_total = total_saving.total_amount + income_amount


			if income_mode == 'CASH':
				new_cash = total_saving.in_cash + income_amount
				obj = TotalSaving.objects.create(total_amount=new_total, in_cash=new_cash, in_bank=total_saving.in_bank,user=request.user)
			elif income_mode == 'BANK':
				new_bank = total_saving.in_bank + income_amount
				obj = TotalSaving.objects.create(total_amount=new_total, in_cash=total_saving.in_cash, in_bank=new_bank,user=request.user)
			else:
				pass

			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()

	incomes = Income.objects.filter(user=request.user).order_by('-pk')
	total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))
	total_income = total_income.get('amount__sum')
	form = IncomeForm()
	return render(request, 'main/income.html', {'incomes':incomes,'form':form, 'total_income':total_income})

@login_required
def income_update(request,pk):
	obj = get_object_or_404(Income, id=pk)
	if obj.user == request.user:
		form = IncomeForm(request.POST or None, instance=obj)
	else:
		message = 'You are not authorized to access this page!'
		return render(request, "main/update_income.html",{'message':message})
	old_amount = obj.amount
	old_payment_mode = obj.payment_mode
	

	if form.is_valid():
		new_amount = form.cleaned_data['amount']
		new_payment_mode = form.cleaned_data['payment_mode']


		if old_payment_mode != new_payment_mode:
			if new_amount == old_amount:
				savings =  TotalSaving.objects.filter(user=request.user).last()
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
			savings = TotalSaving.objects.filter(user=request.user).last()
			total_amount = savings.total_amount - old_amount

			if old_payment_mode == 'CASH':
				in_cash = savings.in_cash - old_amount
				TotalSaving.objects.filter(id=savings.id, user=request.user).update(in_cash=in_cash, total_amount=total_amount, user=request.user)

			if old_payment_mode == 'BANK':
				in_bank = savings.in_bank - old_amount
				TotalSaving.objects.filter(id=savings.id, user=request.user).update(in_bank=in_bank, total_amount=total_amount, user=request.user)

			savings = TotalSaving.objects.filter(user=request.user).last()

			if new_payment_mode == 'CASH':
				total_amount = savings.total_amount + new_amount
				in_cash = savings.in_cash + new_amount
				TotalSaving.objects.filter(id=savings.id, user=request.user).update(in_cash=in_cash, total_amount=total_amount, user=request.user)
				
			if new_payment_mode == 'BANK':
				total_amount = savings.total_amount + new_amount
				in_bank = savings.in_bank + new_amount
				TotalSaving.objects.filter(id=savings.id, user=request.user).update(in_bank=in_bank, total_amount=total_amount, user=request.user)

		form.save()
		return redirect('/income/')
	return render(request, "main/update_income.html",{'form':form})

@login_required
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

	total_expenditure = Expenditure.objects.aggregate(Sum('amount'))
	total_expenditure = total_expenditure.get('amount__sum')
	expenditures = Expenditure.objects.all().order_by('-pk')
	form = ExpenditureForm()
	return render(request, 'main/expenditure.html', {'expenditures':expenditures,'total_expenditure':total_expenditure,'form':form})

@login_required
def expenditure_update(request, pk):
	obj = get_object_or_404(Expenditure, id=pk)
	form = ExpenditureForm(request.POST or None, instance=obj)

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
					savings.in_bank = savings.in_bank + new_amount
					savings.in_cash = savings.in_cash - new_amount
				elif new_payment_mode == 'BANK':
					savings.in_cash = savings.in_cash + new_amount
					savings.in_bank = savings.in_bank - new_amount
				else:
					pass
				savings.save()

		if new_amount != old_amount:
			savings = TotalSaving.objects.last()
			total_amount = savings.total_amount + old_amount
			if old_payment_mode == 'CASH':
				in_cash = savings.in_cash + old_amount
				TotalSaving.objects.filter(id=savings.id).update(in_cash=in_cash, total_amount=total_amount)

			if old_payment_mode == 'BANK':
				in_bank = savings.in_bank + old_amount
				TotalSaving.objects.filter(id=savings.id).update(in_bank=in_bank, total_amount=total_amount)

			savings = TotalSaving.objects.last()
			if new_payment_mode == 'CASH':
				total_amount = savings.total_amount - new_amount
				in_cash = savings.in_cash - new_amount
				TotalSaving.objects.filter(id=savings.id).update(in_cash=in_cash, total_amount=total_amount)

			if new_payment_mode == 'BANK':
				total_amount = savings.total_amount - new_amount
				in_bank = savings.in_bank - new_amount
				TotalSaving.objects.filter(id=savings.id).update(in_bank=in_bank, total_amount=total_amount)

		form.save()
		return redirect('/expenditure/')
	return render(request, "main/update_expenditure.html",{'form':form})

@login_required
def money_lended(request):
	if request.method == "POST":
		form = MoneyLendedForm(request.POST or None)
		if form.is_valid():
			form.save()

	money_lended = MoneyLended.objects.all()
	total_money_lended = MoneyLended.objects.filter(collected=False).aggregate(Sum('amount'))
	total_money_lended = total_money_lended.get('amount__sum')
	if total_money_lended == None:
		total_money_lended = 0
	form = MoneyLendedForm()
	return render(request, 'main/money_lended.html', {'money_lended':money_lended, 'total_money_lended':total_money_lended, 'form':form})

@login_required
def money_lended_update(request,pk):
	obj = get_object_or_404(MoneyLended, id=pk)
	form = MoneyLendedForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		return redirect('/money-lended/')
	return render(request, 'main/money_lended_update.html',{'form':form})

@login_required
def money_borrowed(request):
	if request.method == 'POST':
		form = MoneyBorrowedForm(request.POST or None)
		if form.is_valid():
			form.save()
	money_borrowed = MoneyBorrowed.objects.all()
	total_money_borrowed = MoneyBorrowed.objects.filter(returned=False).aggregate(Sum('amount'))
	total_money_borrowed = total_money_borrowed.get('amount__sum')
	if total_money_borrowed == None:
		total_money_borrowed = 0
	form = MoneyBorrowedForm()
	return render(request, 'main/money_borrowed.html', {'money_borrowed':money_borrowed,'total_money_borrowed':total_money_borrowed,'form':form})

@login_required
def money_borrowed_update(request, pk):
	obj = get_object_or_404(MoneyBorrowed, id=pk)
	form = MoneyBorrowedForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		return redirect('/money-borrowed/')
	return render(request, 'main/money_borrowed_update.html',{'form':form})

@login_required
def item_line(request):
	if request.method == 'POST':
		form = BuyingItemListForm(request.POST or None)
		if form.is_valid():
			form.save()

	items = BuyingItemList.objects.all()
	form = BuyingItemListForm()
	return render(request, 'main/item_line.html',{'form':form, 'items':items})

@login_required
def item_line_update(request, pk):
	obj = get_object_or_404(BuyingItemList,id=pk)
	form = BuyingItemListForm(request.POST or None, instance=obj)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('/item-line/')
	return render(request, 'main/item_line_update.html',{'form':form})

@login_required
def trip_line(request):
	if request.method == 'POST':
		form = TripPlannedListForm(request.POST or None)
		if form.is_valid():
			form.save()

	trips = TripPlannedList.objects.all()
	form = TripPlannedListForm()
	return render(request, 'main/trip_line.html',{'form':form,'trips':trips})

@login_required
def trip_line_update(request,pk):
	obj = get_object_or_404(TripPlannedList,id=pk)
	form = TripPlannedListForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('/trip-line/')
	return render(request, 'main/trip_line_update.html',{'form':form})

@login_required
def income_source(request):
	return render(request, 'main/income_source.html')