from django.contrib import admin
from . models import (
		TotalSaving,
		IncomeType,
		Income,
		ExpenditureType,
		Expenditure,
		MoneyLended,
		MoneyBorrowed,
		BuyingItemType,
		BuyingItemList,
		TripPlannedList,
		IncomeFrequency,
		CurrentIncomeSource,
		PossibleIncomeSource,
	)


admin.site.register(TotalSaving)
admin.site.register(IncomeType)
admin.site.register(Income)
admin.site.register(ExpenditureType)
admin.site.register(Expenditure)
admin.site.register(MoneyLended)
admin.site.register(MoneyBorrowed)
admin.site.register(BuyingItemType)
admin.site.register(BuyingItemList)
admin.site.register(TripPlannedList)
admin.site.register(IncomeFrequency)
admin.site.register(CurrentIncomeSource)
admin.site.register(PossibleIncomeSource)

