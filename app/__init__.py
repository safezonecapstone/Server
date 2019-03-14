from flask import Flask, render_template, request, Blueprint
from app.routes.crimes import CrimeRouter
from app.routes.stations import StationRouter

app = Flask(__name__)

app.register_blueprint(CrimeRouter)
app.register_blueprint(StationRouter)

# TRAIN_LINE 
# Possible values:
# ----

# CRIME_NAME
# Possible values:
# ----

# timeSpan
# Possible Values:
# 'YEAR' - Year To Date
# 'MONT' - Last 28 Days
# 'WEEK' - Week To Date

@app.route('/', methods=['GET'])
def index():
    return '''
        <div style="text-align:center">
            <h1>Flask Server Running in Dev Mode</h1>
            <h2>Change value of FLASK_ENV in the .flaskenv file to run in Production Mode</h2>
        </div>
    '''