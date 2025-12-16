from django.shortcuts import render, redirect
from .models import Income, Bill, Spending
from .utils import calculate_leftover, calculate_remaining_until_next_disbursement
from .forms import IncomeForm, BillForm, SpendingForm


def home(request):
    return render(request, "gd/home.html")


def dashboard(request):
    leftover = calculate_leftover()
    remaining_info = calculate_remaining_until_next_disbursement()
    total_income = sum(i.amount for i in Income.objects.all())
    total_bills = sum(b.amount for b in Bill.objects.all())
    total_spending = sum(s.amount for s in Spending.objects.all())

    if request.method == "POST":
        if "income_submit" in request.POST:
            form = IncomeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("dashboard")
        elif "bill_submit" in request.POST:
            form = BillForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("dashboard")
        elif "spending_submit" in request.POST:
            form = SpendingForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("dashboard")
        elif "clear_all" in request.POST:
            Income.objects.all().delete()
            Bill.objects.all().delete()
            Spending.objects.all().delete()
            return redirect("dashboard")

    context = {
        "income": Income.objects.all(),
        "bills": Bill.objects.all(),
        "spending": Spending.objects.all(),
        "leftover": leftover,
        "remaining_info": remaining_info,
        "total_income": total_income,
        "total_bills": total_bills,
        "total_spending": total_spending,
        "income_form": IncomeForm(),
        "bill_form": BillForm(),
        "spending_form": SpendingForm(),
    }
    return render(request, "gd/dashboard.html", context)
