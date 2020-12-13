from recipe_hub import app, db
from recipe_hub.db_funcs import reset_units

UNITS = [('grams', 'g'), ('milliliter', 'ml'), ('whole')]

if __name__ == '__main__':
    db.create_all()
    reset_units(UNITS)
    app.run(threaded=True, port=5000)