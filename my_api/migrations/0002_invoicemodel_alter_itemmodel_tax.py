# Generated by Django 4.0 on 2022-01-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.FileField(upload_to='invoices')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='tax',
            field=models.IntegerField(choices=[(0, '0%'), (1, '1%'), (5, '5%'), (10, '10%')]),
        ),
    ]
