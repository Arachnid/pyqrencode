import sys
from PIL import Image
from . import _qrencode

if sys.version_info >= (3,):
    unicode = str
    basestring = (str, bytes)

QR_ECLEVEL_L = 0
QR_ECLEVEL_M = 1
QR_ECLEVEL_Q = 2
QR_ECLEVEL_H = 3
levels = [QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_Q, QR_ECLEVEL_H]


QR_MODE_8 = 2
QR_MODE_KANJI = 3
hints = [QR_MODE_8, QR_MODE_KANJI]


def encode(data, version=0, level=QR_ECLEVEL_L, hint=QR_MODE_8,
           case_sensitive=True):
    """Creates a QR-Code from string data.

    Args:
      data: string: The data to encode in a QR-code. If a unicode string is
          supplied, it will be encoded in UTF-8. Raw bytes are also supported.
      version: int: The minimum version to use. If set to 0, the library picks
          the smallest version that the data fits in.
      level: int: Error correction level. Defaults to 'L'.
      hint: int: The type of data to encode. Either QR_MODE_8 or QR_MODE_KANJI.
      case_sensitive: bool: Should string data be encoded case-preserving?
    Returns:
      A (version, size, image) tuple, where image is a size*size PIL image of
      the QR-code.
    """
    if isinstance(data, unicode):
        data = data.encode('utf8')
    elif not isinstance(data, basestring):
        raise ValueError('data argument must be a string or bytes.')
    if not data:
        raise ValueError('data argument cannot be empty.')
    version = int(version)
    if level not in levels:
        raise ValueError('Invalid error-correction level.')
    if hint not in hints:
        raise ValueError('Invalid encoding mode.')
    try:
        output = _qrencode.encode(data, version, level, hint, case_sensitive)
    except (ValueError, TypeError):
        output = _qrencode.encode_bytes(data, version, level)
    if not output:
        raise ValueError('Error generating QR-Code.')
    version, size, data = output

    im = Image.frombytes('L', (size, size), data)
    return (version, size, im)


def encode_scaled(data, size, version=0, level=QR_ECLEVEL_L, hint=QR_MODE_8,
                  case_sensitive=True):
    """Creates a QR-code from string data, resized to the specified dimensions.

    Args:
      data: string: The data to encode in a QR-code. If a unicode string is
          supplied, it will be encoded in UTF-8. Raw bytes are also supported.
      size: int: Output size. If this is not an exact multiple of the QR-code's
          dimensions, padding will be added. If this is smaller than the
          QR-code's dimensions, it is ignored.
      version: int: The minimum version to use. If set to 0, the library picks
          the smallest version that the data fits in.
      level: int: Error correction level. Defaults to 'L'.
      hint: int: The type of data to encode. Either QR_MODE_8 or QR_MODE_KANJI.
      case_sensitive: bool: Should string data be encoded case-preserving?
    Returns:
      A (version, size, image) tuple, where image is a size*size PIL image of
      the QR-code.
    """
    version, src_size, im = encode(data, version, level, hint, case_sensitive)
    if size < src_size:
        size = src_size
    qr_size = (size / src_size) * src_size
    im = im.resize((qr_size, qr_size), Image.NEAREST)
    pad = (size - qr_size) / 2
    ret = Image.new("L", (size, size), 255)
    ret.paste(im, (pad, pad))

    return (version, size, ret)
