import os
import subprocess
from .variables import variables 

packeges = [
    "pyTelegramBotAPI", "psycopg2-binary", "python-decouple", "pandas",
    "SQLAlchemy", "openpyxl"
]

class TelegramBotTemplate:
    def __init__(self, project_location):
        self.location = project_location
        self.dirs = [
            {"config": ["loader.py", ".env", "settings.py", "database.py", "states.py", "__init__.py"]},
            {"keyboards": ["inline_markup.py", "relpy_markup.py", "__init__.py"]},
            {"handlers": ["__init__.py"]}, 
            {"handlers/admin": ["callbacks.py", "text_handlers.py", "__init__.py"]}, 
            {"handlers/users": ["commands.py", "callbacks.py", "text_handlers.py", "__init__.py"]}
        ]
        self.main_files = ["main.py", ".env.example", "test.py"]
        


    def write_init_file(self, file, folder, data):
        if file == "__init__.py":
            data[folder].remove(file)
            for f2 in data[folder]:
                if f2 != ".env":
                    with open(f"{self.location}/{folder}/{file}", "a") as f:
                        f.write(f"from . import {f2.replace('.py', '')}\n")


    def generate_template(self):
        os.system(f"cd {self.location} && python3 -m venv online")
        for pkg in packeges:
            install_pkg = f"{self.location}/online/bin/python -m pip install {pkg} >> {self.location}/install_pkg.txt 2>&1"
            pip_freeze = f"{self.location}/online/bin/python -m pip freeze > {self.location}/requarements.txt"
            subprocess.Popen(install_pkg, shell=True)
            subprocess.run(pip_freeze, shell=True)
            print("Installed: ", pkg)

        for data in self.dirs:
            for folder in data:
                subprocess.Popen(f"mkdir {self.location}/{folder}/", shell=True)
                for file in data[folder]:
                    subprocess.Popen(f"touch {self.location}/{folder}/{file}", shell=True)
                    self.write_init_file(file, folder, data)      
                if folder == "handlers":
                    with open(f"{self.location}/{folder}/__init__.py", "a") as f:
                        f.write(f"from . import admin\nfrom . import users")

        for f in self.main_files:
            subprocess.Popen(f"touch {self.location}/{f}", shell=True)
    
        with open(f"{self.location}/main.py", "a") as main:
            main.write(variables.MAIN)
    
        with open(f"{self.location}/test.py", "a") as test:
            test.write(variables.TEST)
    
        with open(f"{self.location}/config/.env", "a") as env:
            env.write(variables.ENV)

        with open(f"{self.location}/.env.example", "a") as env:
            env.write(variables.ENV)

        with open(f"{self.location}/config/database.py", "a") as database:
            database.write(variables.DATABASE)

        with open(f"{self.location}/config/loader.py", "a") as database:
            database.write(variables.LOADER)

        with open(f"{self.location}/config/settings.py", "a") as database:
            database.write(variables.SETTINGS)

        with open(f"{self.location}/config/states.py", "a") as database:
            database.write(variables.STATES)

        with open(f"{self.location}/handlers/admin/callbacks.py", "a") as database:
            database.write(variables.CALLBACK_QUERY)

        with open(f"{self.location}/handlers/admin/text_handlers.py", "a") as database:
            database.write(variables.TEXT_HANDLER)

        with open(f"{self.location}/handlers/users/callbacks.py", "a") as database:
            database.write(variables.CALLBACK_QUERY)

        with open(f"{self.location}/handlers/users/text_handlers.py", "a") as database:
            database.write(variables.TEXT_HANDLER)

        with open(f"{self.location}/handlers/users/commands.py", "a") as database:
            database.write(variables.COMMANDS)

        with open(f"{self.location}/keyboards/inline_markup.py", "a") as database:
            database.write(variables.INLINE_MARKUB)

        with open(f"{self.location}/keyboards/relpy_markup.py", "a") as database:
            database.write(variables.REPLY_MARKUB)

