from django import forms

class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
        ('UPI', 'UPI'),
    ]
    payment_method = forms.ChoiceField(choices = PAYMENT_CHOICES, widget=forms.RadioSelect)
