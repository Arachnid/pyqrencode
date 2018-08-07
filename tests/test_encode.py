
import qrencode

import hypothesis as ht
from hypothesis import strategies as st


@ht.given(st.text())
def test_encode_string(value):
    assert qrencode.encode(value)
