from django import forms
from django.core.exceptions import  ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range

class SendConversation(forms.Form):
    renew_date = forms.CharField(help_text="Testing this.")

    def clean_sent_data(self):
        message = self.cleaned_data['renew_date']
        #
        # #check date is not in past
        # if data < datetime.date.today():
        #     raise ValidationError(_('Invalid date - renewal in past'))
        #
        # #check date is in range librarian allowed to change (+4 weeks).
        # if data > datetime.date.today() + datetime.timedelta(weeks = 4):
        #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        #Remember to always return the cleaned data.
        return message
