import os
import fileinput
import subprocess
from django.core.management.utils import get_random_secret_key

from django_template.files import (settings, views_and_urls, templates)

packeges_list = [
    "django", "django-cors-headers", "whitenoise", "drf-spectacular", 
    "drf-spectacular[sidecar]", "gunicorn", "djangorestframework",
    "markdown", "django-filter", "psycopg2-binary", "python-decouple" 
]

class dJangoFramework:
    def __init__(self, project_location, apps):
        self.location = project_location
        self.apps:list = apps

    def generate_project(self):
        start_project = "django-admin startproject config ."
        start_app = "python3 manage.py startapp "
        os.system(f"cd {self.location} && {start_project}") 
        os.system(f"cd {self.location} && python3 -m venv online && mkdir templates && mkdir static")
        
        for pkg in packeges_list:
            install_pkgs = f"{self.location}/online/bin/python -m pip install {pkg} >> {self.location}install_log.txt 2>&1"
            pip_freeze = f"{self.location}/online/bin/python -m pip freeze > {self.location}/requarements.txt"
            print(f"Installing: {pkg}")
            subprocess.Popen(f"{install_pkgs}", shell=True) # install packeges
            subprocess.run(pip_freeze, shell=True) # add requarements text

        for app in self.apps:
            # make apps
            os.system(f"cd {self.location} && {start_app} {app}")

        with open(file=f"{self.location}/config/.env", mode="w") as ff:
            # write .env file in config folder 
            ff.write(settings.ENV)
        
        with open(file=f"{self.location}/.env.example", mode="w") as ff:
            # write .env.example file in base folder 
            ff.write(settings.ENV)

        with open(f"{self.location}/config/settings.py", "w") as f:
            f.write(settings.SETTINGS)     

        with open(f"{self.location}/config/urls.py", "w") as f:
            f.write(views_and_urls.CONFIG_URLS)     

        with fileinput.FileInput(f"{self.location}/config/settings.py", inplace=True) as file:
            local_apps = [f"{a}.apps.{a.title()}Config" for a in self.apps]
            for index, line in enumerate(file, start=1):
                if index == 45:
                    print(f"LOCAL_APPS = {local_apps}")
                if index == 55:
                    print("INSTALLED_APPS += LOCAL_APPS + GLOBAL_APPS")
                else:
                    print(line, end="")

        local_urls = [f"path('{a}/', include('{a}.urls'))" for a in self.apps]
        new_local_urls_line = f"local_urlpatterns = [{', '.join(local_urls)}]\n"
        new_urlpatterns_line = "urlpatterns += local_urlpatterns\n"
        with fileinput.FileInput(f"{self.location}/config/urls.py", inplace=True) as file:
            for index, line in enumerate(file, start=1):
                if index == 39:
                    print(new_local_urls_line)
                elif index == 41:
                    print(new_urlpatterns_line)
                else:
                    print(line, end="")

        for app in self.apps:
            with open(f"{self.location}/{app}/views.py", "w") as f:
                f.write(views_and_urls.VIEWS)
            with open(f"{self.location}/{app}/urls.py", "w") as f:
                f.write(views_and_urls.URLS)

        for template in ["base", "home", "index"]:
            if template == "base":
                with open(f"{self.location}templates/base.html", "w") as t:
                    t.write(templates.BASE)
            elif template == "home":
                with open(f"{self.location}templates/home.html", "w") as t:
                    t.write(templates.HOME)
            elif template == "index":
                with open(f"{self.location}templates/index.html", "w") as t:
                    t.write(templates.INDEX)

        with fileinput.FileInput(f"{self.location}/config/.env", inplace=True) as e:
            secret_key = f'SECRET_KEY="{get_random_secret_key()}"'
            for index, line in enumerate(e, start=1):
                if index == 1:
                    print(secret_key)
                else:
                    print(line, end="")
