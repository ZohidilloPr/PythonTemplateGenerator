
import os

packeges_list = [
    "django", "django-cors-headers", "whitenoise", "drf-spectacular", 
    "drf-spectacular[sidecar]", "gunicorn", "djangorestframework",
    "markdown", "django-filter", "psycopg2-binary", "python-decouple",
    "django-quill-editor"
]

with open(f"{os.path.expanduser('~')}/Desktop/PythonTemplateGenerator/requarements.txt", "w") as file:
    for i in packeges_list:
        file.write(f"{i}\n")