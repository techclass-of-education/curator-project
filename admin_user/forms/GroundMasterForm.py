from django import forms
from django.db import connection

class GroundMasterForm(forms.Form):
    org_id = forms.CharField(max_length=255)
    ground_name = forms.CharField(max_length=255)
    state_name = forms.ChoiceField(choices=[], required=True)
    state_code = forms.CharField(widget=forms.HiddenInput(), required=False)
    city_name = forms.ChoiceField(choices=[], required=False)
    count_main_pitches = forms.IntegerField()
    count_practice_pitches = forms.IntegerField()
    is_side_screen = forms.BooleanField(required=False)
    count_placement_side_screen = forms.IntegerField(required=False)
    is_broadcasting_facility = forms.BooleanField(required=False)
    is_irrigation_pitches = forms.BooleanField(required=False)
    count_hydrants = forms.IntegerField(required=False)
    count_pumps = forms.IntegerField(required=False)
    count_showers = forms.IntegerField(required=False)
    is_lawn_nursary = forms.BooleanField(required=False)
    name_centre_square = forms.CharField(max_length=255, required=False)
    is_curator_room = forms.BooleanField(required=False)
    is_seperate_practice_area = forms.BooleanField(required=False)
    outfield = forms.CharField(max_length=255, required=False)
    profile_of_outfield = forms.CharField(max_length=255, required=False)
    lawn_species = forms.CharField(max_length=255, required=False)
    is_drainage_system_available = forms.BooleanField(required=False)
    is_water_drainage_system = forms.BooleanField(required=False)
    is_irrigation_system_available = forms.BooleanField(required=False)
    is_availability_of_water = forms.BooleanField(required=False)
    is_water_source = forms.BooleanField(required=False)
    storage_capacity_in_litres = forms.IntegerField(required=False)
    count_pop_ups = forms.IntegerField(required=False)
    size_of_pumps = forms.CharField(max_length=255, required=False)
    is_automation_if_any = forms.BooleanField(required=False)
    is_ground_equipments = forms.BooleanField(required=False)
    is_maintenance_contract = forms.BooleanField(required=False)
    is_maintenance_agency = forms.BooleanField(required=False)
    boundary_size_mtrs = forms.IntegerField(required=False)
    is_availability_of_mot = forms.BooleanField(required=False)
    is_machine_shed = forms.BooleanField(required=False)
    is_soil_shed = forms.BooleanField(required=False)
    is_pitch_or_run_up_covers = forms.BooleanField(required=False)
    size_of_covers_in_mtrs = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GroundMasterForm, self).__init__(*args, **kwargs)
        self.fields['state_name'].choices = [('','Select any state')] + self.get_states()
        if self.request.method == 'POST':
            self.fields['city_name'].choices = self.get_cities(self.request.POST.get('state_name'))

    def get_states(self):
        org_id = self.request.session.get('org_id')
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT id, state, state_code FROM {org_id}_state_master')
            states = cursor.fetchall()
        return [(state[0], state[1]) for state in states]

    def get_cities(self, state_id):
        org_id = self.request.session.get('org_id')
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT id, city_name FROM {org_id}_city_master WHERE state_id = %s', [state_id])
            cities = cursor.fetchall()
        return [(city[0], city[1]) for city in cities]