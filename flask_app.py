# This file is used for hosting at PythonAnywhere.com
# 'app' must point to a Flask Application object.

from app import create_app

app=create_app()
app.run(host='127.0.0.1',port='2000')

