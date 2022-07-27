from django import forms


class WeatherForm(forms.Form):
    city = forms.CharField(max_length=50, required=True, label='',
                           widget=forms.TextInput(attrs={
                               'placeholder': 'Enter your city',
                               'style': 'width: 900px; height:50px;',
                               'class': 'form-control'
                           }))