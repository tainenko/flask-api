from main import init_app
import os
app = init_app(os.environ.get('FLASK_ENV',"test"))
