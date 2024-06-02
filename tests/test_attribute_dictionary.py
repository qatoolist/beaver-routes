import pytest

from beaver_routes.core.attribute_dictionary import AttributeDictionary


class TestAttributeDictionary:

    def test_initialization(self) -> None:
        ad = AttributeDictionary()
        assert ad._data == {}

        data = {"a": 1, "b": 2}
        ad = AttributeDictionary(data)
        assert ad._data == {"a": 1, "b": 2}

    def test_getattr(self) -> None:
        ad = AttributeDictionary()
        ad.some_attr = 42
        assert ad.some_attr == 42

        assert isinstance(ad.non_existing_attr, AttributeDictionary)
        assert ad.non_existing_attr._data == {}

    def test_setattr(self) -> None:
        ad = AttributeDictionary()
        ad.some_attr = 42
        assert ad._data["some_attr"] == 42

        ad.nested_attr = {"x": 1}
        assert isinstance(ad.nested_attr, AttributeDictionary)
        assert ad.nested_attr._data == {"x": 1}

    def test_getitem(self) -> None:
        data = {"a": 1, "b": {"x": 10}}
        ad = AttributeDictionary(data)
        assert ad["a"] == 1
        assert isinstance(ad["b"], AttributeDictionary)
        assert ad["b"].to_dict() == {"x": 10}

    def test_setitem(self) -> None:
        ad = AttributeDictionary()
        ad["key"] = "value"
        assert ad._data["key"] == "value"

        ad["nested"] = {"inner_key": "inner_value"}
        assert isinstance(ad._data["nested"], AttributeDictionary)
        assert ad["nested"].to_dict() == {"inner_key": "inner_value"}

    def test_contains(self) -> None:
        data = {"a": 1, "b": 2}
        ad = AttributeDictionary(data)
        assert "a" in ad
        assert "c" not in ad

    def test_wrap(self) -> None:
        ad = AttributeDictionary()
        wrapped = ad._wrap({"key": "value"})
        assert isinstance(wrapped, AttributeDictionary)
        assert wrapped.to_dict() == {"key": "value"}

        not_wrapped = ad._wrap(42)
        assert not_wrapped == 42

    def test_to_dict(self) -> None:
        data = {"a": 1, "b": {"x": 10, "y": 20}}
        ad = AttributeDictionary(data)
        assert ad.to_dict() == {"a": 1, "b": {"x": 10, "y": 20}}

        ad_with_invalid_keys = AttributeDictionary({"items": 1, "keys": 2})
        with pytest.raises(AttributeError):
            ad_with_invalid_keys.to_dict()

    def test_repr(self) -> None:
        data = {"a": 1, "b": 2}
        ad = AttributeDictionary(data)
        assert repr(ad) == repr(data)

    def test_str(self) -> None:
        data = {"a": 1, "b": 2}
        ad = AttributeDictionary(data)
        assert str(ad) == str(data)

    def test_deep_nested_structure(self) -> None:
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": 42
                    }
                }
            }
        }
        ad = AttributeDictionary(data)
        assert ad.level1.level2.level3.value == 42
        assert ad.to_dict() == data

    def test_update_nested_structure(self) -> None:
        ad = AttributeDictionary()
        ad.level1.level2.level3.value = 42
        assert ad.level1.level2.level3.value == 42

        ad.level1.level2.new_value = "test"
        assert ad.level1.level2.new_value == "test"

        expected_dict = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": 42
                    },
                    "new_value": "test"
                }
            }
        }
        assert ad.to_dict() == expected_dict

    def test_complex_structure(self) -> None:
        data = {
            "a": 1,
            "b": {
                "x": 10,
                "y": {
                    "nested": {
                        "value": 42
                    }
                }
            },
            "c": [1, 2, 3],
            "d": {"e": {"f": {"g": "value"}}}
        }
        ad = AttributeDictionary(data)
        assert ad.b.y.nested.value == 42
        assert ad.c == [1, 2, 3]
        assert ad.d.e.f.g == "value"
        assert ad.to_dict() == data

    def test_list_in_dictionary(self) -> None:
        data = {"list_key": [1, 2, {"nested_key": "nested_value"}]}
        ad = AttributeDictionary(data)
        assert ad.list_key == [1, 2, {"nested_key": "nested_value"}]

        ad.list_key.append(3)
        assert ad.list_key == [1, 2, {"nested_key": "nested_value"}, 3]
        assert ad.to_dict() == {"list_key": [1, 2, {"nested_key": "nested_value"}, 3]}
