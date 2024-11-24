from django.contrib.admin import widgets
from django import forms


class AdminDateWidget(forms.DateInput):
    input_type = "date"

    class Media:
        css = {
            "all": [
                "date-time-picker/date-picker.css",
            ],
        }

    def format_value(self, value):
        return value

    def __init__(self, attrs=None, format=None):
        attrs = {"class": "vTextField date-widget", **(attrs or {})}
        super().__init__(attrs=attrs, format=format)


class AdminTimeWidget(forms.TimeInput):
    input_type = "time"

    class Media:
        css = {
            "all": [
                "date-time-picker/date-picker.css",
            ],
        }

    def __init__(self, attrs=None, format=None):
        attrs = {"class": "vTextField date-widget", **(attrs or {})}
        super().__init__(attrs=attrs, format=format)


class AdminSplitDateTime(widgets.AdminSplitDateTime):
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)
