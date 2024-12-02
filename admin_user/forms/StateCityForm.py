from django import forms
from django.db import connection

class StateCityForm(forms.Form):
    state = forms.CharField(max_length=255)
    state_code = forms.CharField(max_length=2)
    city_name = forms.CharField(max_length=255)
    state_id = forms.ChoiceField(choices=[], required=False)

    def __init__(self, request, *args, **kwargs):
        super(StateCityForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['state_id'].choices = self.get_states()

    def get_states(self):
        org_id = self.request.session.get('org_id')
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT id, state FROM {org_id}_state_master')
            states = cursor.fetchall()
        return [(state[0], state[1]) for state in states]
