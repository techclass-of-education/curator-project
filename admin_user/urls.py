from django.urls import path
from . import views


urlpatterns = [
path('', views.login, name='login'),  # Root URL
path('login', views.login, name='login_org'),  # Root URL
path('curator/login', views.curatorLogin, name='login_curator'),  # Root URL
path('groundman/login', views.groundmanLogin, name='login_groundman'),  # Root URL
path('scorer/login', views.scorerLogin, name='login_scorer'),  # Root URL
path('login_auth', views.login_auth, name='login_auth'),  # Root URL
path('login_auth_role', views.login_auth_role, name='login_auth_role'),  # Root URL
path('create_admin_user_role', views.create_admin_user_role, name='create_admin_user_role'),
path('admin_users_roles_list', views.admin_user_roles_list, name='admin_user_roles_list'),
path('admin_user_role_details/<int:admin_id>', views.admin_user_role_details, name='admin_user_role_details'),
path('orgdashboard', views.org_dashboard, name='org_dashboard'),  # Root URL
path('roledashboard', views.role_dashboard, name='role_dashboard'),  # Root URL
path('logout', views.logout_view, name='logout'),
path('add_state_city', views.add_state_city, name='add_state_city'),
path('list_state_city', views.list_state_city, name='list_state_city'),
path('create_ground_master/', views.create_ground_master, name='create_ground_master'),
path('update_ground_master/<int:ground_id>', views.update_ground_master, name='update_ground_master'),
path('delete_ground_master/<int:ground_id>', views.delete_ground_master, name='delete_ground_master'),
path('update_pitches/<int:ground_id>/', views.update_pitches, name='update_pitches'),
path('ground_list/', views.ground_list, name='ground_list'),
path('ground_pitches/<int:ground_id>', views.ground_pitches, name='ground_pitches'),
path('edit_pitch/<int:pitch_id>/<int:ground_id>', views.edit_pitch, name='edit_pitch'),
path('save_edit_pitch', views.save_edit_pitch, name='save_edit_pitch'),
path('get_cities/', views.get_cities, name='get_cities'),
path('curator_daily_recording_form/', views.curator_daily_recording_form, name='curator_daily_recording_form'),
path('update_daily/<int:daily_id>', views.update_daily, name='update_daily'),
path('delete_daily/<int:daily_id>', views.delete_daily, name='delete_daily'),
path('curator_daily_recording_list/', views.curator_daily_recording_list, name='curator_daily_recording_list'),
path('get_pitches/<str:ground_id>', views.get_pitches, name='get_pitches'),
path('get_pitch/<str:pitch_id>', views.get_pitch, name='get_pitch'),
path('get_all_pitches/', views.get_all_pitches, name='get_all_pitches'),
path('get_grounds/', views.get_grounds, name='get_grounds'),
path('machinery/', views.machinery_list, name='machinery_list'),
    path('machinery/insert/', views.insert_machinery, name='insert_machinery'),
    path('machinery/update/<str:machinery_id>', views.update_machinery, name='update_machinery'),
    path('machinery/<int:machinery_id>/', views.get_machinery_details, name='get_machinery_details'),
path('matches/', views.match_list, name='match_list'),        # URL to list all matches
    path('matches/insert/', views.insert_match, name='insert_match'),  # URL to insert a new match
    path('matches/update/<int:match_id>/', views.update_match, name='update_match'),  # URL to update a match
    path('add_score/<int:match_id>/', views.add_score, name='add_score'),
    path('save_scores/', views.save_scores, name='save_scores'),
    path('get_match_scores/<int:match_id>/', views.get_match_scores, name='get_match_scores'),
    path('match_scores_list/<int:match_id>', views.match_scores_list, name='match_scores_list'),
    path('delete_score/<int:score_id>/', views.delete_score, name='delete_score'),
    path('update_score/<int:score_id>/', views.update_score, name='update_score'),
path('api/machinery-data/', views.get_machinery_data, name='machinery_data'),
]


