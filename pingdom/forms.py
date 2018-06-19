from django import forms

MODE = (
    (0, "False"),
    (1, "True"),
)


class AddTest(forms.Form):
    sitename = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control input-s'}))
    url = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control input-s'}))
    auto_test_mode = forms.CharField(label="Set Auto Test Mode",
                                     widget=forms.Select(choices=MODE, attrs={'class': 'form-control input-s'}),
                                     required=True)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control input-s'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control input-s'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control input-s'}))


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control input-s'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control input-s'}))


class EditForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control input-s'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control input-s'}))
