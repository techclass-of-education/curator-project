from .models import SuperAdmin, AdminUserList

# Create your views here.
from admin_user.forms.adminRoleForm import AdminUserRoleForm


def login(request):
    return render(request, 'super_admin_user/login.html')


def login_auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # SuperAdmin.objects.
        try:
            user = SuperAdmin.objects.get( username=username, password=password)
            if user is not None:
                return render(request, 'super_admin_user/dashboard.html',{'user':user})
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'super_admin_user/login.html')
        except Exception as e:
            print(e)
            return render(request, 'super_admin_user/login.html')


def dashboard(request):
    return render(request, 'super_admin_user/dashboard.html')


def logout_root(request):
    return redirect('login_root')

# views.py

from django.shortcuts import render, redirect
from .templates.super_admin_user.admin.adminForm import AdminUserForm
from django.contrib import messages
from django.db import connection
from .models import MastersList

def createTable(tableName,t,org):
    with connection.cursor() as cursor:
        if(t=="state"):
            sql=f'''CREATE TABLE IF NOT EXISTS {tableName} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        state VARCHAR(255) NOT NULL UNIQUE,
        state_code VARCHAR(2) NOT NULL UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    '''
            cursor.execute(sql)
        elif (t == "city"):
            sql = f'''CREATE TABLE IF NOT EXISTS {tableName} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_name VARCHAR(255) NOT NULL UNIQUE,
                state_id INT,
                FOREIGN KEY (state_id) REFERENCES {org}_state_master(id),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
            '''
            cursor.execute(sql)

        elif (t == "ground"):
            sql = f'''
        CREATE TABLE IF NOT EXISTS {tableName} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            org_id VARCHAR(255),
            google_location TEXT,
            year_of_construction VARCHAR(255),
            phone_numbers VARCHAR(255),
            slop_ratio VARCHAR(255),
            ground_name VARCHAR(255),
            state_code VARCHAR(2),
            state_name VARCHAR(255),
            city_name VARCHAR(255),
            count_main_pitches INT,
            count_practice_pitches INT,
            is_side_screen BOOLEAN,
            count_placement_side_screen INT,
            is_broadcasting_facility BOOLEAN,
            is_irrigation_pitches BOOLEAN,
            count_hydrants INT,
            count_pumps INT,
            count_showers INT,
            is_lawn_nursary BOOLEAN,
            name_centre_square VARCHAR(255),
            is_curator_room BOOLEAN,
            is_seperate_practice_area BOOLEAN,
            outfield VARCHAR(255),
            profile_of_outfield VARCHAR(255),
            lawn_species VARCHAR(255),
            is_drainage_system_available BOOLEAN,
            is_water_drainage_system BOOLEAN,
            is_irrigation_system_available BOOLEAN,
            is_availability_of_water BOOLEAN,
            water_source text,
            storage_capacity_in_litres INT,
            count_pop_ups INT,
            size_of_pumps VARCHAR(255),
            is_automation_if_any BOOLEAN,
            is_ground_equipments BOOLEAN,
            is_maintenance_contract BOOLEAN,
            is_maintenance_agency BOOLEAN,
            boundary_size_mtrs text,
            is_availability_of_mot BOOLEAN,
            is_machine_shed BOOLEAN,
            is_soil_shed BOOLEAN,
            is_pitch_or_run_up_covers BOOLEAN,
            size_of_covers_in_mtrs VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
            '''
            cursor.execute(sql)
        elif (t == "pitch"):
            sql = f'''
        CREATE TABLE IF NOT EXISTS {tableName} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            org_id VARCHAR(255),
            ground_id INT,
            size_pitch_square text,
            pitch_no VARCHAR(255),
            pitch_type VARCHAR(255),
            profile_of_pitches VARCHAR(255),
            last_used_date DATE,
            last_used_match VARCHAR(255),
            soil_type VARCHAR(255),
            is_uniformtiy_of_grass BOOLEAN,
            size_of_grass text,
            mowing_last_date DATE,
            size_pitch VARCHAR(45),
            pitch_placement VARCHAR(45),
            pitch_in_out VARCHAR(45),
            mowing_size text,
            start_date_of_pitch_preparation DATE,
            date_pitch_construction DATE,
            pitch_details text,
            FOREIGN KEY (ground_id) REFERENCES {org}_ground_master(id),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
            '''
            cursor.execute(sql)
        elif (t == "curator_daily_recording"):
                    sql = f'''
                CREATE TABLE IF NOT EXISTS {tableName} (
                             id INT AUTO_INCREMENT PRIMARY KEY,
    pitch_id INT NOT NULL,
    pitch_location VARCHAR(255),
    rolling_start_date DATE NOT NULL,
    min_temp VARCHAR(45),
    max_temp VARCHAR(45),
    forecast VARCHAR(255),
    clagg_hammer VARCHAR(255),
    moisture VARCHAR(255),

    machinery_id INT,
    no_of_passes INT NOT NULL,
    rolling_speed FLOAT NOT NULL,
    last_watering_on DATE NOT NULL,
    quantity_of_water FLOAT NOT NULL,
    time_of_application TIME NOT NULL,
    time_roller TIME NOT NULL,
    is_daily_watering BOOLEAN NOT NULL,

    mover_machinery_id INT,
    date_mowing_done_last DATE NOT NULL,
    time_of_application_mover TIME NOT NULL,
    mowing_done_at_mm FLOAT NOT NULL,

    is_fertilizers_used BOOLEAN NOT NULL,
    fertilizers_details VARCHAR(255),
    chemical_details_remark LONGTEXT,
    remark_by_groundsman VARCHAR(255),

    out_machinery_id INT,
    out_no_of_passes INT,
    out_rolling_speed FLOAT,
    out_last_watering_on DATE,
    out_quantity_of_water FLOAT,
    out_time_of_application TIME,
    out_time_roller TIME,
    out_is_daily_watering BOOLEAN,

    out_mover_machinery_id INT,
    out_date_mowing_done_last DATE,
    time_of_application_out_mover TIME,
    out_mowing_done_at_mm FLOAT,
    out_is_fertilizers_used BOOLEAN,
    out_fertilizers_details VARCHAR(255),
    out_chemical_details_remark LONGTEXT,
    out_remark_by_groundsman VARCHAR(255),

    recording_type VARCHAR(45),
    ground_id INT NOT NULL,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (pitch_id) REFERENCES {org}_pitch_master(id),
   
    FOREIGN KEY (ground_id) REFERENCES {org}_ground_master(id)
);
                        
                    
                
                    '''
                    cursor.execute(sql)
        elif (t == "machinery"):
                    sql = f'''
    CREATE TABLE IF NOT EXISTS {tableName} (    
  `id` int NOT NULL AUTO_INCREMENT,
  `equipment_name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `specification` text NOT NULL,
  `unit` varchar(50) NOT NULL,
  `value` text NOT NULL,
  `model` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

                    '''
                    cursor.execute(sql)
        elif (t == "match_scores"):
                    sql = f'''
    CREATE TABLE IF NOT EXISTS {tableName} (    
    id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT,
    `day` INT DEFAULT 1,
    team TEXT,
    inning INT,
    `session` INT,
    wickets INT,
    overs FLOAT,
    runs INT,
    winner INT,
    day_end VARCHAR(45),
    FOREIGN KEY (match_id) REFERENCES {org}_match_master(id) ON DELETE CASCADE
);
                    '''
                    cursor.execute(sql)
        elif (t == "match"):
                    sql = f'''
  CREATE TABLE IF NOT EXISTS {tableName} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_type VARCHAR(255) , 
    name_tournament VARCHAR(255) ,
    team1 VARCHAR(255) ,
    team2 VARCHAR(255) ,
    preparation_date text,
    match_date text,
    from_date text,
    to_date text,
    days_count text,
    start_time text ,
    pitch_id int ,
    ground_id int ,
    is_pitch_level text,
    lawn_height text,
    grass_cover VARCHAR(255),
    min_temp text,
    max_temp text,
    forecast TEXT,
    moisture_upto text,
   
    dew_factor text,
    access_bounce text,
    machinery_id text,
    no_of_passes text ,
    rolling_speed text ,
    last_watering_on text,
    quantity_of_water text ,
    time_of_application text ,
    time_roller text,
    is_daily_watering text ,

    mover_machinery_id text,
    date_mowing_done_last text,
    time_of_application_mover text ,
    mowing_done_at_mm text ,

    is_fertilizers_used text ,
    fertilizers_details VARCHAR(255),
    chemical_details_remark LONGTEXT,
    remark_by_groundsman VARCHAR(255),

    out_machinery_id text,
    out_no_of_passes text,
    out_rolling_speed text,
    out_last_watering_on text,
    out_quantity_of_water text,
    out_time_of_application text,
    out_time_roller text,
    out_is_daily_watering text,

    out_mover_machinery_id text,
    out_date_mowing_done_last text,
    time_of_application_out_mover text,
    out_mowing_done_at_mm text,
    out_is_fertilizers_used text,
    out_fertilizers_details VARCHAR(255),
    out_chemical_details_remark LONGTEXT,
    out_remark_by_groundsman VARCHAR(255),

    brief_match_pitch_assessment TEXT,
    FOREIGN KEY (pitch_id) REFERENCES {org}_pitch_master(id),
    FOREIGN KEY (ground_id) REFERENCES {org}_ground_master(id),
   
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


                    '''
                    cursor.execute(sql)



def createAllMastersName(instance):
    tables = ["state","city", "ground", "pitch","curator_daily_recording","machinery","match","match_scores"]
    for t in tables:
        tableName=instance.org_id+"_"+t+"_master"
        masterList=MastersList()
        masterList.org_id=instance.org_id
        masterList.tablename=tableName
        masterList.admin_id=instance
        masterList.auth_scorer=True
        masterList.auth_curator=True
        masterList.auth_groundman=True
        masterList.save()

        createTable(tableName,t,instance.org_id)




def create_admin_user(request):
    try:
        if request.method == 'POST':
            form = AdminUserForm(request.POST, request.FILES)
            if form.is_valid():

                instance=form.save()
                messages.success(request, 'Admin user created successfully')
                createAllMastersName(instance)

                return redirect('admin_users_list')  # Redirect to a view that lists admin users
            else:
                messages.error(request, 'Please correct the errors below')
        else:
            form = AdminUserForm()
        return render(request, 'super_admin_user/admin/create_admin.html', {'form': form})
    except Exception as e:
        print(e)
#
# def create_admin_role(request):
#     if request.method == 'POST':
#         form = AdminUserRoleForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance=form.save()
#             messages.success(request, 'Admin user created successfully')
#             # createAllMastersTables(instance)
#             return redirect('admin_users_list')  # Redirect to a view that lists admin users
#         else:
#             messages.error(request, 'Please correct the errors below')
#     else:
#         form = AdminUserForm()
#     return render(request, 'super_admin_user/admin/create_admin.html', {'form': form})

def admin_users_list(request):
    admin_users = AdminUserList.objects.all()
    return render(request, 'super_admin_user/admin/admin_users_list.html', {'admin_users': admin_users})

def admin_user_details(request, admin_id):
    admin = AdminUserList.objects.get(id=admin_id)
    return render(request, 'super_admin_user/admin/admin_user_details.html', {'admin': admin})