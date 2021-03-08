from django.contrib import admin
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


admin.site.register(TotalSaving)
admin.site.register(IncomeType)
admin.site.register(Income)
admin.site.register(ExpenditureType)
admin.site.register(Expenditure)
admin.site.register(ToPay)
admin.site.register(YouLended)
admin.site.register(BuyingItemType)
admin.site.register(BuyingItemList)
admin.site.register(TripPlannedList)
admin.site.register(IncomeFrequency)
admin.site.register(CurrentIncomeSource)
admin.site.register(PossibleIncomeSource)

