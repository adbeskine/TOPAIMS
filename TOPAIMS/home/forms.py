from django import forms

class new_job_form(forms.Form):
	Name = forms.CharField(widget = forms.TextInput(attrs={'id':'Name'}))
	Email = forms.CharField(widget = forms.TextInput(attrs={'id':'Email'}))
	Phone = forms.CharField(widget = forms.TextInput(attrs={'id':'Phone'}))
	Address = forms.CharField(widget = forms.TextInput(attrs={'id':'Address'}))
	Note = forms.CharField(widget = forms.TextInput(attrs={'id':'Note'}))

class new_note_form(forms.Form):
	Title = forms.CharField(widget = forms.TextInput(attrs={'id':'Title_input'}))
	Text = forms.CharField(widget = forms.TextInput(attrs={'id':'Note_input'}))


