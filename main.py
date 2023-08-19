import os
import argparse
from django_template.oop import dJangoFramework
from pyTelegramBotApi.oop import TelegramBotTemplate

description = """
    This program can make standart templates for two framework,
    starter settings and install nessesiry packeges, set env for project\n
    example for django project:\n
        \tpython3 main.py -f django -n <project_name> [-w /home/user/Desktop/ -ap main base users] -> those are not requared\n
    example for pyTelegramBotApi project:\n
        \tpython3 main.py -f telebot -n <project_name> [-w /home/user/Desktop/] -> this is not requared\n
"""

parser = argparse.ArgumentParser(description=description)
def Main():
    parser.add_argument("--framework", "-f", type=str, required=True, help="templtes framework, for example: '-f django' or '-f telebot' ")
    parser.add_argument("--project_name", "-n", type=str, required=True, help="Project name")
    parser.add_argument("--where", "-w", type=str, help="where need to save folder")  
    parser.add_argument("--apps", "-ap", nargs="*", default=["main"], action="store", help="django apps list for example: 'main base users' this is only django framework")
    args = parser.parse_args()
    framework, project_name = args.framework.lower(), args.project_name.lower()
    where = args.where
    apps = args.apps
    if where:
        os.system(f"mkdir {where}/{project_name}/")
        project_location = f"{where}/{project_name}/"
    else:
        os.system(f"mkdir {os.path.expanduser('~')}/Desktop/{project_name}/")
        project_location = f"{os.path.expanduser('~')}/Desktop/{project_name}/"
    if framework == "django":
        dJangoFramework(project_location, apps).generate_project()
    elif framework == "telebot":
        TelegramBotTemplate(project_location).generate_template()


if __name__ == "__main__":
    Main()