# Generated by Django 3.1.7 on 2021-03-23 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuyingItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenditureType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MoneyBorrowed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_borrowed', models.DateField()),
                ('return_date', models.DateField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('returned', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MoneyLended',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_lended', models.DateField()),
                ('collection_date', models.DateField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('collected', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TotalSaving',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=1000, null=True)),
                ('in_cash', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('in_bank', models.DecimalField(decimal_places=2, max_digits=1000)),
            ],
        ),
        migrations.CreateModel(
            name='TripPlannedList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('reason', models.CharField(max_length=50)),
                ('trip_from', models.CharField(max_length=30)),
                ('trip_to', models.CharField(max_length=30)),
                ('expected_cost', models.DecimalField(decimal_places=2, max_digits=100)),
                ('actual_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('trip_type', models.CharField(choices=[('ADVANTURE', 'ADVANTURE'), ('HOME', 'HOME'), ('BUSINESS', 'BUSINESS'), ('FUNACTION', 'FUNACTION')], max_length=20)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], max_length=20)),
                ('date_status_changed', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PossibleIncomeSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('interval', models.DateField()),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('frequency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.incomefrequency')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('payment_mode', models.CharField(choices=[('CASH', 'CASH'), ('BANK', 'BANK')], max_length=20)),
                ('date', models.DateTimeField(auto_now=True)),
                ('income_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.incometype')),
            ],
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_mode', models.CharField(choices=[('CASH', 'CASH'), ('BANK', 'BANK')], max_length=20)),
                ('date', models.DateTimeField(auto_now=True)),
                ('expenditure_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.expendituretype')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentIncomeSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('interval', models.DateField()),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], max_length=30)),
                ('frequency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.incomefrequency')),
            ],
        ),
        migrations.CreateModel(
            name='BuyingItemList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('purpose', models.CharField(max_length=100)),
                ('expected_cost', models.DecimalField(decimal_places=2, max_digits=100)),
                ('actual_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('urgency', models.CharField(choices=[('URGENT', 'URGENT'), ('NESSASITY', 'NESSASITY'), ('WISH', 'WISH')], max_length=20)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], max_length=20)),
                ('date_status_changed', models.DateTimeField(blank=True, null=True)),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.buyingitemtype')),
            ],
        ),
    ]
