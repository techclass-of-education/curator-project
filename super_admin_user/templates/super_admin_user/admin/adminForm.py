# # forms.py
#
# from django import forms
# from super_admin_user.models import AdminUserList
#
# class AdminUserForm(forms.ModelForm):
#     class Meta:
#         model = AdminUserList
#         fields = ['org_id','name', 'email', 'password', 'username', 'logo', 'address', 'mobile', 'superadmin_id']
#         widgets = {
#             'password': forms.PasswordInput(),
#             'address': forms.Textarea(attrs={'rows': 4}),
#         }


from django import forms
from super_admin_user.models import AdminUserList

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = AdminUserList
        fields = ['org_id', 'name', 'email', 'password', 'username', 'logo', 'address', 'mobile', 'superadmin_id']
        widgets = {
            'org_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'superadmin_id': forms.Select(attrs={'class': 'form-control'}),
        }


