from recipe_hub import app, db
from recipe_hub.db_funcs import reset_units

UNITS = [{'name': 'grams', 'symbol': 'g'},
         {'name': 'milliliter', 'symbol': 'ml'},
         {'name': 'whole'}]

if __name__ == '__main__':
    db.create_all()
    reset_units(UNITS)
    app.run(threaded=True, port=5000)