
import pytest
import qrencode

import hypothesis as ht
from hypothesis import strategies as st

falsy_values = st.one_of(
    st.none(), st.just(False), st.just(0), st.just(''),
    st.just(dict()), st.just(list()), st.just(tuple()), st.just(set())
)


@ht.given(st.text(min_size=1))
def test_encode_string(value):
    assert qrencode.encode(value)


@ht.given(st.binary(min_size=1))
def test_encode_bytes(value):
    assert qrencode.encode(value)


@ht.given(falsy_values)
def test_encode_invalid_data(value):
    with pytest.raises(ValueError):
        qrencode.encode(value)
