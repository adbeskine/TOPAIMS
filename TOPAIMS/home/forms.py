from django import forms
from .models import Jobs, Purchase_orders




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

class update_scheduled_item_date_form(forms.Form):
	update_date_1 = forms.DateField(widget = forms.SelectDateWidget(attrs={'id':'schedule_item_date_input_start'}))
	update_date_2 = forms.DateField(required=False, widget = forms.SelectDateWidget(attrs={'id':'schedule_item_date_input_finish'}))

class purchase_order_form(forms.Form):
	Supplier = forms.CharField()
	Supplier_ref = forms.CharField()
	order_no = forms.IntegerField(initial=Purchase_orders.objects.count()+1, disabled=True)

	item_1_description = forms.CharField(required=False)
	item_1_fullname = forms.CharField(required=False)
	item_1_price = forms.IntegerField(required=False)
	item_1_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_1_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_1_delivery_date = forms.DateField(required=False)
	item_1_quantity = forms.IntegerField(required=False)

	item_2_description = forms.CharField(required=False)
	item_2_fullname = forms.CharField(required=False)
	item_2_price = forms.IntegerField(required=False)
	item_2_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_2_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_2_delivery_date = forms.DateField(required=False)
	item_2_quantity = forms.IntegerField(required=False)

	item_3_description = forms.CharField(required=False)
	item_3_fullname = forms.CharField(required=False)
	item_3_price = forms.IntegerField(required=False)
	item_3_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_3_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_3_delivery_date = forms.DateField(required=False)
	item_3_quantity = forms.IntegerField(required=False)

	item_4_description = forms.CharField(required=False)
	item_4_fullname = forms.CharField(required=False)
	item_4_price = forms.IntegerField(required=False)
	item_4_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_4_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_4_delivery_date = forms.DateField(required=False)
	item_4_quantity = forms.IntegerField(required=False)

	item_5_description = forms.CharField(required=False)
	item_5_fullname = forms.CharField(required=False)
	item_5_price = forms.IntegerField(required=False)
	item_5_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_5_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_5_delivery_date = forms.DateField(required=False)
	item_5_quantity = forms.IntegerField(required=False)

	item_6_description = forms.CharField(required=False)
	item_6_fullname = forms.CharField(required=False)
	item_6_price = forms.IntegerField(required=False)
	item_6_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_6_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_6_delivery_date = forms.DateField(required=False)
	item_6_quantity = forms.IntegerField(required=False)

	item_7_description = forms.CharField(required=False)
	item_7_fullname = forms.CharField(required=False)
	item_7_price = forms.IntegerField(required=False)
	item_7_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_7_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_7_delivery_date = forms.DateField(required=False)
	item_7_quantity = forms.IntegerField(required=False)

	item_8_description = forms.CharField(required=False)
	item_8_fullname = forms.CharField(required=False)
	item_8_price = forms.IntegerField(required=False)
	item_8_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_8_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_8_delivery_date = forms.DateField(required=False)
	item_8_quantity = forms.IntegerField(required=False)

	item_9_description = forms.CharField(required=False)
	item_9_fullname = forms.CharField(required=False)
	item_9_price = forms.IntegerField(required=False)
	item_9_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_9_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_9_delivery_date = forms.DateField(required=False)
	item_9_quantity = forms.IntegerField(required=False)

	item_10_description = forms.CharField(required=False)
	item_10_fullname = forms.CharField(required=False)
	item_10_price = forms.IntegerField(required=False)
	item_10_job = forms.ModelChoiceField(queryset=Jobs.objects.all(), to_field_name="address", required=False) # CHANGE LATER TO ONLY ACTIVE JOBS ON THIS
	item_10_delivery_location = forms.ChoiceField(choices=(('shop', 'shop'),('site', 'site')), required=False) # make it a radio widget, see docs on widgets
	item_10_delivery_date = forms.DateField(required=False)
	item_10_quantity = forms.IntegerField(required=False)


