from django import forms
from .models import Income, Bill, Spending

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'frequency', 'next_disbursement']


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name', 'amount', 'due_day']


class SpendingForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = ['item', 'amount', 'date']
