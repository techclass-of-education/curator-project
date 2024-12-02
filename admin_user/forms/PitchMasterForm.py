from django import forms

class PitchMasterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pitches = kwargs.pop('pitches')
        super(PitchMasterForm, self).__init__(*args, **kwargs)
        for pitch in pitches:
            pitch_id = pitch[0]
            self.fields[f'pitch_no_{pitch_id}'] = forms.CharField(initial=pitch[3], required=True)
            self.fields[f'pitch_type_{pitch_id}'] = forms.CharField(initial=pitch[4], required=False)
            self.fields[f'profile_of_pitches_{pitch_id}'] = forms.CharField(initial=pitch[5], required=False)
            self.fields[f'last_used_date_{pitch_id}'] = forms.DateField(initial=pitch[6], required=False)
            self.fields[f'last_used_match_{pitch_id}'] = forms.CharField(initial=pitch[7], required=False)
            self.fields[f'is_uniformtiy_of_grass_{pitch_id}'] = forms.BooleanField(initial=pitch[8], required=False)
            self.fields[f'size_of_grass_{pitch_id}'] = forms.CharField(initial=pitch[9], required=False)
            self.fields[f'mowing_last_date_{pitch_id}'] = forms.DateField(initial=pitch[10], required=False)
            self.fields[f'mowing_size_{pitch_id}'] = forms.CharField(initial=pitch[11], required=False)
            self.fields[f'start_date_of_pitch_preparation_{pitch_id}'] = forms.DateField(initial=pitch[12], required=False)
            self.fields[f'soil_type_{pitch_id}'] = forms.CharField(initial=pitch[13], required=False)
