#------------------------------------------------------------------------------------------#
# This file is part of Pyccel which is released under MIT License. See the LICENSE file or #
# go to https://github.com/pyccel/pyccel/blob/master/LICENSE for full license details.     #
#------------------------------------------------------------------------------------------#
# pylint: disable=missing-function-docstring

"""
Handling the transitions between python code and C code.
"""

import numpy as np

from ..errors.errors   import Errors
from ..errors.messages import PYCCEL_RESTRICTION_TODO

from .datatypes import NativeInteger, NativeReal, NativeComplex
from .datatypes import NativeBool, NativeGeneric, NativeVoid

from .cwrapper  import PyccelPyObject, PyccelPyArrayObject

from .core      import FunctionCall, FunctionDef

from .variable  import Variable

errors = Errors()

__all__ = (
    'numpy_get_ndims',
    'numpy_get_data',
    'numpy_get_dim',
    'numpy_get_stride',
    'numpy_check_flag',
    'numpy_get_base',
    'numpy_itemsize',
    'numpy_flag_own_data',
    'numpy_flag_c_contig',
    'numpy_flag_f_contig',
    'numpy_dtype_registry',
)

PyArray_Type = Variable(NativeGeneric(), 'PyArray_Type')

#-------------------------------------------------------------------
#                      Numpy functions
#-------------------------------------------------------------------

numpy_get_ndims   = FunctionDef(name = 'PyArray_NDIM',
                           body      = [],
                           arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                           results   = [Variable(dtype=NativeInteger(), name = 'i')])

numpy_get_data    = FunctionDef(name = 'PyArray_DATA',
                           body      = [],
                           arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                           results   = [Variable(dtype=NativeGeneric(), name = 'v', rank=1)])

numpy_get_dim     = FunctionDef(name = 'PyArray_DIM',
                           body      = [],
                           arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True),
                                        Variable(dtype=NativeInteger(), name = 'idx')],
                           results   = [Variable(dtype=NativeInteger(), name = 'd')])

numpy_get_stride  = FunctionDef(name = 'PyArray_STRIDE',
                           body      = [],
                           arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True),
                                        Variable(dtype=NativeInteger(), name = 'idx')],
                           results   = [Variable(dtype=NativeInteger(), name = 's')])

numpy_get_strides = FunctionDef(name = 'PyArray_STRIDES',
                           body      = [],
                           arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                           results   = [Variable(dtype=NativeInteger(), name = 's', is_pointer=True)])

numpy_check_flag  = FunctionDef(name  = 'PyArray_CHKFLAGS',
                            body      = [],
                            arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True),
                                            Variable(dtype=NativeInteger(), name = 'flag')],
                            results   = [Variable(dtype=NativeBool(), name = 'i')])

numpy_get_base    = FunctionDef(name  = 'PyArray_BASE',
                            body      = [],
                            arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                            results   = [Variable(dtype=PyccelPyObject(), name = 'i')])

numpy_get_shape   = FunctionDef(name  = 'PyArray_SHAPE',
                            body      = [],
                            arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                            results   = [Variable(dtype=NativeInteger(), name = 'i', is_pointer=True)])

numpy_itemsize    = FunctionDef(name  = 'PyArray_ITEMSIZE',
                            body      = [],
                            arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                            results   = [Variable(dtype=NativeInteger(), name = 'i')])

numpy_get_size    = FunctionDef(name  = 'PyArray_SIZE',
                            body      = [],
                            arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                            results   = [Variable(dtype=NativeInteger(), name = 'i')])

numpy_nbytes      = FunctionDef(name  = 'PyArray_NBYTES',
                            body      = [],
                            arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                            results   = [Variable(dtype=NativeInteger(), name = 'i')])

numpy_get_type    = FunctionDef(name  = 'PyArray_TYPE',
                            body      = [],
                            arguments = [Variable(dtype=PyccelPyArrayObject(), name = 'o', is_pointer=True)],
                            results   = [Variable(dtype=NativeInteger(), name = 'i', precision = 4)])

numpy_flag_own_data     = Variable(dtype=NativeInteger(),  name = 'NPY_ARRAY_OWNDATA')
numpy_flag_c_contig     = Variable(dtype=NativeInteger(),  name = 'NPY_ARRAY_C_CONTIGUOUS')
numpy_flag_f_contig     = Variable(dtype=NativeInteger(),  name = 'NPY_ARRAY_F_CONTIGUOUS')
numpy_bool_type         = Variable(dtype=NativeInteger(),  name = 'NPY_BOOL', precision = 4)
numpy_byte_type         = Variable(dtype=NativeInteger(),  name = 'NPY_BYTE', precision = 4)
numpy_ubyte_type        = Variable(dtype=NativeInteger(),  name = 'NPY_UBYTE', precision = 4)
numpy_short_type        = Variable(dtype=NativeInteger(),  name = 'NPY_SHORT', precision = 4)
numpy_ushort_type       = Variable(dtype=NativeInteger(),  name = 'NPY_USHORT', precision = 4)
numpy_int_type          = Variable(dtype=NativeInteger(),  name = 'NPY_INT32', precision = 4)
numpy_uint_type         = Variable(dtype=NativeInteger(),  name = 'NPY_UINT', precision = 4)
numpy_long_type         = Variable(dtype=NativeInteger(),  name = 'NPY_LONG', precision = 4)
numpy_ulong_type        = Variable(dtype=NativeInteger(),  name = 'NPY_ULONG', precision = 4)
numpy_longlong_type     = Variable(dtype=NativeInteger(),  name = 'NPY_INT64', precision = 4)
numpy_ulonglong_type    = Variable(dtype=NativeInteger(),  name = 'NPY_ULONGLONG', precision = 4)
numpy_float_type        = Variable(dtype=NativeInteger(),  name = 'NPY_FLOAT', precision = 4)
numpy_double_type       = Variable(dtype=NativeInteger(),  name = 'NPY_DOUBLE', precision = 4)
numpy_longdouble_type   = Variable(dtype=NativeInteger(),  name = 'NPY_LONGDOUBLE', precision = 4)
numpy_cfloat_type       = Variable(dtype=NativeInteger(),  name = 'NPY_CFLOAT', precision = 4)
numpy_cdouble_type      = Variable(dtype=NativeInteger(),  name = 'NPY_CDOUBLE', precision = 4)
numpy_clongdouble_type  = Variable(dtype=NativeInteger(),  name = 'NPY_CLONGDOUBLE', precision = 4)

numpy_num_to_type = {0 : numpy_bool_type,
                     1 : numpy_byte_type,
                     2 : numpy_ubyte_type,
                     3 : numpy_short_type,
                     4 : numpy_ushort_type,
                     5 : numpy_int_type,
                     6 : numpy_uint_type,
                     7 : numpy_long_type,
                     8 : numpy_ulong_type,
                     9 : numpy_longlong_type,
                    10 : numpy_ulonglong_type,
                    11 : numpy_float_type,
                    12 : numpy_double_type,
                    13 : numpy_longdouble_type,
                    14 : numpy_cfloat_type,
                    15 : numpy_cdouble_type,
                    16 : numpy_clongdouble_type}

# This dictionary is required as the precision does not line up with the expected type on windows
numpy_int_type_precision_map = {
        1 : np.dtype(np.int8).num,
        2 : np.dtype(np.int16).num,
        4 : np.dtype(np.int32).num,
        8 : np.dtype(np.int64).num}

numpy_dtype_registry = {('bool',4)     : numpy_bool_type,
                        ('int',1)      : numpy_num_to_type[numpy_int_type_precision_map[1]],
                        ('int',2)      : numpy_num_to_type[numpy_int_type_precision_map[2]],
                        ('int',4)      : numpy_num_to_type[numpy_int_type_precision_map[4]],
                        ('int',8)      : numpy_num_to_type[numpy_int_type_precision_map[8]],
                        ('int',16)     : numpy_longlong_type,
                        ('real',4)     : numpy_float_type,
                        ('real',8)     : numpy_double_type,
                        ('real',16)    : numpy_longdouble_type,
                        ('complex',4)  : numpy_cfloat_type,
                        ('complex',8)  : numpy_cdouble_type,
                        ('complex',16) : numpy_clongdouble_type}

PyArray_CheckScalar   = FunctionDef(name      = 'PyArray_CheckScalar',
                                    body      = [],
                                    arguments = [Variable(dtype=PyccelPyObject(), name = 'o', is_pointer=True)],
                                    results   = [Variable(dtype=NativeBool(), name = 'r')])

PyArray_ScalarAsCtype = FunctionDef(name      = 'PyArray_ScalarAsCtype',
                                    body      = [],
                                    arguments = [Variable(dtype=PyccelPyObject(), name = 'o', is_pointer=True),
                                                Variable(dtype=NativeVoid(), name = 'c', is_pointer = True)],
                                    results   = [])

# construct the call of the function numpy_to_ndarray_strides
# (the function definition is available at pyccel/stdlib/ndarrays/ndarrays.c)
numpy_to_ndarray_strides = FunctionDef(name    = 'numpy_to_ndarray_strides',
                                    body       = [],
                                    arguments  = [Variable(dtype=NativeInteger(), name = 'np_strides', is_pointer=True),
                                                 Variable(dtype=NativeInteger(), name = 'type_size'),
                                                 Variable(dtype=NativeInteger(), name = 'nd')],
                                    results    = [Variable(dtype=NativeInteger(), name = 'nd_strides', is_pointer=True)])

# construct the call of the function numpy_to_ndarray_shape
# (the function definition is available at pyccel/stdlib/ndarrays/ndarrays.c)
numpy_to_ndarray_shape   = FunctionDef(name    = 'numpy_to_ndarray_shape',
                                    body       = [],
                                    arguments  = [Variable(dtype=NativeInteger(), name = 'np_shape', is_pointer=True),
                                                  Variable(dtype=NativeInteger(), name = 'nd')],
                                    results    = [Variable(dtype=NativeInteger(), name = 'nd_strides', is_pointer=True)])


# Needed to check for numpy arguments type
Numpy_Bool_ref       = Variable(dtype=NativeVoid(),  name = 'Bool')
Numpy_Int8_ref       = Variable(dtype=NativeVoid(),  name = 'Int8')
Numpy_Int16_ref      = Variable(dtype=NativeVoid(),  name = 'Int16')
Numpy_Int32_ref      = Variable(dtype=NativeVoid(),  name = 'Int32')
Numpy_Int64_ref      = Variable(dtype=NativeVoid(),  name = 'Int64')
Numpy_Float_ref      = Variable(dtype=NativeVoid(),  name = 'Float32')
Numpy_Double_ref     = Variable(dtype=NativeVoid(),  name = 'Float64')
Numpy_Complex64_ref  = Variable(dtype=NativeVoid(),  name = 'Complex64')
Numpy_Complex128_ref = Variable(dtype=NativeVoid(),  name = 'Complex128')

numpy_type_check_registry = {
    (NativeInteger(), 4)       : Numpy_Int32_ref,
    (NativeInteger(), 8)       : Numpy_Int64_ref,
    (NativeInteger(), 2)       : Numpy_Int16_ref,
    (NativeInteger(), 1)       : Numpy_Int8_ref,
    (NativeReal(), 8)          : Numpy_Double_ref,
    (NativeReal(), 4)          : Numpy_Float_ref,
    (NativeComplex(), 4)       : Numpy_Complex64_ref,
    (NativeComplex(), 8)       : Numpy_Complex128_ref,
    (NativeBool(), 4)          : Numpy_Bool_ref
}