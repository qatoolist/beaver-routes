import pytest
from beaver_routes.core.attribute_dictionary import AttributeDictionary

class TestAttributeDictionary:
    
    def test_initialization(self):
        ad = AttributeDictionary()
        assert ad._data == {}
        
        data = {'a': 1, 'b': 2}
        ad = AttributeDictionary(data)
        assert ad._data == {'a': 1, 'b': 2}

    def test_getattr(self):
        ad = AttributeDictionary()
        ad.some_attr = 42
        assert ad.some_attr == 42
        
        assert isinstance(ad.non_existing_attr, AttributeDictionary)
        assert ad.non_existing_attr._data == {}

    def test_setattr(self):
        ad = AttributeDictionary()
        ad.some_attr = 42
        assert ad._data['some_attr'] == 42
        
        ad.nested_attr = {'x': 1}
        assert isinstance(ad.nested_attr, AttributeDictionary)
        assert ad.nested_attr._data == {'x': 1}

    def test_getitem(self):
        data = {'a': 1, 'b': {'x': 10}}
        ad = AttributeDictionary(data)
        assert ad['a'] == 1
        assert isinstance(ad['b'], AttributeDictionary)
        assert ad['b'].to_dict() == {'x': 10}

    def test_setitem(self):
        ad = AttributeDictionary()
        ad['key'] = 'value'
        assert ad._data['key'] == 'value'
        
        ad['nested'] = {'inner_key': 'inner_value'}
        assert isinstance(ad._data['nested'], AttributeDictionary)
        assert ad['nested'].to_dict() == {'inner_key': 'inner_value'}

    def test_contains(self):
        data = {'a': 1, 'b': 2}
        ad = AttributeDictionary(data)
        assert 'a' in ad
        assert 'c' not in ad

    def test_wrap(self):
        ad = AttributeDictionary()
        wrapped = ad._wrap({'key': 'value'})
        assert isinstance(wrapped, AttributeDictionary)
        assert wrapped.to_dict() == {'key': 'value'}
        
        not_wrapped = ad._wrap(42)
        assert not_wrapped == 42

    def test_to_dict(self):
        data = {'a': 1, 'b': {'x': 10, 'y': 20}}
        ad = AttributeDictionary(data)
        assert ad.to_dict() == {'a': 1, 'b': {'x': 10, 'y': 20}}
        
        ad_with_invalid_keys = AttributeDictionary({'items': 1, 'keys': 2})
        with pytest.raises(AttributeError):
            ad_with_invalid_keys.to_dict()

    def test_repr(self):
        data = {'a': 1, 'b': 2}
        ad = AttributeDictionary(data)
        assert repr(ad) == repr(data)

    def test_str(self):
        data = {'a': 1, 'b': 2}
        ad = AttributeDictionary(data)
        assert str(ad) == str(data)
