import sys
import os

# Update the path to the project root
project_root = '/home/techclass/public_html/curator.web'  # change this path if you rename the folder

# Add project and virtual environment paths
sys.path.insert(0, project_root)
sys.path.insert(1, os.path.join(project_root, 'venv/lib/python3.10/site-packages'))

# Set the environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'curator.web.settings'  # adjust to match the new folder name

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
