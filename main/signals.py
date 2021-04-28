from django.db.models.signals import pre_save
from django.dispatch import receiver
from . models import TotalSaving, Income

@receiver(pre_save, sender=TotalSaving)
def update_total_savings(sender, instance, **kwargs):
	instance.total_amount = instance.in_cash + instance.in_bank

# @receiver(pre_save, sender=Income)
# def addition_in_total_savings(sender, instance, **kwargs):
# 	total_savings = TotalSaving.objects.get(id=1)
# 	if instance.payment_mode == 'CASH':
# 		new_in_cash = total_savings.in_cash+instance.amount
# 		new_total_amount = total_savings.total_amount+new_in_cash
# 		TotalSaving.objects.select_related().filter(id=1).update(in_cash=new_in_cash, total_amount=new_total_amount)
# 	elif instance.payment_mode == 'BANK':
# 		new_in_bank = total_savings.in_bank+instance.amount
# 		new_total_amount = total_savings.total_amount+new_in_bank
# 		TotalSaving.objects.select_related().filter(id=1).update(in_bank=new_in_bank, total_amount=new_total_amount)
# 	else:
# 		pass

# @receiver(pre_save, sender=Income)
# def addition_in_total_savings(sender, instance, **kwargs):
# 	total_savings = TotalSaving.objects.get(id=1)
# 	if instance.payment_mode == 'CASH':
# 		total_savings.in_cash = instance.amount+total_savings.in_cash
# 		total_savings.save()
# 	elif instance.payment_mode == 'BANK':
# 		total_savings.in_bank = instance.amount+total_savings.in_bank	
# 		total_savings.save()
# 	else:
# 		pass