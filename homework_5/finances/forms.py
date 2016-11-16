from datetime import date
from decimal import Decimal

from django import forms

from .models import Charge, Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "number"
        ]


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = [
            "value",
            "date"
        ]

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get('value')
        charge_date = cleaned_data.get('date')

        if value and charge_date:
            if Decimal.compare(Decimal(0), value) == Decimal('0'):
                self.add_error("value", "Charge can't be a zero value")
            if value < 0 and charge_date > date.today():
                self.add_error("date", "You can't set negative charge on future day")
            return cleaned_data