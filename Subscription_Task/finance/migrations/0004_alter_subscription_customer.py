# Generated by Django 4.1.7 on 2023-03-03 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_alter_subscription_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.customer'),
        ),
    ]
