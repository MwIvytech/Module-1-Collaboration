from django.db import models
from datetime import timedelta

class Income(models.Model):
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Biweekly'),
        ('monthly', 'Monthly'),
    ]

    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='monthly')
    next_disbursement = models.DateField(null=True, blank=True)

    def following_disbursement(self):
        """Calculate the following disbursement date after the one stored."""
        if not self.next_disbursement:
            return None

        if self.frequency == 'weekly':
            return self.next_disbursement + timedelta(weeks=1)
        elif self.frequency == 'biweekly':
            return self.next_disbursement + timedelta(weeks=2)
        elif self.frequency == 'monthly':
            return self.next_disbursement + relativedelta(months=1)
        return None


class Bill(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_day = models.PositiveSmallIntegerField()  # 1–31

    def __str__(self):
        return f"{self.name}: {self.amount} (due day {self.due_day})"


class Spending(models.Model):
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category}: {self.amount}"
