import pytest
from datetime import date, datetime
from cerberus import DocumentError

from .example_data_sets import ExampleDataSet


class TestDataSet:
    generic_example_raw_data = {
        "key_string": "abc",
        "key_none_string": None,
        "key_nullable_string": "",
        "key_uuid_string": "7c674878-e544-431c-8c11-f11565299cac",
        "key_integer": 5,
        "key_none_integer": None,
        "key_nullable_integer": "",
        "key_bool": "True",
        "key_none_bool": None,
        "key_float": "7.5",
        "key_none_float": None,
        "key_nullable_float": "",
        "key_date": "1900-01-31",
        "key_none_date": None,
        "key_datetime": "1900-01-31T09:30:00.532649",
        "key_none_datetime": None,
    }
    generic_expected_data = {
        "key_string": "abc",
        "key_none_string": "",
        "key_nullable_string": None,
        "key_uuid_string": "7c674878-e544-431c-8c11-f11565299cac",
        "key_integer": 5,
        "key_none_integer": 0,
        "key_nullable_integer": None,
        "key_bool": True,
        "key_none_bool": False,
        "key_float": 7.5,
        "key_none_float": 0.0,
        "key_nullable_float": None,
        "key_date": date.fromisoformat("1900-01-31"),
        "key_none_date": None,
        "key_datetime": datetime.fromisoformat("1900-01-31T09:30:00.532649"),
        "key_none_datetime": None,
    }

    def test_full_valid_data_set(self):
        validated_data_set = ExampleDataSet.validate_object(
            TestDataSet.generic_example_raw_data
        )
        assert validated_data_set == TestDataSet.generic_expected_data

    def test_partial_valid_data_set(self):
        example_raw_data = {
            "key_string": "abc",
        }
        expected_data = {
            "key_string": "abc",
        }
        validated_data_set = ExampleDataSet.validate_object(example_raw_data)
        assert validated_data_set == expected_data

    def test_unknown_key(self):
        example_raw_data = {
            "unknown_key": "",
        }
        with pytest.raises(DocumentError):
            ExampleDataSet.validate_object(example_raw_data)

    def test_list_unknown_key(self):
        example_raw_data = {
            "unknown_key": "",
        }
        with pytest.raises(DocumentError):
            ExampleDataSet.validate_objects([example_raw_data])

    def test_validate_list(self):
        validated_data_set = ExampleDataSet.validate_objects(
            [TestDataSet.generic_example_raw_data, TestDataSet.generic_example_raw_data]
        )
        assert validated_data_set == [
            TestDataSet.generic_expected_data,
            TestDataSet.generic_expected_data,
        ]

    def test_validate_data_object(self):
        validated_data_set = ExampleDataSet.validate_one(
            {"data": [TestDataSet.generic_example_raw_data]}
        )
        assert validated_data_set == TestDataSet.generic_expected_data

    def test_validate_data_list(self):
        validated_data_set = ExampleDataSet.validate_many(
            {
                "data": [
                    TestDataSet.generic_example_raw_data,
                    TestDataSet.generic_example_raw_data,
                ]
            }
        )
        assert validated_data_set == [
            TestDataSet.generic_expected_data,
            TestDataSet.generic_expected_data,
        ]

    def test_one_missing_data_key(self):
        validate_data_set = ExampleDataSet.validate_one({"NOT_DATA": []})
        assert validate_data_set == {}

    def test_many_missing_data_key(self):
        validate_data_set = ExampleDataSet.validate_many({"NOT_DATA": []})
        assert validate_data_set == []
