from recipe_hub import Base, app, engine
from recipe_hub.db_funcs import reset_units

UNITS = [('grams', 'g'), ('milliliter', 'ml'), ('whole')]

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    reset_units()
    app.run(threaded=True, port=5000, debug=True)