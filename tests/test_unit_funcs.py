import pytest

from recipe_hub import db, db_funcs
from recipe_hub.mappings import Unit
from tests import conftest

UNITS = [
    ({'name': 'test', 'symbol': 't'}, 't'),
    ({'name': 'test'}, ' test')
]


@pytest.mark.parametrize('unit_details, name', UNITS)
def test_get_unit_name(unit_details, name):
    unit = Unit(**unit_details)
    db.session.add(unit)
    db.session.commit()
    assert db_funcs.get_unit_name(unit.unit_id) == name
    conftest.delete(unit)


def test_get_unit_id():
    unit = Unit(name='test', symbol='t')
    db.session.add(unit)
    db.session.commit()
    assert db_funcs.get_unit_id('test') == unit.unit_id
    assert db_funcs.get_unit_id('t') == unit.unit_id
    conftest.delete(unit)


def test_get_all_units():
    amount = len(Unit.query.all())
    unit = Unit(name='test', symbol='t')
    db.session.add(unit)
    db.session.commit()
    units = db_funcs.get_all_units()
    assert len(units) == amount + 1
    assert all(map(lambda x: isinstance(x, str), units))
    conftest.delete(unit)