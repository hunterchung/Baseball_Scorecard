from django.forms import ModelForm
from django import forms
from scorecard.models import *

# class Delete_bpd_form(forms.Form):
#     bpd_id_str = forms.CharField()
#     rand_str_str = forms.CharField()
#     
#     def clean(self):
#         cleaned_data = super(Delete_bpd_form, self).clean()
#         
#         if "bpd_id_str" in cleaned_data:
#             try:
#                 cleaned_data["bpd_ids"] = map(int, cleaned_data["bpd_id_str"].split(","))
#             except ValueError:
#                 raise forms.ValidationError("These ids do not look like id.")
#         if "rand_str_str" in cleaned_data:
#             cleaned_data["rand_strs"] = cleaned_data["rand_str_str"].split(",")
#             if any(map(lambda x: len(x)!=32, cleaned_data["rand_strs"])):
#                 raise forms.ValidationError("Random string is in incorrect format.")
#         if len(cleaned_data["rand_strs"])!=len(cleaned_data["bpd_ids"]):
#             raise forms.ValidationError("Ids and random strings are not match")
#         return cleaned_data

class Player_form(ModelForm):
    class Meta:
        model = Player
        exclude = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active', 'password')

class Game_form(ModelForm):
    class Meta:
        model = Game
        exclude = ('end_time')