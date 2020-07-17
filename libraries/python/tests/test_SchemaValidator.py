import validator as validator
import json
import utils.utils as utils
import os


def test_validator():
    """Test SchemaValidator.
    Procedure:
        - Create a new validator.
        - Create shacl constraints with error of severity:
            * Violation
            * Warning
            * Info
        - Create an entity with error in a literal.
        - Create an entity with nested error(inside a object).
        - Create an entity that has errors in multiple objects that belong to
          same attribute.
        - Make sure these errors are of varying severity.
        - Validate all entities.

    Verification:
        - Check if all errors are detected.
        - Check if the paths of nested errors are identfied properly.
        - Check if multiple invalid objects within same attribute throw
          multiple errors.
        - Check if the conformance is false only if severity is Violation.
        - Check if messages are identified properly.
    """
    v = validator.SchemaValidator(
        './tests/files/validator_constraints.ttl',
        './tests/files/test_report.html')

    with open('./tests/files/validator_data_feed.json') as f:
        dump = json.load(f)

    expected_conformance = [False, True, True]
    out_conformance = []

    for m in dump['dataFeedElement']:
        out_conformance.append(v.add_entity(m))

    assert expected_conformance == out_conformance, 'Expected and returned conformance dont match.'

    v.close()
    os.remove('./tests/files/test_report.html')

    expected = []
    expected.append(utils.ResultRow(
        'Id: movieid1',
        'Name of movie must be string.',
        '.name',
        '123',
        'Violation'
    ))
    expected.append(utils.ResultRow(
        'Id: id2',
        'Name of person must be string.',
        '.actor.name',
        '123',
        'Warning'
    ))
    expected.append(utils.ResultRow(
        'Id: id3',
        'Name of organization must be string.',
        '.creator.url',
        '345',
        'Info'
    ))
    expected.append(utils.ResultRow(
        'Id: id3',
        'Name of person must be string.',
        '.creator.name',
        '123',
        'Warning'
    ))

    assert(len(v.reports['Movie']) == len(expected)
           ), 'Expected report count not equal.'

    for m in expected:
        assert m in v.reports['Movie'], 'Expected report not generated.'


def test_validator_datafeed():
    """Test SchemaValidator with DataFeed.
    Procedure:
        - Create a new validator.
        - Create shacl constraints with error of severity:
            * Violation
            * Warning
            * Info
        - Create a datafeed.
        - Add an entity with error in a literal.
        - Add an entity with nested error(inside a object).
        - Add an entity that has errors in multiple objects that belong to same
          attribute.
        - Make sure these errors are of varying severity.
        - Validate datafeed.

    Verification:
        - Check if all errors within the nested feeds are detected.
        - Check if the paths of nested errors are identfied properly.
        - Check if multiple invalid objects within same attribute throw
          multiple errors.
        - Check if the conformance is false only if severity is Violation.
        - Check if messages are identified properly.
    """

    v = validator.SchemaValidator(
        './tests/files/validator_constraints.ttl',
        './tests/files/test_report.html')

    with open('./tests/files/validator_data_feed.json') as f:
        dump = json.load(f)

    v.add_entity(dump)
    v.close()
    os.remove('./tests/files/test_report.html')

    expected = []
    expected.append(utils.ResultRow(
        'Id: movieid1',
        'Name of movie must be string.',
        '.name',
        '123',
        'Violation'
    ))
    expected.append(utils.ResultRow(
        'Id: id2',
        'Name of person must be string.',
        '.actor.name',
        '123',
        'Warning'
    ))
    expected.append(utils.ResultRow(
        'Id: id3',
        'Name of organization must be string.',
        '.creator.url',
        '345',
        'Info'
    ))
    expected.append(utils.ResultRow(
        'Id: id3',
        'Name of person must be string.',
        '.creator.name',
        '123',
        'Warning'
    ))

    assert(len(v.reports['Movie']) == len(expected)
           ), 'Expected report count not equal.'

    for m in expected:
        assert m in v.reports['Movie'], 'Expected report not generated.'


def test_validator_itemlist():
    """Test SchemaValidator with ItemList.
    Procedure:
        - Create a new validator.
        - Create shacl constraints with error of severity:
            * Violation
            * Warning
            * Info
        - Create a itemlist.
        - Add an entity with error in a literal.
        - Add an entity with nested error(inside a object).
        - Add an entity that has errors in multiple objects that belong to
          same attribute.
        - Make sure these errors are of varying severity.
        - Validate itemlist.

    Verification:
        - Check if all errors within the nested items are detected.
        - Check if the paths of nested errors are identfied properly.
        - Check if multiple invalid objects within same attribute throw
          multiple errors.
        - Check if the conformance is false only if severity is Violation.
        - Check if messages are identified properly.
    """

    v = validator.SchemaValidator(
        './tests/files/validator_constraints.ttl',
        './tests/files/test_report.html')

    with open('./tests/files/validator_item_list.json') as f:
        dump = json.load(f)

    v.add_entity(dump)
    v.close()
    os.remove('./tests/files/test_report.html')

    expected = []
    expected.append(utils.ResultRow(
        'Id: movieid1',
        'Name of movie must be string.',
        '.name',
        '123',
        'Violation'
    ))
    expected.append(utils.ResultRow(
        'Id: id2',
        'Name of person must be string.',
        '.actor.name',
        '123',
        'Warning'
    ))
    expected.append(utils.ResultRow(
        'Id: id3',
        'Name of organization must be string.',
        '.creator.url',
        '345',
        'Info'
    ))
    expected.append(utils.ResultRow(
        'Id: id3',
        'Name of person must be string.',
        '.creator.name',
        '123',
        'Warning'
    ))

    assert(len(v.reports['Movie']) == len(expected)
           ), 'Expected report count not equal.'

    for m in expected:
        assert m in v.reports['Movie'], 'Expected report not generated.'
