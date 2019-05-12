from flask_restplus import fields, Model

frequencies = Model('Frequencies',
    {
        'Burglary': fields.Integer,
        'Felony Assault': fields.Integer,
        'Grand Larceny': fields.Integer,
        'Kidnapping': fields.Integer,
        'Misdemeanor Assault': fields.Integer,
        'Misdemeanor Sex Crimes': fields.Integer,
        'Murder': fields.Integer,
        'Offenses against Public Order': fields.Integer,
        'Petit Larceny': fields.Integer,
        'Rape': fields.Integer,
        'Robbery': fields.Integer,
        'Shootings': fields.Integer
    }
)

crime = Model('Crime', 
    {
        "category": fields.String,
        "date": fields.String,
        "latitude": fields.Integer,
        "longitude": fields.Integer,
        "ofns_desc": fields.String,
        "pd_desc": fields.String
    }
)

station = Model('Station', 
    {
        "id": fields.Integer,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "lines": fields.List(fields.String),
        "name": fields.String,
        "percentile": fields.Float
    }
)

line = Model('Line', 
    {
        'direction': fields.String,
        'line': fields.String
    }
)

route = Model('Route', 
    {
        'leg': fields.Raw,
        'lines': fields.List( fields.Nested(line) ),
        'rating': fields.Float
    }
)

nearby_crime_response = Model('NearbyCrimeResponse', 
    {
        'frequencies': fields.Nested(frequencies),
        'results': fields.List(fields.Nested(crime))
    }
)

error_response = Model('Error', 
    {
        'error': fields.String
    }
)

def register_models(api):
    models = [
        frequencies,
        crime, 
        station,
        line,
        route,
        nearby_crime_response,
        error_response
    ]
    for model in models:
        api.models[model.name] = model