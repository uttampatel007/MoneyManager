from django.db import models
from django.utils import timezone
from django.db.models import DEFERRED
from user_profile.models import User

 

class TotalSaving(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	total_amount = models.DecimalField(max_digits=1000,decimal_places=2, blank=True, null=True)
	in_cash = models.DecimalField(max_digits=1000,decimal_places=2)
	in_bank = models.DecimalField(max_digits=1000,decimal_places=2)


PYMENT_MODE = [
	('CASH','CASH'),
	('BANK','BANK'),
]


class IncomeType(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name


class Income(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	source = models.CharField(max_length=30)
	income_type = models.ForeignKey(IncomeType, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=100, decimal_places=2)
	payment_mode = models.CharField(choices=PYMENT_MODE, max_length=20)
	date = models.DateTimeField(auto_now=True)


class ExpenditureType(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Expenditure(models.Model):
	purpose = models.CharField(max_length=50)
	expenditure_type = models.ForeignKey(ExpenditureType, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10,decimal_places=2)
	payment_mode = models.CharField(choices=PYMENT_MODE, max_length=20)
	date = models.DateTimeField(auto_now=True)


class MoneyBorrowed(models.Model):
	person_name = models.CharField(max_length=50)
	reason = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=10,decimal_places=2)
	date_borrowed = models.DateField()
	return_date = models.DateField()
	created = models.DateTimeField(auto_now=True)
	returned = models.BooleanField(default=False, blank=True)


class MoneyLended(models.Model):
	person_name = models.CharField(max_length=50)
	reason = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=10,decimal_places=2)
	date_lended = models.DateField()
	collection_date = models.DateField()
	created = models.DateTimeField(auto_now=True)
	collected = models.BooleanField(default=False, blank=True)
	

class BuyingItemType(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


URGENCY = [
	('URGENT','URGENT'),
	('NESSASITY','NESSASITY'),
	('WISH','WISH'),
]


STATUS = [
	('ACTIVE','ACTIVE'),
	('COMPLETED','COMPLETED'),
	('CANCELLED','CANCELLED')
]


class BuyingItemList(models.Model):
	name = models.CharField(max_length=50)
	purpose = models.CharField(max_length=100)
	expected_cost = models.DecimalField(max_digits=100, decimal_places=2)
	actual_cost = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
	item_type = models.ForeignKey(BuyingItemType, on_delete=models.CASCADE)
	urgency = models.CharField(choices=URGENCY, max_length=20)
	date_added = models.DateTimeField(auto_now=True)
	status = models.CharField(choices=STATUS, max_length=20)
	date_status_changed = models.DateTimeField(blank=True, null=True)

	@classmethod
	def from_db(cls, db, field_names, values):
	    # Default implementation of from_db() (subject to change and could
	    # be replaced with super()).
	    if len(values) != len(cls._meta.concrete_fields):
	        values = list(values)
	        values.reverse()
	        values = [
	            values.pop() if f.attname in field_names else DEFERRED
	            for f in cls._meta.concrete_fields
	        ]
	    instance = cls(*values)
	    instance._state.adding = False
	    instance._state.db = db
	    # customization to store the original field values on the instance
	    instance._loaded_values = dict(zip(field_names, values))
	    return instance

	def save(self, *args, **kwargs):
		if not self._state.adding and (self.status != self._loaded_values['status']):
			self.date_status_changed = timezone.now()
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name

TRIP_TYPE = [
	('ADVANTURE','ADVANTURE'),
	('HOME','HOME'),
	('BUSINESS','BUSINESS'),
	('FUNACTION','FUNACTION'),
]


class TripPlannedList(models.Model):
	name = models.CharField(max_length=20)
	reason = models.CharField(max_length=50)
	trip_from = models.CharField(max_length=30)
	trip_to = models.CharField(max_length=30)
	expected_cost = models.DecimalField(max_digits=100, decimal_places=2)
	actual_cost = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
	trip_type = models.CharField(choices=TRIP_TYPE, max_length=20)
	date_added = models.DateTimeField(auto_now=True)
	status = models.CharField(choices=STATUS, max_length=20)
	date_status_changed = models.DateTimeField(blank=True, null=True)


class IncomeFrequency(models.Model):
	name = models.CharField(max_length=20)


class CurrentIncomeSource(models.Model):
	name = models.CharField(max_length=30)
	amount = models.DecimalField(max_digits=1000, decimal_places=2)
	frequency = models.ForeignKey(IncomeFrequency, on_delete=models.CASCADE)
	interval = models.DateField()
	date_added = models.DateTimeField(auto_now=True)
	status = models.CharField(choices=STATUS, max_length=30)


class PossibleIncomeSource(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=1000, decimal_places=2)
	frequency = models.ForeignKey(IncomeFrequency, on_delete=models.CASCADE)
	interval = models.DateField()
	date_added = models.DateTimeField(auto_now=True)


# from django.db.models.signals import pre_save
# from django.dispatch import receiver


# @receiver(pre_save, sender=TotalSaving)
# def update_total_savings(sender, instance, **kwargs):
# 	print('signal')
# 	instance.total_amount = instance.in_cash + instance.in_bank