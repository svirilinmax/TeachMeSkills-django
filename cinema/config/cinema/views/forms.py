from datetime import datetime

from django import forms
from django.utils import timezone


class ScheduleFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search")
    genre = forms.CharField(required=False, label="Genre")
    date_from = forms.DateField(
        required=False,
        label="From date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        required=False, label="To date", widget=forms.DateInput(attrs={"type": "date"})
    )
    price_min = forms.DecimalField(
        required=False, label="Min price", min_value=0, decimal_places=2
    )
    price_max = forms.DecimalField(
        required=False, label="Max price", min_value=0, decimal_places=2
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
        price_min = cleaned_data.get("price_min")
        price_max = cleaned_data.get("price_max")

        # Date validation
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("Date from cannot be after date to")

        # Price validation
        if price_min and price_max and price_min > price_max:
            raise forms.ValidationError("Min price cannot be greater than max price")

        return cleaned_data

    def get_date_range(self):
        """Возвращает отфильтрованные даты с учетом timezone"""
        date_from = self.cleaned_data.get("date_from")
        date_to = self.cleaned_data.get("date_to")

        date_range = {}

        if date_from:
            start = timezone.make_aware(
                datetime.combine(date_from, datetime.min.time()),
                timezone.get_current_timezone(),
            )
            date_range["movie_start__gte"] = start

        if date_to:
            end = timezone.make_aware(
                datetime.combine(date_to, datetime.max.time().replace(microsecond=0)),
                timezone.get_current_timezone(),
            )
            date_range["movie_start__lte"] = end

        return date_range

    def is_filtered(self):
        return any(
            [
                self.data.get("q"),
                self.data.get("genre"),
                self.data.get("date_from"),
                self.data.get("date_to"),
                self.data.get("price_min"),
                self.data.get("price_max"),
            ]
        )
