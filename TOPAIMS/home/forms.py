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

class new_scheduled_item_form(forms.Form):
	description = forms.CharField(widget = forms.TextInput(attrs={'id':'schedule_item_name_input'}))
	date_1 = forms.DateField(widget = forms.SelectDateWidget(attrs={'id':'schedule_item_date_input_start'}))
	date_2 = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'schedule_item_date_input_finish'}))
	quantity = forms.IntegerField(widget = forms.NumberInput(attrs = {'id':'schedule_item_quantity_input'}))

