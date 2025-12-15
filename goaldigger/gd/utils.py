from .models import Income, Bill, Spending
from datetime import date

def calculate_monthly_income():
    total = 0
    for i in Income.objects.all():
        if i.frequency == 'weekly':
            total += i.amount * 4  # approx 4 weeks in a month
        elif i.frequency == 'biweekly':
            total += i.amount * 2  # approx 2 pay periods in a month
        elif i.frequency == 'monthly':
            total += i.amount
    return total

def calculate_leftover():
    total_income = calculate_monthly_income()
    total_bills = sum(b.amount for b in Bill.objects.all())
    total_spending = sum(s.amount for s in Spending.objects.all())
    return total_income - (total_bills + total_spending)



def calculate_remaining_until_next_disbursement():
    today = date.today()
    upcoming_incomes = [i for i in Income.objects.all() if i.next_disbursement]

    if not upcoming_incomes:
        return None

    # Find the soonest upcoming disbursement
    next_income = min(upcoming_incomes, key=lambda x: x.next_disbursement)

    # If the disbursement is today → treat income as received, then move to following
    if next_income.next_disbursement == today and next_income.following_disbursement():
        # Add today's income to leftover
        income_received = next_income.amount

        # Bills due before following disbursement
        next_date = next_income.following_disbursement()
        bills_due = sum(
            b.amount for b in Bill.objects.all()
            if b.due_day and b.due_day <= next_date.day
        )
        spending = sum(s.amount for s in Spending.objects.all())

        leftover = income_received - (bills_due + spending)

        return {
            "leftover": leftover,
            "next_date": next_date,
            "days_until": (next_date - today).days,
            "source": next_income.source,
            "frequency": next_income.get_frequency_display(),
        }

    # If the disbursement is in the future → funds are 0 until then
    if next_income.next_disbursement > today:
        bills_due = sum(
            b.amount for b in Bill.objects.all()
            if b.due_day and b.due_day <= next_income.next_disbursement.day
        )
        spending = sum(s.amount for s in Spending.objects.all())
        leftover = 0 - (bills_due + spending)

        return {
            "leftover": leftover,
            "next_date": next_income.next_disbursement,
            "days_until": (next_income.next_disbursement - today).days,
            "source": next_income.source,
            "frequency": next_income.get_frequency_display(),
        }