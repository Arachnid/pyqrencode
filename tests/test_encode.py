
import qrencode

def test_encode_string(value='data'):
    assert qrencode.encode(value)
