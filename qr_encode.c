#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <qrencode.h>

#if PY_MAJOR_VERSION >= 3
#  define BYTES "y"
#else
#  define BYTES "s"
#endif

static PyObject *encode(PyObject *self, PyObject *args)
{
    char *str;
    int i, version, level, hint, case_sensitive, num_pixels;
    QRcode *code;
    PyObject *ret;

    if(!PyArg_ParseTuple(args, BYTES "iiii:_qrencode.encode",
                         &str, &version, &level, &hint, &case_sensitive))
        return NULL;

    code = QRcode_encodeString(str, version, level, hint, case_sensitive);
    if (!code) {
        return Py_BuildValue("");
    }

    num_pixels = code->width * code->width;
    for(i = 0; i < num_pixels; i++)
      code->data[i] = 255 - (code->data[i] & 0x1) * 0xFF;

    ret = Py_BuildValue("(ii" BYTES "#)", code->version, code->width,
                        code->data, num_pixels);
    QRcode_free(code);
    return ret;
};

static PyObject *encode_bytes(PyObject *self, PyObject *args)
{
    char *str;
    int size, i, version, level, num_pixels;
    QRcode *code;
    PyObject *ret;

    if(!PyArg_ParseTuple(args, BYTES "#ii:_qrencode.encode",
                         &str, &size, &version, &level))
        return NULL;

    code = QRcode_encodeData(size, str, version, level);
    if (!code) {
        return Py_BuildValue("");
    }

    num_pixels = code->width * code->width;
    for(i = 0; i < num_pixels; i++)
      code->data[i] = 255 - (code->data[i] & 0x1) * 0xFF;

    ret = Py_BuildValue("(ii" BYTES "#)", code->version, code->width,
                        code->data, num_pixels);
    QRcode_free(code);
    return ret;
};

static PyMethodDef methods[] =
{
    {"encode", encode, METH_VARARGS, "Encodes a string as a QR-code. Returns a tuple of (version, width, data)"},
    {"encode_bytes", encode_bytes, METH_VARARGS, "Encodes raw bytes as a QR-code. Returns a tuple of (version, width, data)"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "qrencode._qrencode",
    NULL,
    -1,
    methods,
};

PyMODINIT_FUNC
PyInit__qrencode(void)
{
    return PyModule_Create(&module);
}

#else

PyMODINIT_FUNC
init_qrencode(void)
{
    Py_InitModule("qrencode._qrencode", methods);
}

#endif
