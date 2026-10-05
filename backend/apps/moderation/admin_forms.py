from django import forms


class ActionReasonForm(forms.Form):
    """Обязательная причина для любого действия модератора."""

    reason = forms.CharField(widget=forms.Textarea, min_length=5)
