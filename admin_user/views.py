import os.path
from builtins import print

from django.conf import settings
from django.db import connection, transaction
from django.shortcuts import render,redirect
from django.contrib import messages

from admin_user.forms.GroundMasterForm import GroundMasterForm
from admin_user.forms.PitchMasterForm import PitchMasterForm
from admin_user.forms.adminRoleForm import AdminUserRoleForm
from admin_user.forms.StateCityForm import StateCityForm
from admin_user.models import AdminRole
from super_admin_user.models import AdminUserList


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



def login(request):
    return render(request,'admin_user/org_login.html')

def curatorLogin(request):
    return render(request,'curator/org_login.html')

def groundmanLogin(request):
    return render(request,'groundman/org_login.html')

def scorerLogin(request):
    return render(request,'scorer/org_login.html')


def login_auth(request):
    if request.method == 'POST':
        org_id = request.POST['org_id']
        username = request.POST['username']
        password = request.POST['password']
        # print(org_id)
        try:
            user = AdminUserList.objects.get( org_id=org_id,username=username, password=password)
            if user is not None:
                request.session["org_id"]=user.org_id
                request.session["user_id"] = user.id
                # request.session["org_user"]=user
                return render(request,'admin_user/dashboard.html',{'user':user})
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'admin_user/org_login.html')
        except Exception as e:
            print(e)
            return render(request, 'admin_user/org_login.html')

def login_auth_role(request):

    if request.method == 'POST':
        org_id = request.POST['org_id']
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        try:
            user = AdminRole.objects.get( org_id=org_id,username=username, password=password,role=role)
            if user is not None:
                request.session["org_id"]=user.org_id
                profilePath = user.profileImage.url
                if(role=="Groundman"):
                    return render(request,'groundman/dashboard.html',{'user':user,'profilePath':profilePath})
                elif(role=="Curator"):
                    return render(request,'curator/dashboard.html',{'user':user,'profilePath':profilePath})
                elif(role=="Scorer"):
                    return render(request,'scorer/dashboard.html',{'user':user,'profilePath':profilePath})

            else:
                messages.error(request, 'Invalid username or password')
        except Exception as e:
            print(e)
            if (role == "Groundman"):
                return render(request, 'groundman/org_login.html')
            elif (role == "Curator"):
                return render(request, 'curator/org_login.html')
            elif (role == "Scorer"):
                return render(request, 'scorer/org_login.html')

def org_dashboard(request):
    user_id = request.session.get("user_id")  # Retrieve the stored ID from the session
    if user_id:
        try:
            user = AdminUserList.objects.get(id=user_id)  # Retrieve the user object from the database
            return render(request, 'admin_user/dashboard.html', {'user': user})
        except AdminUserList.DoesNotExist:
            org_user = None  # Handle the case where the user does not exist


def role_dashboard(request):
    return render(request,'admin_user/dashboard_role.html')

def logout_view(request):
    return redirect('login')

def add_state_city(request):
    org_id = request.session.get('org_id')
    if request.method == 'POST':
        try:
            state_name = request.POST['state'].split("-")[1].strip()
            state_code = request.POST['state-code']
            city_name = request.POST['city']
            with connection.cursor() as cursor:
                print("Method Post")
                cursor.execute(f'''INSERT INTO {org_id}_state_master (state, state_code) VALUES (%s, %s)''',
                               [state_name, state_code])

                cursor.execute(f'SELECT id FROM {org_id}_state_master WHERE state = %s', [state_name])
                state_id = cursor.fetchone()[0]

                # Insert city data
                cursor.execute(f'''INSERT INTO {org_id}_city_master (city_name, state_id) VALUES (%s, %s)''',
                               [city_name, state_id])

                return redirect('list_state_city')



        except Exception as e:
            print(e)
            # messages.error(request, e)
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT id FROM {org_id}_state_master WHERE state = %s', [state_name])
                state_id = cursor.fetchone()[0]

                # Insert city data
                cursor.execute(f'''INSERT INTO {org_id}_city_master (city_name, state_id) VALUES (%s, %s)''',
                               [city_name, state_id])

                return redirect('list_state_city')

        # Insert state data if not already present

    else:
        print("Method GET")
        return render(request, 'admin_user/masters/add_state_city.html')
        # form = StateCityForm(request)


def list_state_city(request):
    org_id = request.session.get('org_id')
    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT s.state, s.state_code, c.city_name
            FROM {org_id}_state_master s
            LEFT JOIN {org_id}_city_master c ON s.id = c.state_id
        ''')
        state_city_data = cursor.fetchall()

    return render(request, 'admin_user/masters/list_state_city.html', {'state_city_data': state_city_data})


def create_admin_user_role(request):

    try:
        if request.method == 'POST':
            form = AdminUserRoleForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    instance=form.save()
                    messages.success(request, 'Admin user created successfully')
                    # createAllMastersTables(instance)
                    return redirect('/usr_admin/admin_users_roles_list')  # Redirect to a view that lists admin users
                except Exception as e:
                    messages.error(request, e)
            else:
                messages.error(request, form.errors)
        else:
            form = AdminUserRoleForm(initial={'org_id':request.session["org_id"]})
        return render(request, 'admin_user/create_admin_role.html', {'form': form})
    except Exception as e:
        messages.error(request, e)
        print(e)

def admin_user_roles_list(request):
    org_id = request.session["org_id"]
    admin_roles = AdminRole.objects.filter(org_id=org_id)
    print(admin_roles)
    return render(request, 'admin_user/admin_users_roles_list.html', {'admin_roles': admin_roles})

def admin_user_role_details(request, admin_id):
    admin = AdminRole.objects.get(id=admin_id)
    profilePath=admin.profileImage.url
    # print(profilePath)
    return render(request, 'admin_user/admin_user_role_details.html', {'admin': admin,'profilePath':profilePath})

def create_ground_master(request):
    # if request.method == 'POST':
    #     org_id=request.session["org_id"]
    #     form = GroundMasterForm(request.POST,request=request)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         grdTableName=org_id+"_ground_master"
    #         pitchTableName=org_id+"_pitch_master"
    #
    #         print(data)
    #         with connection.cursor() as cursor:
    #             cursor.execute(f'''
    #                 INSERT INTO {grdTableName} (
    #                     org_id, ground_name, state_code, state_name, city_name,
    #                     count_main_pitches, count_practice_pitches, is_side_screen,
    #                     count_placement_side_screen, is_broadcasting_facility, is_irrigation_pitches,
    #                     count_hydrants, count_pumps, count_showers, is_lawn_nursary, name_centre_square,
    #                     is_curator_room, is_seperate_practice_area, outfield, profile_of_outfield,
    #                     lawn_species, is_drainage_system_available, is_water_drainage_system, is_irrigation_system_available,
    #                     is_availability_of_water, is_water_source, storage_capacity_in_litres, count_pop_ups,
    #                     size_of_pumps, is_automation_if_any, is_ground_equipments, is_maintenance_contract,
    #                     is_maintenance_agency, boundary_size_mtrs, is_availability_of_mot, is_machine_shed,
    #                     is_soil_shed, is_pitch_or_run_up_covers, size_of_covers_in_mtrs
    #                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    #             ''', (
    #                 data['org_id'], data['ground_name'], data['state_code'], data['state_name'], data['city_name'],
    #                 data['count_main_pitches'], data['count_practice_pitches'], data['is_side_screen'],
    #                 data['count_placement_side_screen'], data['is_broadcasting_facility'], data['is_irrigation_pitches'],
    #                 data['count_hydrants'], data['count_pumps'], data['count_showers'], data['is_lawn_nursary'], data['name_centre_square'],
    #                 data['is_curator_room'], data['is_seperate_practice_area'], data['outfield'], data['profile_of_outfield'],
    #                 data['lawn_species'], data['is_drainage_system_available'], data['is_water_drainage_system'], data['is_irrigation_system_available'],
    #                 data['is_availability_of_water'], data['is_water_source'], data['storage_capacity_in_litres'], data['count_pop_ups'],
    #                 data['size_of_pumps'], data['is_automation_if_any'], data['is_ground_equipments'], data['is_maintenance_contract'],
    #                 data['is_maintenance_agency'], data['boundary_size_mtrs'], data['is_availability_of_mot'], data['is_machine_shed'],
    #                 data['is_soil_shed'], data['is_pitch_or_run_up_covers'], data['size_of_covers_in_mtrs']
    #             ))
    #             ground_id = cursor.lastrowid
    #
    #             total_pitches = data['count_main_pitches'] + data['count_practice_pitches']
    #             for pitch_no in range(1, total_pitches + 1):
    #                 cursor.execute(f'''
    #                     INSERT INTO {pitchTableName} (
    #                         org_id, ground_id, pitch_no
    #                     ) VALUES (%s, %s, %s)
    #                 ''', (data['org_id'], ground_id, "p"+str(pitch_no)))
    #
    #         return redirect(f'update_pitches/{ground_id}')
    # else:
    #     form = GroundMasterForm(initial={'org_id':request.session["org_id"]},request=request)
    # return render(request, 'admin_user/create_ground_master.html', {'form': form})
        org_id = request.session["org_id"]
        if request.method == "POST":
            org_id = request.POST['org_id']
            google_location = request.POST['google_location']
            year_of_construction = request.POST['year_of_construction']
            phone_numbers = request.POST['phone_numbers']
            slop_ratio = request.POST['slop_ratio']
            ground_name = request.POST['ground_name']
            state_code = request.POST['state_code']
            state_name = request.POST['state_name']
            city_name = request.POST['city_name']
            count_main_pitches = request.POST['count_main_pitches']
            count_practice_pitches = request.POST['count_practice_pitches']
            is_side_screen = request.POST.get('is_side_screen',False)
            print("is_side_screen",is_side_screen)
            count_placement_side_screen = request.POST['count_placement_side_screen']
            is_broadcasting_facility = request.POST.get('is_broadcasting_facility', False)
            is_irrigation_pitches = request.POST.get('is_irrigation_pitches', False)
            count_hydrants = request.POST['count_hydrants']
            count_pumps = request.POST['count_pumps']
            count_showers = request.POST['count_showers']
            is_lawn_nursary = request.POST.get('is_lawn_nursary', False)
            name_centre_square = request.POST['name_centre_square']
            is_curator_room = request.POST.get('is_curator_room', False)
            is_seperate_practice_area = request.POST.get('is_seperate_practice_area', False)
            outfield = request.POST['outfield']
            profile_of_outfield = request.POST['profile_of_outfield']
            lawn_species = request.POST['lawn_species']
            is_drainage_system_available = request.POST.get('is_drainage_system_available', False)
            is_water_drainage_system = request.POST.get('is_water_drainage_system', False)
            is_irrigation_system_available = request.POST.get('is_irrigation_system_available', False)
            is_availability_of_water = request.POST.get('is_availability_of_water', False)
            is_water_source = request.POST.get('is_water_source', False)
            storage_capacity_in_litres = request.POST['storage_capacity_in_litres']
            count_pop_ups = request.POST['count_pop_ups']
            size_of_pumps = request.POST['size_of_pumps']
            is_automation_if_any = request.POST.get('is_automation_if_any', False)
            is_ground_equipments = request.POST.get('is_ground_equipments', False)
            is_maintenance_contract = request.POST.get('is_maintenance_contract', False)
            is_maintenance_agency = request.POST.get('is_maintenance_agency', False)
            boundary_size_mtrs = request.POST['boundary_size_mtrs']
            is_availability_of_mot = request.POST.get('is_availability_of_mot', False)
            is_machine_shed = request.POST.get('is_machine_shed', False)
            is_soil_shed = request.POST.get('is_soil_shed', False)
            is_pitch_or_run_up_covers = request.POST.get('is_pitch_or_run_up_covers', False)
            size_of_covers_in_mtrs = request.POST['size_of_covers_in_mtrs']

            with connection.cursor() as cursor:
                # Insert into Ground Master table
                cursor.execute(f'''
                            SELECT state, state_code
                            FROM {org_id}_state_master''')
                state_data = cursor.fetchall()
                cursor.execute(
                    f"""INSERT INTO {org_id}_ground_master (
                        org_id, google_location, year_of_construction ,phone_numbers ,slop_ratio, ground_name, state_code, state_name, city_name, count_main_pitches, count_practice_pitches, 
                        is_side_screen, count_placement_side_screen, is_broadcasting_facility, is_irrigation_pitches, count_hydrants, 
                        count_pumps, count_showers, is_lawn_nursary, name_centre_square, is_curator_room, is_seperate_practice_area, 
                        outfield, profile_of_outfield, lawn_species, is_drainage_system_available,
                           is_water_drainage_system
                          , 
                        is_irrigation_system_available, is_availability_of_water, water_source, storage_capacity_in_litres, 
                        count_pop_ups, size_of_pumps, is_automation_if_any, is_ground_equipments, is_maintenance_contract, 
                        is_maintenance_agency, boundary_size_mtrs, is_availability_of_mot, is_machine_shed, is_soil_shed, 
                        is_pitch_or_run_up_covers, size_of_covers_in_mtrs) 
                    VALUES (%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    [org_id, google_location,year_of_construction,phone_numbers,slop_ratio,ground_name, state_code, state_name, city_name, count_main_pitches, count_practice_pitches,
                     is_side_screen, count_placement_side_screen, is_broadcasting_facility, is_irrigation_pitches,
                     count_hydrants,
                     count_pumps, count_showers, is_lawn_nursary, name_centre_square, is_curator_room,
                     is_seperate_practice_area,
                     outfield, profile_of_outfield, lawn_species, is_drainage_system_available,
                     is_water_drainage_system,
                     is_irrigation_system_available, is_availability_of_water, is_water_source,
                     storage_capacity_in_litres,
                     count_pop_ups, size_of_pumps, is_automation_if_any, is_ground_equipments, is_maintenance_contract,
                     is_maintenance_agency, boundary_size_mtrs, is_availability_of_mot, is_machine_shed, is_soil_shed,
                     is_pitch_or_run_up_covers, size_of_covers_in_mtrs]
                )
                ground_id = cursor.lastrowid  # Get the ID of the newly inserted ground

                # Insert into Pitch Master table
                # total_pitches = int(count_main_pitches) + int(count_practice_pitches)
                i=1
                while(i<=int(count_main_pitches)):
                    cursor.execute(
                        f"INSERT INTO {org_id}_pitch_master (org_id, ground_id, pitch_no,pitch_type) VALUES (%s, %s, %s,%s)",
                        [org_id, ground_id, i,"main"]

                    )
                    i+=1

                i=1
                while(i<=int(count_practice_pitches)):
                    cursor.execute(
                        f"INSERT INTO {org_id}_pitch_master (org_id, ground_id, pitch_no,pitch_type) VALUES (%s, %s, %s,%s)",
                        [org_id, ground_id, i,"practice"]

                    )
                    i+=1
                # for i in range(1, total_pitches + 1):
                #     cursor.execute(
                #         f"INSERT INTO {org_id}_pitch_master (org_id, ground_id, pitch_no,pitch_type) VALUES (%s, %s, %s,%s)",
                #         [org_id, ground_id, i]
                #     )
            return redirect('ground_pitches',ground_id)
        with connection.cursor() as cursor:
                # Insert into Ground Master table
                cursor.execute(f'''
                            SELECT id,state, state_code
                            FROM {org_id}_state_master''')
                state_data = cursor.fetchall()
                print(state_data)
        return render(request, 'admin_user/create_ground_master.html',{'org_id':request.session["org_id"],'state_data':state_data})


def update_pitches(request, ground_id):
    org_id = request.session.get("org_id")
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {org_id}_ground_master WHERE id = %s', [ground_id])
        ground = cursor.fetchone()

        cursor.execute(f'SELECT * FROM {org_id}_pitch_master WHERE ground_id = %s', [ground_id])
        pitches = cursor.fetchall()

    if request.method == 'POST':
        form = PitchMasterForm(request.POST, pitches=pitches)
        if form.is_valid():
            with transaction.atomic():
                with connection.cursor() as cursor:
                    for pitch in pitches:
                        pitch_id = pitch[0]
                        pitch_data = {
                            'pitch_no': form.cleaned_data[f'pitch_no_{pitch_id}'],
                            'pitch_type': form.cleaned_data[f'pitch_type_{pitch_id}'],
                            'profile_of_pitches': form.cleaned_data[f'profile_of_pitches_{pitch_id}'],
                            'size_pitch_square': form.cleaned_data[f'size_pitch_square_{pitch_id}'],
                            'last_used_date': form.cleaned_data[f'last_used_date_{pitch_id}'],
                            'last_used_match': form.cleaned_data[f'last_used_match_{pitch_id}'],
                            'is_uniformtiy_of_grass': form.cleaned_data[f'is_uniformtiy_of_grass_{pitch_id}'],
                            'size_of_grass': form.cleaned_data[f'size_of_grass_{pitch_id}'],
                            'mowing_last_date': form.cleaned_data[f'mowing_last_date_{pitch_id}'],
                            'mowing_size': form.cleaned_data[f'mowing_size_{pitch_id}'],
                            'start_date_of_pitch_preparation': form.cleaned_data[
                                f'start_date_of_pitch_preparation_{pitch_id}'],
                            'date_of_pitch_construction': form.cleaned_data[
                                f'date_of_pitch_construction_{pitch_id}'],
                            'soil_type': form.cleaned_data[f'soil_type_{pitch_id}']
                        }
                        cursor.execute(f'''
                                UPDATE {org_id}_pitch_master SET
                                    pitch_no = %s, pitch_type = %s, profile_of_pitches = %s,size_pitch_square=%s, last_used_date = %s,
                                    last_used_match = %s, is_uniformtiy_of_grass = %s, size_of_grass = %s, mowing_last_date = %s,
                                    mowing_size = %s, start_date_of_pitch_preparation = %s,date_of_pitch_construction = %s, soil_type = %s
                                WHERE id = %s
                            ''', (
                            pitch_data['pitch_no'], pitch_data['pitch_type'], pitch_data['profile_of_pitches'],
                            pitch_data['size_pitch_square'],pitch_data['last_used_date'],
                            pitch_data['last_used_match'], pitch_data['is_uniformtiy_of_grass'],
                            pitch_data['size_of_grass'], pitch_data['mowing_last_date'],
                            pitch_data['mowing_size'], pitch_data['start_date_of_pitch_preparation'],
                            pitch_data['date_of_pitch_construction'],pitch_data['soil_type'], pitch_id
                        ))
            return redirect('ground_list')
    else:
        initial_data = {}
        for pitch in pitches:
            pitch_id = pitch[0]
            initial_data[f'pitch_no_{pitch_id}'] = pitch[3]
            initial_data[f'pitch_type_{pitch_id}'] = pitch[4]
            initial_data[f'profile_of_pitches_{pitch_id}'] = pitch[5]
            initial_data[f'size_pitch_square_{pitch_id}'] = pitch[17]
            initial_data[f'last_used_date_{pitch_id}'] = pitch[6]
            initial_data[f'last_used_match_{pitch_id}'] = pitch[7]
            initial_data[f'is_uniformtiy_of_grass_{pitch_id}'] = pitch[8]
            initial_data[f'size_of_grass_{pitch_id}'] = pitch[9]
            initial_data[f'mowing_last_date_{pitch_id}'] = pitch[10]
            initial_data[f'mowing_size_{pitch_id}'] = pitch[11]
            initial_data[f'start_date_of_pitch_preparation_{pitch_id}'] = pitch[12]
            initial_data[f'date_of_pitch_construction_{pitch_id}'] = pitch[16]
            initial_data[f'soil_type_{pitch_id}'] = pitch[13]
        form = PitchMasterForm(initial=initial_data, pitches=pitches)
        # print(form)
    # return render(request, 'update_pitches.html', {'form': form, 'ground': ground})

    return render(request, 'admin_user/update_pitches.html', {
        'form': form,
        'ground': {
            'id': ground[0],
            'name': ground[1],  # Assuming the second column is the ground name
        },
        'pitches': [{'id': pitch[0]} for pitch in pitches]

    })

def ground_list(request):
    org_id = request.session["org_id"]
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {org_id}_ground_master')
        grounds = cursor.fetchall()

    return render(request, 'admin_user/ground_list.html', {'grounds': grounds})

def ground_pitches(request,ground_id):
    org_id = request.session["org_id"]
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {org_id}_ground_master where id=%s',[ground_id])
        grounds = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(f'''SELECT * FROM {org_id}_pitch_master WHERE ground_id = %s''', [ground_id])
        pitches = cursor.fetchall()
    return render(request, 'admin_user/ground_pitches.html', {'pitches': pitches,'grounds':grounds})


def save_edit_pitch(request):
    org_id = request.session["org_id"]
    if request.method == "POST":
        pitch_ids = request.POST.get('pitch_id')
        ground_id = request.POST.get('ground_id')
        pitch_types = request.POST.get('pitch_type')
        size_pitch_square = request.POST.get('size_pitch_square')
        profile_of_pitches_list = request.POST.get('profile_of_pitches')
        last_used_dates = request.POST.get('last_used_date')
        last_used_matches = request.POST.get('last_used_match')
        is_uniformity_of_grasses = 1 if request.POST.get('is_uniformity_of_grass') else 0
        size_of_grasses = request.POST.get('size_of_grass')
        mowing_last_dates = request.POST.get('mowing_last_date')
        mowing_sizes = request.POST.get('mowing_size')
        start_dates_of_pitch_preparation = request.POST.get('start_date_of_pitch_preparation')
        date_pitch_construction = request.POST.get('date_pitch_construction')
        pitch_in_out = request.POST.get('pitch_in_out')
        pitch_placement = request.POST.get('pitch_placement')
        size_pitch = request.POST.get('size_pitch')
        soil_types = request.POST.get('soil_type')

        with connection.cursor() as cursor:
                cursor.execute(
                    f"""UPDATE {org_id}_pitch_master 
                    SET pitch_type=%s, profile_of_pitches=%s,size_pitch_square=%s, last_used_date=%s, last_used_match=%s, is_uniformtiy_of_grass=%s, 
                        size_of_grass=%s, mowing_last_date=%s, mowing_size=%s,date_pitch_construction=%s, start_date_of_pitch_preparation=%s, soil_type=%s,
                        pitch_in_out=%s,pitch_placement=%s,size_pitch=%s
                    WHERE id=%s and ground_id=%s""",
                    [pitch_types, profile_of_pitches_list,size_pitch_square, last_used_dates, last_used_matches,
                     is_uniformity_of_grasses,
                     size_of_grasses, mowing_last_dates, mowing_sizes,date_pitch_construction, start_dates_of_pitch_preparation,
                     soil_types,pitch_in_out,pitch_placement,size_pitch, pitch_ids,ground_id]
                )

        return redirect(f'/usr_admin/ground_pitches/{ground_id}')

def edit_pitch(request,pitch_id,ground_id):
    org_id = request.session["org_id"]
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {org_id}_pitch_master where id=%s',[pitch_id])
        pitch = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {org_id}_ground_master where id=%s',[ground_id])
        ground = cursor.fetchall()

        print(pitch)
        print(ground)
    return render(request, 'admin_user/edit_pitch.html', {'pitch': pitch[0],'ground':ground[0]})


def get_cities(request):
    org_id = request.session["org_id"]
    state_id = request.GET.get('state_id')
    with connection.cursor() as cursor:
        cursor.execute(f'''SELECT id, city_name FROM {org_id}_city_master WHERE state_id = %s''', [state_id])
        cities = cursor.fetchall()
    return JsonResponse({'cities': [{'id': city[0], 'name': city[1]} for city in cities]})


def get_grounds(request):
    org_id = request.session["org_id"]
    # state_id = request.GET.get('state_id')
    with connection.cursor() as cursor:
        cursor.execute(f'''SELECT * FROM {org_id}_ground_master WHERE org_id = %s''', [org_id])
        grounds = cursor.fetchall()
    return JsonResponse({'grounds': [{'ground': ground} for ground in grounds]})

def get_pitches(request,ground_id):
    org_id = request.session["org_id"]
    # ground_id = request.session["ground_id"]
    # state_id = request.GET.get('state_id')
    with connection.cursor() as cursor:
        cursor.execute(f'''SELECT * FROM {org_id}_pitch_master WHERE org_id = %s and ground_id=%s''', [org_id,ground_id])
        pitches = cursor.fetchall()
    return JsonResponse({'grounds': [{'pitch': pitch} for pitch in pitches]})

def get_pitch(request,pitch_id):
    org_id = request.session["org_id"]
    # ground_id = request.session["ground_id"]
    # state_id = request.GET.get('state_id')
    with connection.cursor() as cursor:
        cursor.execute(f'''SELECT * FROM {org_id}_pitch_master WHERE org_id = %s and id=%s''', [org_id,pitch_id])
        pitches = cursor.fetchall()
    return JsonResponse({'grounds': [{'pitch': pitch} for pitch in pitches]})




def get_all_pitches(request):
    org_id = request.session["org_id"]
    # ground_id = request.session["ground_id"]
    # state_id = request.GET.get('state_id')
    with connection.cursor() as cursor:
        cursor.execute(f'''SELECT * FROM {org_id}_pitch_master WHERE org_id = %s''', [org_id])
        pitches = cursor.fetchall()
    return JsonResponse({'grounds': [{'pitches': pitch} for pitch in pitches]})


def curator_daily_recording_form(request):
    try:
        org_id = request.session["org_id"]
        if request.method == "POST":

            if request.POST['pitch_id'] != "all":
                pitch_id = request.POST['pitch_id']
                all_pitches = 0
            elif request.POST['pitch_id'] == "all":
                pitch_id = -1
                all_pitches = 1

            # pitch_location = request.POST['pitch_location']
            # rolling_start_date = request.POST['rolling_start_date']
            # weight_of_the_roller = request.POST['weight_of_the_roller']
            # no_of_passes = request.POST['no_of_passes']
            # rolling_speed = request.POST['rolling_speed']
            # last_watering_on = request.POST['last_watering_on']
            # quantity_of_water = request.POST['quantity_of_water']
            # time_of_application = request.POST['time_of_application']
            # is_daily_watering = request.POST.get('is_daily_watering', 'off') == 'on'
            # remark_by_groundsman = request.POST['remark_by_groundsman']
            # date_mowing_done_last = request.POST['date_mowing_done_last']
            # mowing_done_at_mm = request.POST['mowing_done_at_mm']
            # is_fertilizers_used = request.POST.get('is_fertilizers_used', 'off') == 'on'
            # fertilizers_details = request.POST['fertilizers_details']
            # recording_type = request.POST['recording_type']
            #
            # min_temp = request.POST['min_temp']
            # max_temp = request.POST['max_temp']
            # forecast = request.POST['forecast']
            # chemical_details_remark = request.POST['chemical_details_remark']
            # clagg_hammer = "NA" if recording_type=="daily" or recording_type=="both" else request.POST['clagg_hammer']
            # moisture = "NA" if recording_type=="daily" or recording_type=="both" else request.POST['moisture']
            # ground_id = request.POST['ground_id']
            # with connection.cursor() as cursor:
            #     cursor.execute(
            #         f"""INSERT INTO {org_id}_curator_daily_recording_master (pitch_id,pitch_location, rolling_start_date, weight_of_the_roller, no_of_passes,
            #         rolling_speed, last_watering_on, quantity_of_water, time_of_application, is_daily_watering, remark_by_groundsman,
            #         date_mowing_done_last, mowing_done_at_mm, is_fertilizers_used, fertilizers_details,recording_type,min_temp,max_temp,forecast,clagg_hammer,moisture,ground_id,all_pitches,chemical_details_remark)
            #         VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)""",
            #         [pitch_id, pitch_location, rolling_start_date, weight_of_the_roller, no_of_passes, rolling_speed,
            #          last_watering_on,
            #          quantity_of_water, time_of_application, is_daily_watering, remark_by_groundsman, date_mowing_done_last,
            #          mowing_done_at_mm,
            #          is_fertilizers_used, fertilizers_details, recording_type, min_temp, max_temp, forecast, clagg_hammer,
            #          moisture, ground_id, all_pitches, chemical_details_remark]
            #     )

            recording_type = request.POST['recording_type']
            ground_id = request.POST['ground_id']
            pitch_id = request.POST['pitch_id']
            pitch_location = request.POST['pitch_location']
            rolling_start_date = request.POST['rolling_start_date']
            min_temp = request.POST['min_temp']
            max_temp = request.POST['max_temp']
            forecast = request.POST['forecast']
            clagg_hammer = "NA" if recording_type in ["daily", "both"] else request.POST.get('clagg_hammer', 'NA')
            moisture = "NA" if recording_type in ["daily", "both"] else request.POST.get('moisture', 'NA')
            # Extract pitch entries
            machinery_id = request.POST['machinery_id']
            no_of_passes = request.POST['no_of_passes']
            rolling_speed = request.POST['rolling_speed']
            last_watering_on = request.POST['last_watering_on']
            quantity_of_water = request.POST['quantity_of_water']
            time_of_application = request.POST['time_of_application']
            # is_daily_watering = request.POST.get('is_daily_watering', 'off') == 'on'
            is_daily_watering = "1" if request.POST.get('is_daily_watering', 'off') == 'on' else "0"
            mover_machinery_id = request.POST['mover_machinery_id']
            date_mowing_done_last = request.POST['date_mowing_done_last']
            time_of_application_mover = request.POST['time_of_application_mover']
            mowing_done_at_mm = request.POST['mowing_done_at_mm']
            # is_fertilizers_used = request.POST.get('is_fertilizers_used', 'off') == 'on'
            is_fertilizers_used = "1" if request.POST.get('is_fertilizers_used', 'off') == 'on' else "0"
            fertilizers_details = request.POST['fertilizers_details']
            chemical_details_remark = request.POST['chemical_details_remark']
            remark_by_groundsman = request.POST['remark_by_groundsman']

            # Extract outfield entries
            out_machinery_id = request.POST['out_machinery_id']
            out_no_of_passes = request.POST['out_no_of_passes']
            out_rolling_speed = request.POST['out_rolling_speed']
            out_last_watering_on = request.POST['out_last_watering_on']
            out_quantity_of_water = request.POST['out_quantity_of_water']
            out_time_of_application = request.POST['out_time_of_application']
            # out_is_daily_watering = request.POST.get('out_is_daily_watering', 'off') == 'on'
            out_is_daily_watering = "1" if request.POST.get('out_is_daily_watering', 'off') == 'on' else "0"
            out_mover_machinery_id = request.POST['out_mover_machinery_id']
            out_date_mowing_done_last = request.POST['out_date_mowing_done_last']
            time_of_application_out_mover = request.POST['time_of_application_out_mover']
            out_mowing_done_at_mm = request.POST['out_mowing_done_at_mm']
            # out_is_fertilizers_used = request.POST.get('out_is_fertilizers_used', 'off') == 'on'
            out_is_fertilizers_used = "1" if request.POST.get('out_is_fertilizers_used', 'off') == 'on' else "0"
            out_fertilizers_details = request.POST['out_fertilizers_details']
            out_chemical_details_remark = request.POST['out_chemical_details_remark']
            out_remark_by_groundsman = request.POST['out_remark_by_groundsman']

            # Insert data into the database
            with connection.cursor() as cursor:
                query = f"""
                    INSERT INTO {org_id}_curator_daily_recording_master (
                        pitch_id, pitch_location, rolling_start_date, min_temp, max_temp, forecast, clagg_hammer, moisture, 
                        machinery_id, no_of_passes, rolling_speed, last_watering_on, quantity_of_water, time_of_application, 
                        is_daily_watering, mover_machinery_id, date_mowing_done_last, time_of_application_mover, mowing_done_at_mm, 
                        is_fertilizers_used, fertilizers_details, chemical_details_remark, remark_by_groundsman, 
                        out_machinery_id, out_no_of_passes, out_rolling_speed, out_last_watering_on, out_quantity_of_water, 
                        out_time_of_application, out_is_daily_watering, out_mover_machinery_id, out_date_mowing_done_last, 
                        time_of_application_out_mover, out_mowing_done_at_mm, out_is_fertilizers_used, out_fertilizers_details, 
                        out_chemical_details_remark, out_remark_by_groundsman, recording_type, ground_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                    """
                values = [
                    pitch_id, pitch_location, rolling_start_date, min_temp, max_temp, forecast, clagg_hammer, moisture,
                    machinery_id, no_of_passes, rolling_speed, last_watering_on, quantity_of_water, time_of_application,
                    is_daily_watering, mover_machinery_id, date_mowing_done_last, time_of_application_mover,
                    mowing_done_at_mm,
                    is_fertilizers_used, fertilizers_details, chemical_details_remark, remark_by_groundsman,
                    out_machinery_id, out_no_of_passes, out_rolling_speed, out_last_watering_on, out_quantity_of_water,
                    out_time_of_application, out_is_daily_watering, out_mover_machinery_id, out_date_mowing_done_last,
                    time_of_application_out_mover, out_mowing_done_at_mm, out_is_fertilizers_used,
                    out_fertilizers_details,
                    out_chemical_details_remark, out_remark_by_groundsman, recording_type, ground_id
                ]

                # Debugging: Print the query and values
                print("Query:", query)
                print("Values:", values)

                cursor.execute(query, values)
                print("Hello")
            return redirect('curator_daily_recording_list')


        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {org_id}_pitch_master")
            pitches = cursor.fetchall()
            print(pitches)

        return render(request, 'admin_user/curator_daily_recording_form.html', {'pitches': pitches})
    except Exception as e:
        print(e)


def curator_daily_recording_list(request):
    org_id = request.session["org_id"]
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"SELECT * FROM {org_id}_curator_daily_recording_master order by id desc")
            recordings = cursor.fetchall()
        except Exception as e:
            print(e)
            return messages.error(request,e)
    return render(request, 'admin_user/curator_daily_recording_list.html', {'recordings': recordings})


# Fetch All Machinery
def machinery_list(request):
    org_id = request.session["org_id"]
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {org_id}_machinery_master')
        machinery = cursor.fetchall()
    return render(request, 'admin_user/machinery_list.html', {'machinery': machinery})


# Insert Machinery
def insert_machinery(request):
    org_id = request.session["org_id"]
    if request.method == 'POST':
        equipment_name = request.POST['equipment_name']
        equipment_model = request.POST['equipment_model']
        type_ = request.POST['type']
        company = request.POST['company']
        specification = request.POST['specification']
        unit = request.POST['unit']
        value = request.POST['value']

        with connection.cursor() as cursor:
            cursor.execute(f'''
            INSERT INTO {org_id}_machinery_master
(`equipment_name`,`type`,`specification`,`unit`,`value`,`model`) VALUES
(%s,<%s>,<%s>,<%s>,<%s>,<%s>,<%s>)
            ''', [equipment_name, type_,specification,unit,value,equipment_model ])

        return redirect('machinery_list')

    return render(request, 'admin_user/machinery_master.html')



def get_machinery_data(request):
    org_id = request.session["org_id"]
    with connection.cursor() as cursor:
        try:
            sql=f"SELECT * FROM {org_id}_machinery_master"
            print(sql)
            cursor.execute(f"SELECT * FROM {org_id}_machinery_master")

            data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            machinery_data = [dict(zip(columns, row)) for row in data]
            return JsonResponse(machinery_data, safe=False)
        except Exception as e:
            print(e)

    return JsonResponse(machinery_data, safe=False)


# Update Machinery
def update_machinery(request, machinery_id):

    try:
        org_id = request.session["org_id"]
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {org_id}_machinery_master WHERE id = %s', [machinery_id])
            machinery = cursor.fetchone()


        if request.method == 'POST':
            equipment_name = request.POST['equipment_name']
            equipment_model = request.POST['equipment_model']
            type_ = request.POST['type']
            # company = request.POST['company']
            specification = request.POST['specification']
            unit = request.POST['unit']
            value = request.POST['value']

            with connection.cursor() as cursor:
                cursor.execute(f'''
                UPDATE {org_id}_machinery_master
SET `equipment_name` = %s,`type` = %s,`specification` = %s,`unit` = %s,`value` = %s,
`model` = %s WHERE `id` = %s'''
    , [equipment_name, type_,specification,unit,value,equipment_model ,machinery_id])

            return redirect('machinery_list')
        print(machinery)
        return render(request, 'admin_user/update_machinery.html', {'machinery': machinery})
    except Exception as e:
        print(e)


def get_machinery_details(request, machinery_id):
    org_id = request.session["org_id"]
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT *  FROM {org_id}_machinery_master WHERE id = %s", [machinery_id])
        row = cursor.fetchone()

    if row:
        data = {
            'id': row[0],
            'equipment_name': row[1],
            'model': row[2],
            'type': row[3],

            'specification': row[4],
            'unit': row[5],
            'value': row[6],
        }
        return JsonResponse({'machinery': data})
    else:
        return JsonResponse({'error': 'Machinery not found'}, status=404)



def add_score(request, match_id):
    try:
        org_id = request.session["org_id"]
        query = f"SELECT * FROM {org_id}_match_master WHERE id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(query, [match_id])
            match = cursor.fetchone()

        if request.method == "POST":
            team1_score = request.POST['team1_score']
            team2_score = request.POST['team2_score']
            team1_wickets = request.POST['team1_wickets']
            team2_wickets = request.POST['team2_wickets']
            overs = request.POST['overs']
            winner = request.POST['winner']
            dayEnd = request.POST['day-end']

            if match[1] == 'Test':  # If it's a Test match, store scores by day
                day = request.POST['day']
                query = f"""
                    INSERT INTO {org_id}_match_scores_master (match_id, day, team1_score, team2_score, team1_wickets, team2_wickets, overs, winner,day_end)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s);
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [match_id, day, team1_score, team2_score, team1_wickets, team2_wickets, overs, winner,dayEnd])
            else:
                query = f"""
                    INSERT INTO {org_id}_match_scores_master (match_id, team1_score, team2_score, team1_wickets, team2_wickets, overs, winner,day_end)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s);
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [match_id, team1_score, team2_score, team1_wickets, team2_wickets, overs, winner,dayEnd])

            return redirect('list_matches')

        # match_data = {
        #     'id': match[0],
        #     'match_type': match[1],
        #     'team1': match[2],
        #     'team2': match[3],
        #     'match_date': match[4],
        #     'venue': match[5]
        # }
        print(match)

        return render(request, 'admin_user/score_form.html', {'match': match})
    except Exception as e:
        print(e)

@csrf_exempt
def save_scores(request):
    org_id = request.session["org_id"]
    if request.method == 'POST':
        data = json.loads(request.body)
        match_id = data.get('match_id')
        scores = data.get('scores')

        with connection.cursor() as cursor:
            for score in scores:
                day = score.get('day')
                inning = score.get('inning')
                team = score.get('team')
                session = score.get('session')
                runs = score.get('runs')
                wickets = score.get('wickets')
                overs = score.get('overs')
                winner = score.get('winner')
                dayEnd = score.get('dayEnd')

                # Insert the score into the match_scores table
                cursor.execute(f"""
                    INSERT INTO {org_id}_match_scores_master (match_id, day, inning, team, session, runs, wickets, overs, winner,day_end)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                """, [match_id, day, inning, team, session, runs, wickets, overs, winner,dayEnd])

        return JsonResponse({'status': 'success'})

@csrf_exempt
def get_match_scores(request, match_id):
    try:
        org_id = request.session["org_id"]
        if request.method == 'GET':
            with connection.cursor() as cursor:
                # Fetch scores based on match_id
                cursor.execute(f"""
                    SELECT id, day, inning, team, session, runs, wickets, overs, winner,day_end
                    FROM {org_id}_match_scores_master
                    WHERE match_id = %s
                """, [match_id])
                scores = cursor.fetchall()

            # Format the response data
            scores_data = [
                {
                    'id': row[0],
                    'day': row[1],
                    'inning': row[2],
                    'team': row[3],
                    'session': row[4],
                    'runs': row[5],
                    'wickets': row[6],
                    'overs': row[7],
                    'winner': row[8],
                    'day_end': row[9]
                }
                for row in scores
            ]

            return JsonResponse({'scores': scores_data})
    except Exception as e:
        print(e)

def match_scores_list(request,match_id):
    return render(request, "admin_user/match_scores_list.html", {"match_id": match_id})


@csrf_exempt
def delete_score(request, score_id):
    org_id = request.session["org_id"]
    if request.method == 'DELETE':
        with connection.cursor() as cursor:
            # Delete score by id
            cursor.execute(f"""
                DELETE FROM {org_id}_match_scores_master
                WHERE id = %s
            """, [score_id])

        return JsonResponse({'status': 'success'})

@csrf_exempt
def update_score(request, score_id):
    org_id = request.session["org_id"]
    try:
        if request.method == 'PUT':
            data = json.loads(request.body)
            day = data.get('day')
            inning = data.get('inning')
            team = data.get('team')
            session = data.get('session')
            runs = data.get('runs')
            wickets = data.get('wickets')
            overs = data.get('overs')
            winner = data.get('winner')
            dayEnd = data.get('dayEnd')

            with connection.cursor() as cursor:
                # Update the score entry
                cursor.execute(f"""
                    UPDATE {org_id}_match_scores_master
                    SET day = %s, inning = %s, team = %s, session = %s, runs = %s, wickets = %s, overs = %s, winner = %s,day_end=%s
                    WHERE id = %s
                """, [day, inning, team, session, runs, wickets, overs, winner, dayEnd,score_id])

            return JsonResponse({'status': 'success'})
    except Exception as e:
        print(e)

  # match_type = request.POST['match_type']
            # name_tournament = request.POST['name_tournament']
            # team1 = request.POST['team1']
            # team2 = request.POST['team2']
            # preparation_date = request.POST['preparation_date']
            # match_date = request.POST.get('match_date')
            # from_date = request.POST.get('from_date')
            # to_date = request.POST.get('to_date')
            # days_count = request.POST['days_count']
            # start_time = request.POST['start_time']
            # pitch_id = request.POST['pitch_id']
            # ground_id = request.POST['ground_id']
            # is_pitch_level =   1 if request.POST.get('is_pitch_level')=="on" else 0
            # lawn_height = request.POST['lawn_height']
            # grass_cover = request.POST['grass_cover']
            # weather_condition = request.POST['weather_condition']
            # moisture_upto = request.POST['moisture_upto']
            # rolling_time = request.POST['rolling_time']
            # rolling_pattern = request.POST['rolling_pattern']
            # roller_type = request.POST['machinery_id']
            # # roller_weight = request.POST.get('roller_weight', None)
            # roller_weight = "weight"
            # dew_factor = request.POST['dew_factor']
            # access_bounce = request.POST['access_bounce']
            #
            # # Construct the SQL query to insert the values
            # with connection.cursor() as cursor:
            #     cursor.execute(f'''
            #         INSERT INTO {org_id}_match_master
            #         (match_type, name_tournament, team1, team2, preparation_date, match_date, from_date, to_date,
            #          days_count, start_time, pitch_id,ground_id, is_pitch_level, lawn_height, grass_cover, weather_condition,
            #          moisture_upto, rolling_time, rolling_pattern, roller_type, roller_weight, dew_factor, access_bounce)
            #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            #     ''', [
            #         match_type, name_tournament, team1, team2, preparation_date, match_date, from_date, to_date,
            #         days_count, start_time, pitch_id,ground_id, is_pitch_level, lawn_height, grass_cover, weather_condition,
            #         moisture_upto, rolling_time, rolling_pattern, roller_type, roller_weight, dew_factor, access_bounce
            #     ])
def insert_match(request):
    try:
        org_id = request.session["org_id"]
        if request.method == 'POST':

            match_type = request.POST['match_type']
            name_tournament = request.POST['name_tournament']
            team1 = request.POST['team1']
            team2 = request.POST['team2']
            preparation_date = request.POST['preparation_date']
            match_date = request.POST.get('match_date')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            days_count = request.POST['days_count']
            start_time = request.POST['start_time']
            pitch_id = request.POST['pitch_id']
            ground_id = request.POST['ground_id']
            is_pitch_level = request.POST.get('is_pitch_level', 'off') == 'on'
            lawn_height = request.POST['lawn_height']
            grass_cover = request.POST['grass_cover']
            min_temp = request.POST['min_temp']
            max_temp = request.POST['max_temp']
            forecast = request.POST['forecast']
            moisture_upto = request.POST['moisture_upto']
            # rolling_time = request.POST['rolling_time']
            # rolling_pattern = request.POST['rolling_pattern']
            machinery_id = request.POST['machinery_id']
            dew_factor = request.POST['dew_factor']
            access_bounce = request.POST['access_bounce']
            remark_by_groundsman = request.POST['remark_by_groundsman']
            chemical_details_remark = request.POST['chemical_details_remark']
            out_no_of_passes = request.POST['out_no_of_passes']
            out_rolling_speed = request.POST['out_rolling_speed']
            out_last_watering_on = request.POST['out_last_watering_on']
            out_quantity_of_water = request.POST['out_quantity_of_water']
            out_time_of_application = request.POST['out_time_of_application']
            out_is_daily_watering = request.POST.get('out_is_daily_watering', 'off') == 'on'
            out_machinery_id = request.POST['out_machinery_id']
            out_mowing_done_at_mm = request.POST['out_mowing_done_at_mm']
            out_remark_by_groundsman = request.POST['out_remark_by_groundsman']
            brief_match_pitch_assessment = request.POST['brief_match_pitch_assessment']

            # Insert data
            with connection.cursor() as cursor:
                sql=f'''
                          INSERT INTO {org_id}_match_master 
                          (match_type, name_tournament, team1, team2, preparation_date, match_date, from_date, to_date,
                           days_count, start_time, pitch_id, ground_id, is_pitch_level, lawn_height, grass_cover, 
                           min_temp, max_temp, forecast, moisture_upto, machinery_id,
                           dew_factor, access_bounce, remark_by_groundsman, chemical_details_remark, out_no_of_passes, 
                           out_rolling_speed, out_last_watering_on, out_quantity_of_water, out_time_of_application, 
                           out_is_daily_watering, out_machinery_id, out_mowing_done_at_mm, out_remark_by_groundsman, 
                           brief_match_pitch_assessment) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                      '''
                values=[
                    match_type, name_tournament, team1, team2, preparation_date, match_date, from_date, to_date,
                    days_count, start_time, pitch_id, ground_id, is_pitch_level, lawn_height, grass_cover,
                    min_temp, max_temp, forecast, moisture_upto, machinery_id,
                    dew_factor, access_bounce, remark_by_groundsman, chemical_details_remark, out_no_of_passes,
                    out_rolling_speed, out_last_watering_on, out_quantity_of_water, out_time_of_application,
                    out_is_daily_watering, out_machinery_id, out_mowing_done_at_mm, out_remark_by_groundsman,
                    brief_match_pitch_assessment
                ]
                print(sql)
                print(values)
                cursor.execute(sql,values)

            return redirect('match_list')

        return render(request, 'admin_user/match_master.html')
    except Exception as e:
        print(e)



def update_match(request, match_id):
    try:
        org_id = request.session["org_id"]

        # Fetch match data to pre-populate the form
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {org_id}_match_master WHERE id = %s', [match_id])
            match = cursor.fetchone()

        if not match:
            raise Exception("Match not found")

        if request.method == 'POST':
            # Collecting data from the form
            match_type = request.POST['match_type']
            name_tournament = request.POST['name_tournament']
            team1 = request.POST['team1']
            team2 = request.POST['team2']
            preparation_date = request.POST['preparation_date']
            match_date = request.POST.get('match_date')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            days_count = request.POST['days_count']
            start_time = request.POST['start_time']
            pitch_id = request.POST['pitch_id']
            ground_id = request.POST['ground_id']
            is_pitch_level = request.POST.get('is_pitch_level', 'off') == 'on'
            lawn_height = request.POST['lawn_height']
            grass_cover = request.POST['grass_cover']
            min_temp = request.POST['min_temp']
            max_temp = request.POST['max_temp']
            forecast = request.POST['forecast']
            moisture_upto = request.POST['moisture_upto']
            machinery_id = request.POST['machinery_id']
            dew_factor = request.POST['dew_factor']
            access_bounce = request.POST['access_bounce']
            remark_by_groundsman = request.POST['remark_by_groundsman']
            chemical_details_remark = request.POST['chemical_details_remark']
            out_no_of_passes = request.POST['out_no_of_passes']
            out_rolling_speed = request.POST['out_rolling_speed']
            out_last_watering_on = request.POST['out_last_watering_on']
            out_quantity_of_water = request.POST['out_quantity_of_water']
            out_time_of_application = request.POST['out_time_of_application']
            out_is_daily_watering = request.POST.get('out_is_daily_watering', 'off') == 'on'
            out_machinery_id = request.POST['out_machinery_id']
            out_mowing_done_at_mm = request.POST['out_mowing_done_at_mm']
            out_remark_by_groundsman = request.POST['out_remark_by_groundsman']
            brief_match_pitch_assessment = request.POST['brief_match_pitch_assessment']

            # Update the match record in the database
            with connection.cursor() as cursor:
                sql = f'''
                    UPDATE {org_id}_match_master 
                    SET match_type=%s, name_tournament=%s, team1=%s, team2=%s, preparation_date=%s, match_date=%s, 
                        from_date=%s, to_date=%s, days_count=%s, start_time=%s, pitch_id=%s, ground_id=%s, 
                        is_pitch_level=%s, lawn_height=%s, grass_cover=%s, min_temp=%s, max_temp=%s, forecast=%s, 
                        moisture_upto=%s, machinery_id=%s, dew_factor=%s, access_bounce=%s, 
                        remark_by_groundsman=%s, chemical_details_remark=%s, out_no_of_passes=%s, 
                        out_rolling_speed=%s, out_last_watering_on=%s, out_quantity_of_water=%s, out_time_of_application=%s, 
                        out_is_daily_watering=%s, out_machinery_id=%s, out_mowing_done_at_mm=%s, 
                        out_remark_by_groundsman=%s, brief_match_pitch_assessment=%s
                    WHERE id=%s
                '''
                values = [
                    match_type, name_tournament, team1, team2, preparation_date, match_date, from_date, to_date,
                    days_count, start_time, pitch_id, ground_id, is_pitch_level, lawn_height, grass_cover,
                    min_temp, max_temp, forecast, moisture_upto, machinery_id, dew_factor, access_bounce,
                    remark_by_groundsman, chemical_details_remark, out_no_of_passes, out_rolling_speed,
                    out_last_watering_on, out_quantity_of_water, out_time_of_application, out_is_daily_watering,
                    out_machinery_id, out_mowing_done_at_mm, out_remark_by_groundsman, brief_match_pitch_assessment,
                    match_id
                ]
                cursor.execute(sql, values)

            return redirect('match_list')

        # Pass match data to the form for editing
        return render(request, 'admin_user/match_update_master.html', {'match': match})

    except Exception as e:
        print("Error:", e)
        return render(request, 'admin_user/error.html', {'error': str(e)})


def match_list(request):
    try:
        org_id = request.session["org_id"]
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {org_id}_match_master')
            matches = cursor.fetchall()


        return render(request, 'admin_user/match_list.html', {'matches': matches})
    except Exception as e:
        print(e)


from django.http import JsonResponse
from django.db import connection


# # View to get all Ground IDs
# def get_grounds(request):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id FROM yourapp_ground")
#         rows = cursor.fetchall()
#
#     # Convert the result into a list of dictionaries
#     ground_list = [{'id': row[0]} for row in rows]
#     return JsonResponse(ground_list, safe=False)
#
#
# # View to get Pitches based on selected Ground ID
# def get_pitches(request, ground_id):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id FROM yourapp_pitch WHERE ground_id = %s", [ground_id])
#         rows = cursor.fetchall()
#
#     # Convert the result into a list of dictionaries
#     pitch_list = [{'id': row[0]} for row in rows]
#     return JsonResponse(pitch_list, safe=False)
