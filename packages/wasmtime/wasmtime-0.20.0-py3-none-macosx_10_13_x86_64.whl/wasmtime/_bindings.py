# flake8: noqa
#
# This is a procedurally generated file, DO NOT EDIT
# instead edit `./bindgen.py` at the root of the repo

from ctypes import *
from typing import Any
from ._ffi import dll, wasm_val_t, wasm_ref_t

wasm_byte_t = c_ubyte

class wasm_byte_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(wasm_byte_t)),
    ]

_wasm_byte_vec_new_empty = dll.wasm_byte_vec_new_empty
_wasm_byte_vec_new_empty.restype = None
_wasm_byte_vec_new_empty.argtypes = [POINTER(wasm_byte_vec_t)]
def wasm_byte_vec_new_empty(out: Any) -> None:
    return _wasm_byte_vec_new_empty(out)  # type: ignore

_wasm_byte_vec_new_uninitialized = dll.wasm_byte_vec_new_uninitialized
_wasm_byte_vec_new_uninitialized.restype = None
_wasm_byte_vec_new_uninitialized.argtypes = [POINTER(wasm_byte_vec_t), c_size_t]
def wasm_byte_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_byte_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_byte_vec_new = dll.wasm_byte_vec_new
_wasm_byte_vec_new.restype = None
_wasm_byte_vec_new.argtypes = [POINTER(wasm_byte_vec_t), c_size_t, POINTER(wasm_byte_t)]
def wasm_byte_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_byte_vec_new(out, arg1, arg2)  # type: ignore

_wasm_byte_vec_copy = dll.wasm_byte_vec_copy
_wasm_byte_vec_copy.restype = None
_wasm_byte_vec_copy.argtypes = [POINTER(wasm_byte_vec_t), POINTER(wasm_byte_vec_t)]
def wasm_byte_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_byte_vec_copy(out, arg1)  # type: ignore

_wasm_byte_vec_delete = dll.wasm_byte_vec_delete
_wasm_byte_vec_delete.restype = None
_wasm_byte_vec_delete.argtypes = [POINTER(wasm_byte_vec_t)]
def wasm_byte_vec_delete(arg0: Any) -> None:
    return _wasm_byte_vec_delete(arg0)  # type: ignore

wasm_name_t = wasm_byte_vec_t

class wasm_config_t(Structure):
    pass

_wasm_config_delete = dll.wasm_config_delete
_wasm_config_delete.restype = None
_wasm_config_delete.argtypes = [POINTER(wasm_config_t)]
def wasm_config_delete(arg0: Any) -> None:
    return _wasm_config_delete(arg0)  # type: ignore

_wasm_config_new = dll.wasm_config_new
_wasm_config_new.restype = POINTER(wasm_config_t)
_wasm_config_new.argtypes = []
def wasm_config_new() -> pointer:
    return _wasm_config_new()  # type: ignore

class wasm_engine_t(Structure):
    pass

_wasm_engine_delete = dll.wasm_engine_delete
_wasm_engine_delete.restype = None
_wasm_engine_delete.argtypes = [POINTER(wasm_engine_t)]
def wasm_engine_delete(arg0: Any) -> None:
    return _wasm_engine_delete(arg0)  # type: ignore

_wasm_engine_new = dll.wasm_engine_new
_wasm_engine_new.restype = POINTER(wasm_engine_t)
_wasm_engine_new.argtypes = []
def wasm_engine_new() -> pointer:
    return _wasm_engine_new()  # type: ignore

_wasm_engine_new_with_config = dll.wasm_engine_new_with_config
_wasm_engine_new_with_config.restype = POINTER(wasm_engine_t)
_wasm_engine_new_with_config.argtypes = [POINTER(wasm_config_t)]
def wasm_engine_new_with_config(arg0: Any) -> pointer:
    return _wasm_engine_new_with_config(arg0)  # type: ignore

class wasm_store_t(Structure):
    pass

_wasm_store_delete = dll.wasm_store_delete
_wasm_store_delete.restype = None
_wasm_store_delete.argtypes = [POINTER(wasm_store_t)]
def wasm_store_delete(arg0: Any) -> None:
    return _wasm_store_delete(arg0)  # type: ignore

_wasm_store_new = dll.wasm_store_new
_wasm_store_new.restype = POINTER(wasm_store_t)
_wasm_store_new.argtypes = [POINTER(wasm_engine_t)]
def wasm_store_new(arg0: Any) -> pointer:
    return _wasm_store_new(arg0)  # type: ignore

wasm_mutability_t = c_uint8

class wasm_limits_t(Structure):
    _fields_ = [
        ("min", c_uint32),
        ("max", c_uint32),
    ]

class wasm_valtype_t(Structure):
    pass

_wasm_valtype_delete = dll.wasm_valtype_delete
_wasm_valtype_delete.restype = None
_wasm_valtype_delete.argtypes = [POINTER(wasm_valtype_t)]
def wasm_valtype_delete(arg0: Any) -> None:
    return _wasm_valtype_delete(arg0)  # type: ignore

class wasm_valtype_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_valtype_t))),
    ]

_wasm_valtype_vec_new_empty = dll.wasm_valtype_vec_new_empty
_wasm_valtype_vec_new_empty.restype = None
_wasm_valtype_vec_new_empty.argtypes = [POINTER(wasm_valtype_vec_t)]
def wasm_valtype_vec_new_empty(out: Any) -> None:
    return _wasm_valtype_vec_new_empty(out)  # type: ignore

_wasm_valtype_vec_new_uninitialized = dll.wasm_valtype_vec_new_uninitialized
_wasm_valtype_vec_new_uninitialized.restype = None
_wasm_valtype_vec_new_uninitialized.argtypes = [POINTER(wasm_valtype_vec_t), c_size_t]
def wasm_valtype_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_valtype_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_valtype_vec_new = dll.wasm_valtype_vec_new
_wasm_valtype_vec_new.restype = None
_wasm_valtype_vec_new.argtypes = [POINTER(wasm_valtype_vec_t), c_size_t, POINTER(POINTER(wasm_valtype_t))]
def wasm_valtype_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_valtype_vec_new(out, arg1, arg2)  # type: ignore

_wasm_valtype_vec_copy = dll.wasm_valtype_vec_copy
_wasm_valtype_vec_copy.restype = None
_wasm_valtype_vec_copy.argtypes = [POINTER(wasm_valtype_vec_t), POINTER(wasm_valtype_vec_t)]
def wasm_valtype_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_valtype_vec_copy(out, arg1)  # type: ignore

_wasm_valtype_vec_delete = dll.wasm_valtype_vec_delete
_wasm_valtype_vec_delete.restype = None
_wasm_valtype_vec_delete.argtypes = [POINTER(wasm_valtype_vec_t)]
def wasm_valtype_vec_delete(arg0: Any) -> None:
    return _wasm_valtype_vec_delete(arg0)  # type: ignore

_wasm_valtype_copy = dll.wasm_valtype_copy
_wasm_valtype_copy.restype = POINTER(wasm_valtype_t)
_wasm_valtype_copy.argtypes = [POINTER(wasm_valtype_t)]
def wasm_valtype_copy(arg0: Any) -> pointer:
    return _wasm_valtype_copy(arg0)  # type: ignore

wasm_valkind_t = c_uint8

_wasm_valtype_new = dll.wasm_valtype_new
_wasm_valtype_new.restype = POINTER(wasm_valtype_t)
_wasm_valtype_new.argtypes = [wasm_valkind_t]
def wasm_valtype_new(arg0: Any) -> pointer:
    return _wasm_valtype_new(arg0)  # type: ignore

_wasm_valtype_kind = dll.wasm_valtype_kind
_wasm_valtype_kind.restype = wasm_valkind_t
_wasm_valtype_kind.argtypes = [POINTER(wasm_valtype_t)]
def wasm_valtype_kind(arg0: Any) -> wasm_valkind_t:
    return _wasm_valtype_kind(arg0)  # type: ignore

class wasm_functype_t(Structure):
    pass

_wasm_functype_delete = dll.wasm_functype_delete
_wasm_functype_delete.restype = None
_wasm_functype_delete.argtypes = [POINTER(wasm_functype_t)]
def wasm_functype_delete(arg0: Any) -> None:
    return _wasm_functype_delete(arg0)  # type: ignore

class wasm_functype_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_functype_t))),
    ]

_wasm_functype_vec_new_empty = dll.wasm_functype_vec_new_empty
_wasm_functype_vec_new_empty.restype = None
_wasm_functype_vec_new_empty.argtypes = [POINTER(wasm_functype_vec_t)]
def wasm_functype_vec_new_empty(out: Any) -> None:
    return _wasm_functype_vec_new_empty(out)  # type: ignore

_wasm_functype_vec_new_uninitialized = dll.wasm_functype_vec_new_uninitialized
_wasm_functype_vec_new_uninitialized.restype = None
_wasm_functype_vec_new_uninitialized.argtypes = [POINTER(wasm_functype_vec_t), c_size_t]
def wasm_functype_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_functype_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_functype_vec_new = dll.wasm_functype_vec_new
_wasm_functype_vec_new.restype = None
_wasm_functype_vec_new.argtypes = [POINTER(wasm_functype_vec_t), c_size_t, POINTER(POINTER(wasm_functype_t))]
def wasm_functype_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_functype_vec_new(out, arg1, arg2)  # type: ignore

_wasm_functype_vec_copy = dll.wasm_functype_vec_copy
_wasm_functype_vec_copy.restype = None
_wasm_functype_vec_copy.argtypes = [POINTER(wasm_functype_vec_t), POINTER(wasm_functype_vec_t)]
def wasm_functype_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_functype_vec_copy(out, arg1)  # type: ignore

_wasm_functype_vec_delete = dll.wasm_functype_vec_delete
_wasm_functype_vec_delete.restype = None
_wasm_functype_vec_delete.argtypes = [POINTER(wasm_functype_vec_t)]
def wasm_functype_vec_delete(arg0: Any) -> None:
    return _wasm_functype_vec_delete(arg0)  # type: ignore

_wasm_functype_copy = dll.wasm_functype_copy
_wasm_functype_copy.restype = POINTER(wasm_functype_t)
_wasm_functype_copy.argtypes = [POINTER(wasm_functype_t)]
def wasm_functype_copy(arg0: Any) -> pointer:
    return _wasm_functype_copy(arg0)  # type: ignore

_wasm_functype_new = dll.wasm_functype_new
_wasm_functype_new.restype = POINTER(wasm_functype_t)
_wasm_functype_new.argtypes = [POINTER(wasm_valtype_vec_t), POINTER(wasm_valtype_vec_t)]
def wasm_functype_new(params: Any, results: Any) -> pointer:
    return _wasm_functype_new(params, results)  # type: ignore

_wasm_functype_params = dll.wasm_functype_params
_wasm_functype_params.restype = POINTER(wasm_valtype_vec_t)
_wasm_functype_params.argtypes = [POINTER(wasm_functype_t)]
def wasm_functype_params(arg0: Any) -> pointer:
    return _wasm_functype_params(arg0)  # type: ignore

_wasm_functype_results = dll.wasm_functype_results
_wasm_functype_results.restype = POINTER(wasm_valtype_vec_t)
_wasm_functype_results.argtypes = [POINTER(wasm_functype_t)]
def wasm_functype_results(arg0: Any) -> pointer:
    return _wasm_functype_results(arg0)  # type: ignore

class wasm_globaltype_t(Structure):
    pass

_wasm_globaltype_delete = dll.wasm_globaltype_delete
_wasm_globaltype_delete.restype = None
_wasm_globaltype_delete.argtypes = [POINTER(wasm_globaltype_t)]
def wasm_globaltype_delete(arg0: Any) -> None:
    return _wasm_globaltype_delete(arg0)  # type: ignore

class wasm_globaltype_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_globaltype_t))),
    ]

_wasm_globaltype_vec_new_empty = dll.wasm_globaltype_vec_new_empty
_wasm_globaltype_vec_new_empty.restype = None
_wasm_globaltype_vec_new_empty.argtypes = [POINTER(wasm_globaltype_vec_t)]
def wasm_globaltype_vec_new_empty(out: Any) -> None:
    return _wasm_globaltype_vec_new_empty(out)  # type: ignore

_wasm_globaltype_vec_new_uninitialized = dll.wasm_globaltype_vec_new_uninitialized
_wasm_globaltype_vec_new_uninitialized.restype = None
_wasm_globaltype_vec_new_uninitialized.argtypes = [POINTER(wasm_globaltype_vec_t), c_size_t]
def wasm_globaltype_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_globaltype_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_globaltype_vec_new = dll.wasm_globaltype_vec_new
_wasm_globaltype_vec_new.restype = None
_wasm_globaltype_vec_new.argtypes = [POINTER(wasm_globaltype_vec_t), c_size_t, POINTER(POINTER(wasm_globaltype_t))]
def wasm_globaltype_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_globaltype_vec_new(out, arg1, arg2)  # type: ignore

_wasm_globaltype_vec_copy = dll.wasm_globaltype_vec_copy
_wasm_globaltype_vec_copy.restype = None
_wasm_globaltype_vec_copy.argtypes = [POINTER(wasm_globaltype_vec_t), POINTER(wasm_globaltype_vec_t)]
def wasm_globaltype_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_globaltype_vec_copy(out, arg1)  # type: ignore

_wasm_globaltype_vec_delete = dll.wasm_globaltype_vec_delete
_wasm_globaltype_vec_delete.restype = None
_wasm_globaltype_vec_delete.argtypes = [POINTER(wasm_globaltype_vec_t)]
def wasm_globaltype_vec_delete(arg0: Any) -> None:
    return _wasm_globaltype_vec_delete(arg0)  # type: ignore

_wasm_globaltype_copy = dll.wasm_globaltype_copy
_wasm_globaltype_copy.restype = POINTER(wasm_globaltype_t)
_wasm_globaltype_copy.argtypes = [POINTER(wasm_globaltype_t)]
def wasm_globaltype_copy(arg0: Any) -> pointer:
    return _wasm_globaltype_copy(arg0)  # type: ignore

_wasm_globaltype_new = dll.wasm_globaltype_new
_wasm_globaltype_new.restype = POINTER(wasm_globaltype_t)
_wasm_globaltype_new.argtypes = [POINTER(wasm_valtype_t), wasm_mutability_t]
def wasm_globaltype_new(arg0: Any, arg1: Any) -> pointer:
    return _wasm_globaltype_new(arg0, arg1)  # type: ignore

_wasm_globaltype_content = dll.wasm_globaltype_content
_wasm_globaltype_content.restype = POINTER(wasm_valtype_t)
_wasm_globaltype_content.argtypes = [POINTER(wasm_globaltype_t)]
def wasm_globaltype_content(arg0: Any) -> pointer:
    return _wasm_globaltype_content(arg0)  # type: ignore

_wasm_globaltype_mutability = dll.wasm_globaltype_mutability
_wasm_globaltype_mutability.restype = wasm_mutability_t
_wasm_globaltype_mutability.argtypes = [POINTER(wasm_globaltype_t)]
def wasm_globaltype_mutability(arg0: Any) -> wasm_mutability_t:
    return _wasm_globaltype_mutability(arg0)  # type: ignore

class wasm_tabletype_t(Structure):
    pass

_wasm_tabletype_delete = dll.wasm_tabletype_delete
_wasm_tabletype_delete.restype = None
_wasm_tabletype_delete.argtypes = [POINTER(wasm_tabletype_t)]
def wasm_tabletype_delete(arg0: Any) -> None:
    return _wasm_tabletype_delete(arg0)  # type: ignore

class wasm_tabletype_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_tabletype_t))),
    ]

_wasm_tabletype_vec_new_empty = dll.wasm_tabletype_vec_new_empty
_wasm_tabletype_vec_new_empty.restype = None
_wasm_tabletype_vec_new_empty.argtypes = [POINTER(wasm_tabletype_vec_t)]
def wasm_tabletype_vec_new_empty(out: Any) -> None:
    return _wasm_tabletype_vec_new_empty(out)  # type: ignore

_wasm_tabletype_vec_new_uninitialized = dll.wasm_tabletype_vec_new_uninitialized
_wasm_tabletype_vec_new_uninitialized.restype = None
_wasm_tabletype_vec_new_uninitialized.argtypes = [POINTER(wasm_tabletype_vec_t), c_size_t]
def wasm_tabletype_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_tabletype_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_tabletype_vec_new = dll.wasm_tabletype_vec_new
_wasm_tabletype_vec_new.restype = None
_wasm_tabletype_vec_new.argtypes = [POINTER(wasm_tabletype_vec_t), c_size_t, POINTER(POINTER(wasm_tabletype_t))]
def wasm_tabletype_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_tabletype_vec_new(out, arg1, arg2)  # type: ignore

_wasm_tabletype_vec_copy = dll.wasm_tabletype_vec_copy
_wasm_tabletype_vec_copy.restype = None
_wasm_tabletype_vec_copy.argtypes = [POINTER(wasm_tabletype_vec_t), POINTER(wasm_tabletype_vec_t)]
def wasm_tabletype_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_tabletype_vec_copy(out, arg1)  # type: ignore

_wasm_tabletype_vec_delete = dll.wasm_tabletype_vec_delete
_wasm_tabletype_vec_delete.restype = None
_wasm_tabletype_vec_delete.argtypes = [POINTER(wasm_tabletype_vec_t)]
def wasm_tabletype_vec_delete(arg0: Any) -> None:
    return _wasm_tabletype_vec_delete(arg0)  # type: ignore

_wasm_tabletype_copy = dll.wasm_tabletype_copy
_wasm_tabletype_copy.restype = POINTER(wasm_tabletype_t)
_wasm_tabletype_copy.argtypes = [POINTER(wasm_tabletype_t)]
def wasm_tabletype_copy(arg0: Any) -> pointer:
    return _wasm_tabletype_copy(arg0)  # type: ignore

_wasm_tabletype_new = dll.wasm_tabletype_new
_wasm_tabletype_new.restype = POINTER(wasm_tabletype_t)
_wasm_tabletype_new.argtypes = [POINTER(wasm_valtype_t), POINTER(wasm_limits_t)]
def wasm_tabletype_new(arg0: Any, arg1: Any) -> pointer:
    return _wasm_tabletype_new(arg0, arg1)  # type: ignore

_wasm_tabletype_element = dll.wasm_tabletype_element
_wasm_tabletype_element.restype = POINTER(wasm_valtype_t)
_wasm_tabletype_element.argtypes = [POINTER(wasm_tabletype_t)]
def wasm_tabletype_element(arg0: Any) -> pointer:
    return _wasm_tabletype_element(arg0)  # type: ignore

_wasm_tabletype_limits = dll.wasm_tabletype_limits
_wasm_tabletype_limits.restype = POINTER(wasm_limits_t)
_wasm_tabletype_limits.argtypes = [POINTER(wasm_tabletype_t)]
def wasm_tabletype_limits(arg0: Any) -> pointer:
    return _wasm_tabletype_limits(arg0)  # type: ignore

class wasm_memorytype_t(Structure):
    pass

_wasm_memorytype_delete = dll.wasm_memorytype_delete
_wasm_memorytype_delete.restype = None
_wasm_memorytype_delete.argtypes = [POINTER(wasm_memorytype_t)]
def wasm_memorytype_delete(arg0: Any) -> None:
    return _wasm_memorytype_delete(arg0)  # type: ignore

class wasm_memorytype_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_memorytype_t))),
    ]

_wasm_memorytype_vec_new_empty = dll.wasm_memorytype_vec_new_empty
_wasm_memorytype_vec_new_empty.restype = None
_wasm_memorytype_vec_new_empty.argtypes = [POINTER(wasm_memorytype_vec_t)]
def wasm_memorytype_vec_new_empty(out: Any) -> None:
    return _wasm_memorytype_vec_new_empty(out)  # type: ignore

_wasm_memorytype_vec_new_uninitialized = dll.wasm_memorytype_vec_new_uninitialized
_wasm_memorytype_vec_new_uninitialized.restype = None
_wasm_memorytype_vec_new_uninitialized.argtypes = [POINTER(wasm_memorytype_vec_t), c_size_t]
def wasm_memorytype_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_memorytype_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_memorytype_vec_new = dll.wasm_memorytype_vec_new
_wasm_memorytype_vec_new.restype = None
_wasm_memorytype_vec_new.argtypes = [POINTER(wasm_memorytype_vec_t), c_size_t, POINTER(POINTER(wasm_memorytype_t))]
def wasm_memorytype_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_memorytype_vec_new(out, arg1, arg2)  # type: ignore

_wasm_memorytype_vec_copy = dll.wasm_memorytype_vec_copy
_wasm_memorytype_vec_copy.restype = None
_wasm_memorytype_vec_copy.argtypes = [POINTER(wasm_memorytype_vec_t), POINTER(wasm_memorytype_vec_t)]
def wasm_memorytype_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_memorytype_vec_copy(out, arg1)  # type: ignore

_wasm_memorytype_vec_delete = dll.wasm_memorytype_vec_delete
_wasm_memorytype_vec_delete.restype = None
_wasm_memorytype_vec_delete.argtypes = [POINTER(wasm_memorytype_vec_t)]
def wasm_memorytype_vec_delete(arg0: Any) -> None:
    return _wasm_memorytype_vec_delete(arg0)  # type: ignore

_wasm_memorytype_copy = dll.wasm_memorytype_copy
_wasm_memorytype_copy.restype = POINTER(wasm_memorytype_t)
_wasm_memorytype_copy.argtypes = [POINTER(wasm_memorytype_t)]
def wasm_memorytype_copy(arg0: Any) -> pointer:
    return _wasm_memorytype_copy(arg0)  # type: ignore

_wasm_memorytype_new = dll.wasm_memorytype_new
_wasm_memorytype_new.restype = POINTER(wasm_memorytype_t)
_wasm_memorytype_new.argtypes = [POINTER(wasm_limits_t)]
def wasm_memorytype_new(arg0: Any) -> pointer:
    return _wasm_memorytype_new(arg0)  # type: ignore

_wasm_memorytype_limits = dll.wasm_memorytype_limits
_wasm_memorytype_limits.restype = POINTER(wasm_limits_t)
_wasm_memorytype_limits.argtypes = [POINTER(wasm_memorytype_t)]
def wasm_memorytype_limits(arg0: Any) -> pointer:
    return _wasm_memorytype_limits(arg0)  # type: ignore

class wasm_externtype_t(Structure):
    pass

_wasm_externtype_delete = dll.wasm_externtype_delete
_wasm_externtype_delete.restype = None
_wasm_externtype_delete.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_delete(arg0: Any) -> None:
    return _wasm_externtype_delete(arg0)  # type: ignore

class wasm_externtype_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_externtype_t))),
    ]

_wasm_externtype_vec_new_empty = dll.wasm_externtype_vec_new_empty
_wasm_externtype_vec_new_empty.restype = None
_wasm_externtype_vec_new_empty.argtypes = [POINTER(wasm_externtype_vec_t)]
def wasm_externtype_vec_new_empty(out: Any) -> None:
    return _wasm_externtype_vec_new_empty(out)  # type: ignore

_wasm_externtype_vec_new_uninitialized = dll.wasm_externtype_vec_new_uninitialized
_wasm_externtype_vec_new_uninitialized.restype = None
_wasm_externtype_vec_new_uninitialized.argtypes = [POINTER(wasm_externtype_vec_t), c_size_t]
def wasm_externtype_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_externtype_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_externtype_vec_new = dll.wasm_externtype_vec_new
_wasm_externtype_vec_new.restype = None
_wasm_externtype_vec_new.argtypes = [POINTER(wasm_externtype_vec_t), c_size_t, POINTER(POINTER(wasm_externtype_t))]
def wasm_externtype_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_externtype_vec_new(out, arg1, arg2)  # type: ignore

_wasm_externtype_vec_copy = dll.wasm_externtype_vec_copy
_wasm_externtype_vec_copy.restype = None
_wasm_externtype_vec_copy.argtypes = [POINTER(wasm_externtype_vec_t), POINTER(wasm_externtype_vec_t)]
def wasm_externtype_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_externtype_vec_copy(out, arg1)  # type: ignore

_wasm_externtype_vec_delete = dll.wasm_externtype_vec_delete
_wasm_externtype_vec_delete.restype = None
_wasm_externtype_vec_delete.argtypes = [POINTER(wasm_externtype_vec_t)]
def wasm_externtype_vec_delete(arg0: Any) -> None:
    return _wasm_externtype_vec_delete(arg0)  # type: ignore

_wasm_externtype_copy = dll.wasm_externtype_copy
_wasm_externtype_copy.restype = POINTER(wasm_externtype_t)
_wasm_externtype_copy.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_copy(arg0: Any) -> pointer:
    return _wasm_externtype_copy(arg0)  # type: ignore

wasm_externkind_t = c_uint8

_wasm_externtype_kind = dll.wasm_externtype_kind
_wasm_externtype_kind.restype = wasm_externkind_t
_wasm_externtype_kind.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_kind(arg0: Any) -> wasm_externkind_t:
    return _wasm_externtype_kind(arg0)  # type: ignore

_wasm_functype_as_externtype = dll.wasm_functype_as_externtype
_wasm_functype_as_externtype.restype = POINTER(wasm_externtype_t)
_wasm_functype_as_externtype.argtypes = [POINTER(wasm_functype_t)]
def wasm_functype_as_externtype(arg0: Any) -> pointer:
    return _wasm_functype_as_externtype(arg0)  # type: ignore

_wasm_globaltype_as_externtype = dll.wasm_globaltype_as_externtype
_wasm_globaltype_as_externtype.restype = POINTER(wasm_externtype_t)
_wasm_globaltype_as_externtype.argtypes = [POINTER(wasm_globaltype_t)]
def wasm_globaltype_as_externtype(arg0: Any) -> pointer:
    return _wasm_globaltype_as_externtype(arg0)  # type: ignore

_wasm_tabletype_as_externtype = dll.wasm_tabletype_as_externtype
_wasm_tabletype_as_externtype.restype = POINTER(wasm_externtype_t)
_wasm_tabletype_as_externtype.argtypes = [POINTER(wasm_tabletype_t)]
def wasm_tabletype_as_externtype(arg0: Any) -> pointer:
    return _wasm_tabletype_as_externtype(arg0)  # type: ignore

_wasm_memorytype_as_externtype = dll.wasm_memorytype_as_externtype
_wasm_memorytype_as_externtype.restype = POINTER(wasm_externtype_t)
_wasm_memorytype_as_externtype.argtypes = [POINTER(wasm_memorytype_t)]
def wasm_memorytype_as_externtype(arg0: Any) -> pointer:
    return _wasm_memorytype_as_externtype(arg0)  # type: ignore

_wasm_externtype_as_functype = dll.wasm_externtype_as_functype
_wasm_externtype_as_functype.restype = POINTER(wasm_functype_t)
_wasm_externtype_as_functype.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_as_functype(arg0: Any) -> pointer:
    return _wasm_externtype_as_functype(arg0)  # type: ignore

_wasm_externtype_as_globaltype = dll.wasm_externtype_as_globaltype
_wasm_externtype_as_globaltype.restype = POINTER(wasm_globaltype_t)
_wasm_externtype_as_globaltype.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_as_globaltype(arg0: Any) -> pointer:
    return _wasm_externtype_as_globaltype(arg0)  # type: ignore

_wasm_externtype_as_tabletype = dll.wasm_externtype_as_tabletype
_wasm_externtype_as_tabletype.restype = POINTER(wasm_tabletype_t)
_wasm_externtype_as_tabletype.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_as_tabletype(arg0: Any) -> pointer:
    return _wasm_externtype_as_tabletype(arg0)  # type: ignore

_wasm_externtype_as_memorytype = dll.wasm_externtype_as_memorytype
_wasm_externtype_as_memorytype.restype = POINTER(wasm_memorytype_t)
_wasm_externtype_as_memorytype.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_as_memorytype(arg0: Any) -> pointer:
    return _wasm_externtype_as_memorytype(arg0)  # type: ignore

_wasm_functype_as_externtype_const = dll.wasm_functype_as_externtype_const
_wasm_functype_as_externtype_const.restype = POINTER(wasm_externtype_t)
_wasm_functype_as_externtype_const.argtypes = [POINTER(wasm_functype_t)]
def wasm_functype_as_externtype_const(arg0: Any) -> pointer:
    return _wasm_functype_as_externtype_const(arg0)  # type: ignore

_wasm_globaltype_as_externtype_const = dll.wasm_globaltype_as_externtype_const
_wasm_globaltype_as_externtype_const.restype = POINTER(wasm_externtype_t)
_wasm_globaltype_as_externtype_const.argtypes = [POINTER(wasm_globaltype_t)]
def wasm_globaltype_as_externtype_const(arg0: Any) -> pointer:
    return _wasm_globaltype_as_externtype_const(arg0)  # type: ignore

_wasm_tabletype_as_externtype_const = dll.wasm_tabletype_as_externtype_const
_wasm_tabletype_as_externtype_const.restype = POINTER(wasm_externtype_t)
_wasm_tabletype_as_externtype_const.argtypes = [POINTER(wasm_tabletype_t)]
def wasm_tabletype_as_externtype_const(arg0: Any) -> pointer:
    return _wasm_tabletype_as_externtype_const(arg0)  # type: ignore

_wasm_memorytype_as_externtype_const = dll.wasm_memorytype_as_externtype_const
_wasm_memorytype_as_externtype_const.restype = POINTER(wasm_externtype_t)
_wasm_memorytype_as_externtype_const.argtypes = [POINTER(wasm_memorytype_t)]
def wasm_memorytype_as_externtype_const(arg0: Any) -> pointer:
    return _wasm_memorytype_as_externtype_const(arg0)  # type: ignore

_wasm_externtype_as_functype_const = dll.wasm_externtype_as_functype_const
_wasm_externtype_as_functype_const.restype = POINTER(wasm_functype_t)
_wasm_externtype_as_functype_const.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_as_functype_const(arg0: Any) -> pointer:
    return _wasm_externtype_as_functype_const(arg0)  # type: ignore

_wasm_externtype_as_globaltype_const = dll.wasm_externtype_as_globaltype_const
_wasm_externtype_as_globaltype_const.restype = POINTER(wasm_globaltype_t)
_wasm_externtype_as_globaltype_const.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_as_globaltype_const(arg0: Any) -> pointer:
    return _wasm_externtype_as_globaltype_const(arg0)  # type: ignore

_wasm_externtype_as_tabletype_const = dll.wasm_externtype_as_tabletype_const
_wasm_externtype_as_tabletype_const.restype = POINTER(wasm_tabletype_t)
_wasm_externtype_as_tabletype_const.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_as_tabletype_const(arg0: Any) -> pointer:
    return _wasm_externtype_as_tabletype_const(arg0)  # type: ignore

_wasm_externtype_as_memorytype_const = dll.wasm_externtype_as_memorytype_const
_wasm_externtype_as_memorytype_const.restype = POINTER(wasm_memorytype_t)
_wasm_externtype_as_memorytype_const.argtypes = [POINTER(wasm_externtype_t)]
def wasm_externtype_as_memorytype_const(arg0: Any) -> pointer:
    return _wasm_externtype_as_memorytype_const(arg0)  # type: ignore

class wasm_importtype_t(Structure):
    pass

_wasm_importtype_delete = dll.wasm_importtype_delete
_wasm_importtype_delete.restype = None
_wasm_importtype_delete.argtypes = [POINTER(wasm_importtype_t)]
def wasm_importtype_delete(arg0: Any) -> None:
    return _wasm_importtype_delete(arg0)  # type: ignore

class wasm_importtype_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_importtype_t))),
    ]

_wasm_importtype_vec_new_empty = dll.wasm_importtype_vec_new_empty
_wasm_importtype_vec_new_empty.restype = None
_wasm_importtype_vec_new_empty.argtypes = [POINTER(wasm_importtype_vec_t)]
def wasm_importtype_vec_new_empty(out: Any) -> None:
    return _wasm_importtype_vec_new_empty(out)  # type: ignore

_wasm_importtype_vec_new_uninitialized = dll.wasm_importtype_vec_new_uninitialized
_wasm_importtype_vec_new_uninitialized.restype = None
_wasm_importtype_vec_new_uninitialized.argtypes = [POINTER(wasm_importtype_vec_t), c_size_t]
def wasm_importtype_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_importtype_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_importtype_vec_new = dll.wasm_importtype_vec_new
_wasm_importtype_vec_new.restype = None
_wasm_importtype_vec_new.argtypes = [POINTER(wasm_importtype_vec_t), c_size_t, POINTER(POINTER(wasm_importtype_t))]
def wasm_importtype_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_importtype_vec_new(out, arg1, arg2)  # type: ignore

_wasm_importtype_vec_copy = dll.wasm_importtype_vec_copy
_wasm_importtype_vec_copy.restype = None
_wasm_importtype_vec_copy.argtypes = [POINTER(wasm_importtype_vec_t), POINTER(wasm_importtype_vec_t)]
def wasm_importtype_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_importtype_vec_copy(out, arg1)  # type: ignore

_wasm_importtype_vec_delete = dll.wasm_importtype_vec_delete
_wasm_importtype_vec_delete.restype = None
_wasm_importtype_vec_delete.argtypes = [POINTER(wasm_importtype_vec_t)]
def wasm_importtype_vec_delete(arg0: Any) -> None:
    return _wasm_importtype_vec_delete(arg0)  # type: ignore

_wasm_importtype_copy = dll.wasm_importtype_copy
_wasm_importtype_copy.restype = POINTER(wasm_importtype_t)
_wasm_importtype_copy.argtypes = [POINTER(wasm_importtype_t)]
def wasm_importtype_copy(arg0: Any) -> pointer:
    return _wasm_importtype_copy(arg0)  # type: ignore

_wasm_importtype_new = dll.wasm_importtype_new
_wasm_importtype_new.restype = POINTER(wasm_importtype_t)
_wasm_importtype_new.argtypes = [POINTER(wasm_name_t), POINTER(wasm_name_t), POINTER(wasm_externtype_t)]
def wasm_importtype_new(module: Any, name: Any, arg2: Any) -> pointer:
    return _wasm_importtype_new(module, name, arg2)  # type: ignore

_wasm_importtype_module = dll.wasm_importtype_module
_wasm_importtype_module.restype = POINTER(wasm_name_t)
_wasm_importtype_module.argtypes = [POINTER(wasm_importtype_t)]
def wasm_importtype_module(arg0: Any) -> pointer:
    return _wasm_importtype_module(arg0)  # type: ignore

_wasm_importtype_name = dll.wasm_importtype_name
_wasm_importtype_name.restype = POINTER(wasm_name_t)
_wasm_importtype_name.argtypes = [POINTER(wasm_importtype_t)]
def wasm_importtype_name(arg0: Any) -> pointer:
    return _wasm_importtype_name(arg0)  # type: ignore

_wasm_importtype_type = dll.wasm_importtype_type
_wasm_importtype_type.restype = POINTER(wasm_externtype_t)
_wasm_importtype_type.argtypes = [POINTER(wasm_importtype_t)]
def wasm_importtype_type(arg0: Any) -> pointer:
    return _wasm_importtype_type(arg0)  # type: ignore

class wasm_exporttype_t(Structure):
    pass

_wasm_exporttype_delete = dll.wasm_exporttype_delete
_wasm_exporttype_delete.restype = None
_wasm_exporttype_delete.argtypes = [POINTER(wasm_exporttype_t)]
def wasm_exporttype_delete(arg0: Any) -> None:
    return _wasm_exporttype_delete(arg0)  # type: ignore

class wasm_exporttype_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_exporttype_t))),
    ]

_wasm_exporttype_vec_new_empty = dll.wasm_exporttype_vec_new_empty
_wasm_exporttype_vec_new_empty.restype = None
_wasm_exporttype_vec_new_empty.argtypes = [POINTER(wasm_exporttype_vec_t)]
def wasm_exporttype_vec_new_empty(out: Any) -> None:
    return _wasm_exporttype_vec_new_empty(out)  # type: ignore

_wasm_exporttype_vec_new_uninitialized = dll.wasm_exporttype_vec_new_uninitialized
_wasm_exporttype_vec_new_uninitialized.restype = None
_wasm_exporttype_vec_new_uninitialized.argtypes = [POINTER(wasm_exporttype_vec_t), c_size_t]
def wasm_exporttype_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_exporttype_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_exporttype_vec_new = dll.wasm_exporttype_vec_new
_wasm_exporttype_vec_new.restype = None
_wasm_exporttype_vec_new.argtypes = [POINTER(wasm_exporttype_vec_t), c_size_t, POINTER(POINTER(wasm_exporttype_t))]
def wasm_exporttype_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_exporttype_vec_new(out, arg1, arg2)  # type: ignore

_wasm_exporttype_vec_copy = dll.wasm_exporttype_vec_copy
_wasm_exporttype_vec_copy.restype = None
_wasm_exporttype_vec_copy.argtypes = [POINTER(wasm_exporttype_vec_t), POINTER(wasm_exporttype_vec_t)]
def wasm_exporttype_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_exporttype_vec_copy(out, arg1)  # type: ignore

_wasm_exporttype_vec_delete = dll.wasm_exporttype_vec_delete
_wasm_exporttype_vec_delete.restype = None
_wasm_exporttype_vec_delete.argtypes = [POINTER(wasm_exporttype_vec_t)]
def wasm_exporttype_vec_delete(arg0: Any) -> None:
    return _wasm_exporttype_vec_delete(arg0)  # type: ignore

_wasm_exporttype_copy = dll.wasm_exporttype_copy
_wasm_exporttype_copy.restype = POINTER(wasm_exporttype_t)
_wasm_exporttype_copy.argtypes = [POINTER(wasm_exporttype_t)]
def wasm_exporttype_copy(arg0: Any) -> pointer:
    return _wasm_exporttype_copy(arg0)  # type: ignore

_wasm_exporttype_new = dll.wasm_exporttype_new
_wasm_exporttype_new.restype = POINTER(wasm_exporttype_t)
_wasm_exporttype_new.argtypes = [POINTER(wasm_name_t), POINTER(wasm_externtype_t)]
def wasm_exporttype_new(arg0: Any, arg1: Any) -> pointer:
    return _wasm_exporttype_new(arg0, arg1)  # type: ignore

_wasm_exporttype_name = dll.wasm_exporttype_name
_wasm_exporttype_name.restype = POINTER(wasm_name_t)
_wasm_exporttype_name.argtypes = [POINTER(wasm_exporttype_t)]
def wasm_exporttype_name(arg0: Any) -> pointer:
    return _wasm_exporttype_name(arg0)  # type: ignore

_wasm_exporttype_type = dll.wasm_exporttype_type
_wasm_exporttype_type.restype = POINTER(wasm_externtype_t)
_wasm_exporttype_type.argtypes = [POINTER(wasm_exporttype_t)]
def wasm_exporttype_type(arg0: Any) -> pointer:
    return _wasm_exporttype_type(arg0)  # type: ignore

_wasm_val_delete = dll.wasm_val_delete
_wasm_val_delete.restype = None
_wasm_val_delete.argtypes = [POINTER(wasm_val_t)]
def wasm_val_delete(v: Any) -> None:
    return _wasm_val_delete(v)  # type: ignore

_wasm_val_copy = dll.wasm_val_copy
_wasm_val_copy.restype = None
_wasm_val_copy.argtypes = [POINTER(wasm_val_t), POINTER(wasm_val_t)]
def wasm_val_copy(out: Any, arg1: Any) -> None:
    return _wasm_val_copy(out, arg1)  # type: ignore

class wasm_val_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(wasm_val_t)),
    ]

_wasm_val_vec_new_empty = dll.wasm_val_vec_new_empty
_wasm_val_vec_new_empty.restype = None
_wasm_val_vec_new_empty.argtypes = [POINTER(wasm_val_vec_t)]
def wasm_val_vec_new_empty(out: Any) -> None:
    return _wasm_val_vec_new_empty(out)  # type: ignore

_wasm_val_vec_new_uninitialized = dll.wasm_val_vec_new_uninitialized
_wasm_val_vec_new_uninitialized.restype = None
_wasm_val_vec_new_uninitialized.argtypes = [POINTER(wasm_val_vec_t), c_size_t]
def wasm_val_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_val_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_val_vec_new = dll.wasm_val_vec_new
_wasm_val_vec_new.restype = None
_wasm_val_vec_new.argtypes = [POINTER(wasm_val_vec_t), c_size_t, POINTER(wasm_val_t)]
def wasm_val_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_val_vec_new(out, arg1, arg2)  # type: ignore

_wasm_val_vec_copy = dll.wasm_val_vec_copy
_wasm_val_vec_copy.restype = None
_wasm_val_vec_copy.argtypes = [POINTER(wasm_val_vec_t), POINTER(wasm_val_vec_t)]
def wasm_val_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_val_vec_copy(out, arg1)  # type: ignore

_wasm_val_vec_delete = dll.wasm_val_vec_delete
_wasm_val_vec_delete.restype = None
_wasm_val_vec_delete.argtypes = [POINTER(wasm_val_vec_t)]
def wasm_val_vec_delete(arg0: Any) -> None:
    return _wasm_val_vec_delete(arg0)  # type: ignore

_wasm_ref_delete = dll.wasm_ref_delete
_wasm_ref_delete.restype = None
_wasm_ref_delete.argtypes = [POINTER(wasm_ref_t)]
def wasm_ref_delete(arg0: Any) -> None:
    return _wasm_ref_delete(arg0)  # type: ignore

_wasm_ref_copy = dll.wasm_ref_copy
_wasm_ref_copy.restype = POINTER(wasm_ref_t)
_wasm_ref_copy.argtypes = [POINTER(wasm_ref_t)]
def wasm_ref_copy(arg0: Any) -> pointer:
    return _wasm_ref_copy(arg0)  # type: ignore

_wasm_ref_same = dll.wasm_ref_same
_wasm_ref_same.restype = c_bool
_wasm_ref_same.argtypes = [POINTER(wasm_ref_t), POINTER(wasm_ref_t)]
def wasm_ref_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_ref_same(arg0, arg1)  # type: ignore

_wasm_ref_get_host_info = dll.wasm_ref_get_host_info
_wasm_ref_get_host_info.restype = c_void_p
_wasm_ref_get_host_info.argtypes = [POINTER(wasm_ref_t)]
def wasm_ref_get_host_info(arg0: Any) -> pointer:
    return _wasm_ref_get_host_info(arg0)  # type: ignore

_wasm_ref_set_host_info = dll.wasm_ref_set_host_info
_wasm_ref_set_host_info.restype = None
_wasm_ref_set_host_info.argtypes = [POINTER(wasm_ref_t), c_void_p]
def wasm_ref_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_ref_set_host_info(arg0, arg1)  # type: ignore

_wasm_ref_set_host_info_with_finalizer = dll.wasm_ref_set_host_info_with_finalizer
_wasm_ref_set_host_info_with_finalizer.restype = None
_wasm_ref_set_host_info_with_finalizer.argtypes = [POINTER(wasm_ref_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_ref_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_ref_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

class wasm_frame_t(Structure):
    pass

_wasm_frame_delete = dll.wasm_frame_delete
_wasm_frame_delete.restype = None
_wasm_frame_delete.argtypes = [POINTER(wasm_frame_t)]
def wasm_frame_delete(arg0: Any) -> None:
    return _wasm_frame_delete(arg0)  # type: ignore

class wasm_frame_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_frame_t))),
    ]

_wasm_frame_vec_new_empty = dll.wasm_frame_vec_new_empty
_wasm_frame_vec_new_empty.restype = None
_wasm_frame_vec_new_empty.argtypes = [POINTER(wasm_frame_vec_t)]
def wasm_frame_vec_new_empty(out: Any) -> None:
    return _wasm_frame_vec_new_empty(out)  # type: ignore

_wasm_frame_vec_new_uninitialized = dll.wasm_frame_vec_new_uninitialized
_wasm_frame_vec_new_uninitialized.restype = None
_wasm_frame_vec_new_uninitialized.argtypes = [POINTER(wasm_frame_vec_t), c_size_t]
def wasm_frame_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_frame_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_frame_vec_new = dll.wasm_frame_vec_new
_wasm_frame_vec_new.restype = None
_wasm_frame_vec_new.argtypes = [POINTER(wasm_frame_vec_t), c_size_t, POINTER(POINTER(wasm_frame_t))]
def wasm_frame_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_frame_vec_new(out, arg1, arg2)  # type: ignore

_wasm_frame_vec_copy = dll.wasm_frame_vec_copy
_wasm_frame_vec_copy.restype = None
_wasm_frame_vec_copy.argtypes = [POINTER(wasm_frame_vec_t), POINTER(wasm_frame_vec_t)]
def wasm_frame_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_frame_vec_copy(out, arg1)  # type: ignore

_wasm_frame_vec_delete = dll.wasm_frame_vec_delete
_wasm_frame_vec_delete.restype = None
_wasm_frame_vec_delete.argtypes = [POINTER(wasm_frame_vec_t)]
def wasm_frame_vec_delete(arg0: Any) -> None:
    return _wasm_frame_vec_delete(arg0)  # type: ignore

_wasm_frame_func_index = dll.wasm_frame_func_index
_wasm_frame_func_index.restype = c_uint32
_wasm_frame_func_index.argtypes = [POINTER(wasm_frame_t)]
def wasm_frame_func_index(arg0: Any) -> int:
    return _wasm_frame_func_index(arg0)  # type: ignore

_wasm_frame_func_offset = dll.wasm_frame_func_offset
_wasm_frame_func_offset.restype = c_size_t
_wasm_frame_func_offset.argtypes = [POINTER(wasm_frame_t)]
def wasm_frame_func_offset(arg0: Any) -> int:
    return _wasm_frame_func_offset(arg0)  # type: ignore

_wasm_frame_module_offset = dll.wasm_frame_module_offset
_wasm_frame_module_offset.restype = c_size_t
_wasm_frame_module_offset.argtypes = [POINTER(wasm_frame_t)]
def wasm_frame_module_offset(arg0: Any) -> int:
    return _wasm_frame_module_offset(arg0)  # type: ignore

wasm_message_t = wasm_name_t

class wasm_trap_t(Structure):
    pass

_wasm_trap_delete = dll.wasm_trap_delete
_wasm_trap_delete.restype = None
_wasm_trap_delete.argtypes = [POINTER(wasm_trap_t)]
def wasm_trap_delete(arg0: Any) -> None:
    return _wasm_trap_delete(arg0)  # type: ignore

_wasm_trap_copy = dll.wasm_trap_copy
_wasm_trap_copy.restype = POINTER(wasm_trap_t)
_wasm_trap_copy.argtypes = [POINTER(wasm_trap_t)]
def wasm_trap_copy(arg0: Any) -> pointer:
    return _wasm_trap_copy(arg0)  # type: ignore

_wasm_trap_same = dll.wasm_trap_same
_wasm_trap_same.restype = c_bool
_wasm_trap_same.argtypes = [POINTER(wasm_trap_t), POINTER(wasm_trap_t)]
def wasm_trap_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_trap_same(arg0, arg1)  # type: ignore

_wasm_trap_get_host_info = dll.wasm_trap_get_host_info
_wasm_trap_get_host_info.restype = c_void_p
_wasm_trap_get_host_info.argtypes = [POINTER(wasm_trap_t)]
def wasm_trap_get_host_info(arg0: Any) -> pointer:
    return _wasm_trap_get_host_info(arg0)  # type: ignore

_wasm_trap_set_host_info = dll.wasm_trap_set_host_info
_wasm_trap_set_host_info.restype = None
_wasm_trap_set_host_info.argtypes = [POINTER(wasm_trap_t), c_void_p]
def wasm_trap_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_trap_set_host_info(arg0, arg1)  # type: ignore

_wasm_trap_set_host_info_with_finalizer = dll.wasm_trap_set_host_info_with_finalizer
_wasm_trap_set_host_info_with_finalizer.restype = None
_wasm_trap_set_host_info_with_finalizer.argtypes = [POINTER(wasm_trap_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_trap_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_trap_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

_wasm_trap_as_ref = dll.wasm_trap_as_ref
_wasm_trap_as_ref.restype = POINTER(wasm_ref_t)
_wasm_trap_as_ref.argtypes = [POINTER(wasm_trap_t)]
def wasm_trap_as_ref(arg0: Any) -> pointer:
    return _wasm_trap_as_ref(arg0)  # type: ignore

_wasm_trap_as_ref_const = dll.wasm_trap_as_ref_const
_wasm_trap_as_ref_const.restype = POINTER(wasm_ref_t)
_wasm_trap_as_ref_const.argtypes = [POINTER(wasm_trap_t)]
def wasm_trap_as_ref_const(arg0: Any) -> pointer:
    return _wasm_trap_as_ref_const(arg0)  # type: ignore

_wasm_trap_new = dll.wasm_trap_new
_wasm_trap_new.restype = POINTER(wasm_trap_t)
_wasm_trap_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_message_t)]
def wasm_trap_new(store: Any, arg1: Any) -> pointer:
    return _wasm_trap_new(store, arg1)  # type: ignore

_wasm_trap_message = dll.wasm_trap_message
_wasm_trap_message.restype = None
_wasm_trap_message.argtypes = [POINTER(wasm_trap_t), POINTER(wasm_message_t)]
def wasm_trap_message(arg0: Any, out: Any) -> None:
    return _wasm_trap_message(arg0, out)  # type: ignore

_wasm_trap_origin = dll.wasm_trap_origin
_wasm_trap_origin.restype = POINTER(wasm_frame_t)
_wasm_trap_origin.argtypes = [POINTER(wasm_trap_t)]
def wasm_trap_origin(arg0: Any) -> pointer:
    return _wasm_trap_origin(arg0)  # type: ignore

_wasm_trap_trace = dll.wasm_trap_trace
_wasm_trap_trace.restype = None
_wasm_trap_trace.argtypes = [POINTER(wasm_trap_t), POINTER(wasm_frame_vec_t)]
def wasm_trap_trace(arg0: Any, out: Any) -> None:
    return _wasm_trap_trace(arg0, out)  # type: ignore

class wasm_foreign_t(Structure):
    pass

class wasm_module_t(Structure):
    pass

_wasm_module_delete = dll.wasm_module_delete
_wasm_module_delete.restype = None
_wasm_module_delete.argtypes = [POINTER(wasm_module_t)]
def wasm_module_delete(arg0: Any) -> None:
    return _wasm_module_delete(arg0)  # type: ignore

_wasm_module_copy = dll.wasm_module_copy
_wasm_module_copy.restype = POINTER(wasm_module_t)
_wasm_module_copy.argtypes = [POINTER(wasm_module_t)]
def wasm_module_copy(arg0: Any) -> pointer:
    return _wasm_module_copy(arg0)  # type: ignore

_wasm_module_same = dll.wasm_module_same
_wasm_module_same.restype = c_bool
_wasm_module_same.argtypes = [POINTER(wasm_module_t), POINTER(wasm_module_t)]
def wasm_module_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_module_same(arg0, arg1)  # type: ignore

_wasm_module_get_host_info = dll.wasm_module_get_host_info
_wasm_module_get_host_info.restype = c_void_p
_wasm_module_get_host_info.argtypes = [POINTER(wasm_module_t)]
def wasm_module_get_host_info(arg0: Any) -> pointer:
    return _wasm_module_get_host_info(arg0)  # type: ignore

_wasm_module_set_host_info = dll.wasm_module_set_host_info
_wasm_module_set_host_info.restype = None
_wasm_module_set_host_info.argtypes = [POINTER(wasm_module_t), c_void_p]
def wasm_module_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_module_set_host_info(arg0, arg1)  # type: ignore

_wasm_module_set_host_info_with_finalizer = dll.wasm_module_set_host_info_with_finalizer
_wasm_module_set_host_info_with_finalizer.restype = None
_wasm_module_set_host_info_with_finalizer.argtypes = [POINTER(wasm_module_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_module_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_module_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

_wasm_module_as_ref = dll.wasm_module_as_ref
_wasm_module_as_ref.restype = POINTER(wasm_ref_t)
_wasm_module_as_ref.argtypes = [POINTER(wasm_module_t)]
def wasm_module_as_ref(arg0: Any) -> pointer:
    return _wasm_module_as_ref(arg0)  # type: ignore

_wasm_module_as_ref_const = dll.wasm_module_as_ref_const
_wasm_module_as_ref_const.restype = POINTER(wasm_ref_t)
_wasm_module_as_ref_const.argtypes = [POINTER(wasm_module_t)]
def wasm_module_as_ref_const(arg0: Any) -> pointer:
    return _wasm_module_as_ref_const(arg0)  # type: ignore

class wasm_shared_module_t(Structure):
    pass

_wasm_shared_module_delete = dll.wasm_shared_module_delete
_wasm_shared_module_delete.restype = None
_wasm_shared_module_delete.argtypes = [POINTER(wasm_shared_module_t)]
def wasm_shared_module_delete(arg0: Any) -> None:
    return _wasm_shared_module_delete(arg0)  # type: ignore

_wasm_module_share = dll.wasm_module_share
_wasm_module_share.restype = POINTER(wasm_shared_module_t)
_wasm_module_share.argtypes = [POINTER(wasm_module_t)]
def wasm_module_share(arg0: Any) -> pointer:
    return _wasm_module_share(arg0)  # type: ignore

_wasm_module_obtain = dll.wasm_module_obtain
_wasm_module_obtain.restype = POINTER(wasm_module_t)
_wasm_module_obtain.argtypes = [POINTER(wasm_store_t), POINTER(wasm_shared_module_t)]
def wasm_module_obtain(arg0: Any, arg1: Any) -> pointer:
    return _wasm_module_obtain(arg0, arg1)  # type: ignore

_wasm_module_new = dll.wasm_module_new
_wasm_module_new.restype = POINTER(wasm_module_t)
_wasm_module_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_byte_vec_t)]
def wasm_module_new(arg0: Any, binary: Any) -> pointer:
    return _wasm_module_new(arg0, binary)  # type: ignore

_wasm_module_validate = dll.wasm_module_validate
_wasm_module_validate.restype = c_bool
_wasm_module_validate.argtypes = [POINTER(wasm_store_t), POINTER(wasm_byte_vec_t)]
def wasm_module_validate(arg0: Any, binary: Any) -> c_bool:
    return _wasm_module_validate(arg0, binary)  # type: ignore

_wasm_module_imports = dll.wasm_module_imports
_wasm_module_imports.restype = None
_wasm_module_imports.argtypes = [POINTER(wasm_module_t), POINTER(wasm_importtype_vec_t)]
def wasm_module_imports(arg0: Any, out: Any) -> None:
    return _wasm_module_imports(arg0, out)  # type: ignore

_wasm_module_exports = dll.wasm_module_exports
_wasm_module_exports.restype = None
_wasm_module_exports.argtypes = [POINTER(wasm_module_t), POINTER(wasm_exporttype_vec_t)]
def wasm_module_exports(arg0: Any, out: Any) -> None:
    return _wasm_module_exports(arg0, out)  # type: ignore

class wasm_func_t(Structure):
    pass

_wasm_func_delete = dll.wasm_func_delete
_wasm_func_delete.restype = None
_wasm_func_delete.argtypes = [POINTER(wasm_func_t)]
def wasm_func_delete(arg0: Any) -> None:
    return _wasm_func_delete(arg0)  # type: ignore

_wasm_func_copy = dll.wasm_func_copy
_wasm_func_copy.restype = POINTER(wasm_func_t)
_wasm_func_copy.argtypes = [POINTER(wasm_func_t)]
def wasm_func_copy(arg0: Any) -> pointer:
    return _wasm_func_copy(arg0)  # type: ignore

_wasm_func_same = dll.wasm_func_same
_wasm_func_same.restype = c_bool
_wasm_func_same.argtypes = [POINTER(wasm_func_t), POINTER(wasm_func_t)]
def wasm_func_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_func_same(arg0, arg1)  # type: ignore

_wasm_func_get_host_info = dll.wasm_func_get_host_info
_wasm_func_get_host_info.restype = c_void_p
_wasm_func_get_host_info.argtypes = [POINTER(wasm_func_t)]
def wasm_func_get_host_info(arg0: Any) -> pointer:
    return _wasm_func_get_host_info(arg0)  # type: ignore

_wasm_func_set_host_info = dll.wasm_func_set_host_info
_wasm_func_set_host_info.restype = None
_wasm_func_set_host_info.argtypes = [POINTER(wasm_func_t), c_void_p]
def wasm_func_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_func_set_host_info(arg0, arg1)  # type: ignore

_wasm_func_set_host_info_with_finalizer = dll.wasm_func_set_host_info_with_finalizer
_wasm_func_set_host_info_with_finalizer.restype = None
_wasm_func_set_host_info_with_finalizer.argtypes = [POINTER(wasm_func_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_func_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_func_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

_wasm_func_as_ref = dll.wasm_func_as_ref
_wasm_func_as_ref.restype = POINTER(wasm_ref_t)
_wasm_func_as_ref.argtypes = [POINTER(wasm_func_t)]
def wasm_func_as_ref(arg0: Any) -> pointer:
    return _wasm_func_as_ref(arg0)  # type: ignore

_wasm_func_as_ref_const = dll.wasm_func_as_ref_const
_wasm_func_as_ref_const.restype = POINTER(wasm_ref_t)
_wasm_func_as_ref_const.argtypes = [POINTER(wasm_func_t)]
def wasm_func_as_ref_const(arg0: Any) -> pointer:
    return _wasm_func_as_ref_const(arg0)  # type: ignore

wasm_func_callback_t = CFUNCTYPE(c_size_t, POINTER(wasm_val_t), POINTER(wasm_val_t))

wasm_func_callback_with_env_t = CFUNCTYPE(c_size_t, c_void_p, POINTER(wasm_val_t), POINTER(wasm_val_t))

_wasm_func_new = dll.wasm_func_new
_wasm_func_new.restype = POINTER(wasm_func_t)
_wasm_func_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_functype_t), wasm_func_callback_t]
def wasm_func_new(arg0: Any, arg1: Any, arg2: Any) -> pointer:
    return _wasm_func_new(arg0, arg1, arg2)  # type: ignore

_wasm_func_new_with_env = dll.wasm_func_new_with_env
_wasm_func_new_with_env.restype = POINTER(wasm_func_t)
_wasm_func_new_with_env.argtypes = [POINTER(wasm_store_t), POINTER(wasm_functype_t), wasm_func_callback_with_env_t, c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_func_new_with_env(arg0: Any, type: Any, arg2: Any, env: Any, finalizer: Any) -> pointer:
    return _wasm_func_new_with_env(arg0, type, arg2, env, finalizer)  # type: ignore

_wasm_func_type = dll.wasm_func_type
_wasm_func_type.restype = POINTER(wasm_functype_t)
_wasm_func_type.argtypes = [POINTER(wasm_func_t)]
def wasm_func_type(arg0: Any) -> pointer:
    return _wasm_func_type(arg0)  # type: ignore

_wasm_func_param_arity = dll.wasm_func_param_arity
_wasm_func_param_arity.restype = c_size_t
_wasm_func_param_arity.argtypes = [POINTER(wasm_func_t)]
def wasm_func_param_arity(arg0: Any) -> int:
    return _wasm_func_param_arity(arg0)  # type: ignore

_wasm_func_result_arity = dll.wasm_func_result_arity
_wasm_func_result_arity.restype = c_size_t
_wasm_func_result_arity.argtypes = [POINTER(wasm_func_t)]
def wasm_func_result_arity(arg0: Any) -> int:
    return _wasm_func_result_arity(arg0)  # type: ignore

_wasm_func_call = dll.wasm_func_call
_wasm_func_call.restype = POINTER(wasm_trap_t)
_wasm_func_call.argtypes = [POINTER(wasm_func_t), POINTER(wasm_val_t), POINTER(wasm_val_t)]
def wasm_func_call(arg0: Any, args: Any, results: Any) -> pointer:
    return _wasm_func_call(arg0, args, results)  # type: ignore

class wasm_global_t(Structure):
    pass

_wasm_global_delete = dll.wasm_global_delete
_wasm_global_delete.restype = None
_wasm_global_delete.argtypes = [POINTER(wasm_global_t)]
def wasm_global_delete(arg0: Any) -> None:
    return _wasm_global_delete(arg0)  # type: ignore

_wasm_global_copy = dll.wasm_global_copy
_wasm_global_copy.restype = POINTER(wasm_global_t)
_wasm_global_copy.argtypes = [POINTER(wasm_global_t)]
def wasm_global_copy(arg0: Any) -> pointer:
    return _wasm_global_copy(arg0)  # type: ignore

_wasm_global_same = dll.wasm_global_same
_wasm_global_same.restype = c_bool
_wasm_global_same.argtypes = [POINTER(wasm_global_t), POINTER(wasm_global_t)]
def wasm_global_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_global_same(arg0, arg1)  # type: ignore

_wasm_global_get_host_info = dll.wasm_global_get_host_info
_wasm_global_get_host_info.restype = c_void_p
_wasm_global_get_host_info.argtypes = [POINTER(wasm_global_t)]
def wasm_global_get_host_info(arg0: Any) -> pointer:
    return _wasm_global_get_host_info(arg0)  # type: ignore

_wasm_global_set_host_info = dll.wasm_global_set_host_info
_wasm_global_set_host_info.restype = None
_wasm_global_set_host_info.argtypes = [POINTER(wasm_global_t), c_void_p]
def wasm_global_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_global_set_host_info(arg0, arg1)  # type: ignore

_wasm_global_set_host_info_with_finalizer = dll.wasm_global_set_host_info_with_finalizer
_wasm_global_set_host_info_with_finalizer.restype = None
_wasm_global_set_host_info_with_finalizer.argtypes = [POINTER(wasm_global_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_global_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_global_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

_wasm_global_as_ref = dll.wasm_global_as_ref
_wasm_global_as_ref.restype = POINTER(wasm_ref_t)
_wasm_global_as_ref.argtypes = [POINTER(wasm_global_t)]
def wasm_global_as_ref(arg0: Any) -> pointer:
    return _wasm_global_as_ref(arg0)  # type: ignore

_wasm_global_as_ref_const = dll.wasm_global_as_ref_const
_wasm_global_as_ref_const.restype = POINTER(wasm_ref_t)
_wasm_global_as_ref_const.argtypes = [POINTER(wasm_global_t)]
def wasm_global_as_ref_const(arg0: Any) -> pointer:
    return _wasm_global_as_ref_const(arg0)  # type: ignore

_wasm_global_new = dll.wasm_global_new
_wasm_global_new.restype = POINTER(wasm_global_t)
_wasm_global_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_globaltype_t), POINTER(wasm_val_t)]
def wasm_global_new(arg0: Any, arg1: Any, arg2: Any) -> pointer:
    return _wasm_global_new(arg0, arg1, arg2)  # type: ignore

_wasm_global_type = dll.wasm_global_type
_wasm_global_type.restype = POINTER(wasm_globaltype_t)
_wasm_global_type.argtypes = [POINTER(wasm_global_t)]
def wasm_global_type(arg0: Any) -> pointer:
    return _wasm_global_type(arg0)  # type: ignore

_wasm_global_get = dll.wasm_global_get
_wasm_global_get.restype = None
_wasm_global_get.argtypes = [POINTER(wasm_global_t), POINTER(wasm_val_t)]
def wasm_global_get(arg0: Any, out: Any) -> None:
    return _wasm_global_get(arg0, out)  # type: ignore

_wasm_global_set = dll.wasm_global_set
_wasm_global_set.restype = None
_wasm_global_set.argtypes = [POINTER(wasm_global_t), POINTER(wasm_val_t)]
def wasm_global_set(arg0: Any, arg1: Any) -> None:
    return _wasm_global_set(arg0, arg1)  # type: ignore

class wasm_table_t(Structure):
    pass

_wasm_table_delete = dll.wasm_table_delete
_wasm_table_delete.restype = None
_wasm_table_delete.argtypes = [POINTER(wasm_table_t)]
def wasm_table_delete(arg0: Any) -> None:
    return _wasm_table_delete(arg0)  # type: ignore

_wasm_table_copy = dll.wasm_table_copy
_wasm_table_copy.restype = POINTER(wasm_table_t)
_wasm_table_copy.argtypes = [POINTER(wasm_table_t)]
def wasm_table_copy(arg0: Any) -> pointer:
    return _wasm_table_copy(arg0)  # type: ignore

_wasm_table_same = dll.wasm_table_same
_wasm_table_same.restype = c_bool
_wasm_table_same.argtypes = [POINTER(wasm_table_t), POINTER(wasm_table_t)]
def wasm_table_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_table_same(arg0, arg1)  # type: ignore

_wasm_table_get_host_info = dll.wasm_table_get_host_info
_wasm_table_get_host_info.restype = c_void_p
_wasm_table_get_host_info.argtypes = [POINTER(wasm_table_t)]
def wasm_table_get_host_info(arg0: Any) -> pointer:
    return _wasm_table_get_host_info(arg0)  # type: ignore

_wasm_table_set_host_info = dll.wasm_table_set_host_info
_wasm_table_set_host_info.restype = None
_wasm_table_set_host_info.argtypes = [POINTER(wasm_table_t), c_void_p]
def wasm_table_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_table_set_host_info(arg0, arg1)  # type: ignore

_wasm_table_set_host_info_with_finalizer = dll.wasm_table_set_host_info_with_finalizer
_wasm_table_set_host_info_with_finalizer.restype = None
_wasm_table_set_host_info_with_finalizer.argtypes = [POINTER(wasm_table_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_table_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_table_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

_wasm_table_as_ref = dll.wasm_table_as_ref
_wasm_table_as_ref.restype = POINTER(wasm_ref_t)
_wasm_table_as_ref.argtypes = [POINTER(wasm_table_t)]
def wasm_table_as_ref(arg0: Any) -> pointer:
    return _wasm_table_as_ref(arg0)  # type: ignore

_wasm_table_as_ref_const = dll.wasm_table_as_ref_const
_wasm_table_as_ref_const.restype = POINTER(wasm_ref_t)
_wasm_table_as_ref_const.argtypes = [POINTER(wasm_table_t)]
def wasm_table_as_ref_const(arg0: Any) -> pointer:
    return _wasm_table_as_ref_const(arg0)  # type: ignore

wasm_table_size_t = c_uint32

_wasm_table_new = dll.wasm_table_new
_wasm_table_new.restype = POINTER(wasm_table_t)
_wasm_table_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_tabletype_t), POINTER(wasm_ref_t)]
def wasm_table_new(arg0: Any, arg1: Any, init: Any) -> pointer:
    return _wasm_table_new(arg0, arg1, init)  # type: ignore

_wasm_table_type = dll.wasm_table_type
_wasm_table_type.restype = POINTER(wasm_tabletype_t)
_wasm_table_type.argtypes = [POINTER(wasm_table_t)]
def wasm_table_type(arg0: Any) -> pointer:
    return _wasm_table_type(arg0)  # type: ignore

_wasm_table_get = dll.wasm_table_get
_wasm_table_get.restype = POINTER(wasm_ref_t)
_wasm_table_get.argtypes = [POINTER(wasm_table_t), wasm_table_size_t]
def wasm_table_get(arg0: Any, index: Any) -> pointer:
    return _wasm_table_get(arg0, index)  # type: ignore

_wasm_table_set = dll.wasm_table_set
_wasm_table_set.restype = c_bool
_wasm_table_set.argtypes = [POINTER(wasm_table_t), wasm_table_size_t, POINTER(wasm_ref_t)]
def wasm_table_set(arg0: Any, index: Any, arg2: Any) -> c_bool:
    return _wasm_table_set(arg0, index, arg2)  # type: ignore

_wasm_table_size = dll.wasm_table_size
_wasm_table_size.restype = wasm_table_size_t
_wasm_table_size.argtypes = [POINTER(wasm_table_t)]
def wasm_table_size(arg0: Any) -> int:
    return _wasm_table_size(arg0)  # type: ignore

_wasm_table_grow = dll.wasm_table_grow
_wasm_table_grow.restype = c_bool
_wasm_table_grow.argtypes = [POINTER(wasm_table_t), wasm_table_size_t, POINTER(wasm_ref_t)]
def wasm_table_grow(arg0: Any, delta: Any, init: Any) -> c_bool:
    return _wasm_table_grow(arg0, delta, init)  # type: ignore

class wasm_memory_t(Structure):
    pass

_wasm_memory_delete = dll.wasm_memory_delete
_wasm_memory_delete.restype = None
_wasm_memory_delete.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_delete(arg0: Any) -> None:
    return _wasm_memory_delete(arg0)  # type: ignore

_wasm_memory_copy = dll.wasm_memory_copy
_wasm_memory_copy.restype = POINTER(wasm_memory_t)
_wasm_memory_copy.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_copy(arg0: Any) -> pointer:
    return _wasm_memory_copy(arg0)  # type: ignore

_wasm_memory_same = dll.wasm_memory_same
_wasm_memory_same.restype = c_bool
_wasm_memory_same.argtypes = [POINTER(wasm_memory_t), POINTER(wasm_memory_t)]
def wasm_memory_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_memory_same(arg0, arg1)  # type: ignore

_wasm_memory_get_host_info = dll.wasm_memory_get_host_info
_wasm_memory_get_host_info.restype = c_void_p
_wasm_memory_get_host_info.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_get_host_info(arg0: Any) -> pointer:
    return _wasm_memory_get_host_info(arg0)  # type: ignore

_wasm_memory_set_host_info = dll.wasm_memory_set_host_info
_wasm_memory_set_host_info.restype = None
_wasm_memory_set_host_info.argtypes = [POINTER(wasm_memory_t), c_void_p]
def wasm_memory_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_memory_set_host_info(arg0, arg1)  # type: ignore

_wasm_memory_set_host_info_with_finalizer = dll.wasm_memory_set_host_info_with_finalizer
_wasm_memory_set_host_info_with_finalizer.restype = None
_wasm_memory_set_host_info_with_finalizer.argtypes = [POINTER(wasm_memory_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_memory_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_memory_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

_wasm_memory_as_ref = dll.wasm_memory_as_ref
_wasm_memory_as_ref.restype = POINTER(wasm_ref_t)
_wasm_memory_as_ref.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_as_ref(arg0: Any) -> pointer:
    return _wasm_memory_as_ref(arg0)  # type: ignore

_wasm_memory_as_ref_const = dll.wasm_memory_as_ref_const
_wasm_memory_as_ref_const.restype = POINTER(wasm_ref_t)
_wasm_memory_as_ref_const.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_as_ref_const(arg0: Any) -> pointer:
    return _wasm_memory_as_ref_const(arg0)  # type: ignore

wasm_memory_pages_t = c_uint32

_wasm_memory_new = dll.wasm_memory_new
_wasm_memory_new.restype = POINTER(wasm_memory_t)
_wasm_memory_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_memorytype_t)]
def wasm_memory_new(arg0: Any, arg1: Any) -> pointer:
    return _wasm_memory_new(arg0, arg1)  # type: ignore

_wasm_memory_type = dll.wasm_memory_type
_wasm_memory_type.restype = POINTER(wasm_memorytype_t)
_wasm_memory_type.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_type(arg0: Any) -> pointer:
    return _wasm_memory_type(arg0)  # type: ignore

_wasm_memory_data = dll.wasm_memory_data
_wasm_memory_data.restype = POINTER(c_ubyte)
_wasm_memory_data.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_data(arg0: Any) -> pointer:
    return _wasm_memory_data(arg0)  # type: ignore

_wasm_memory_data_size = dll.wasm_memory_data_size
_wasm_memory_data_size.restype = c_size_t
_wasm_memory_data_size.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_data_size(arg0: Any) -> int:
    return _wasm_memory_data_size(arg0)  # type: ignore

_wasm_memory_size = dll.wasm_memory_size
_wasm_memory_size.restype = wasm_memory_pages_t
_wasm_memory_size.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_size(arg0: Any) -> int:
    return _wasm_memory_size(arg0)  # type: ignore

_wasm_memory_grow = dll.wasm_memory_grow
_wasm_memory_grow.restype = c_bool
_wasm_memory_grow.argtypes = [POINTER(wasm_memory_t), wasm_memory_pages_t]
def wasm_memory_grow(arg0: Any, delta: Any) -> c_bool:
    return _wasm_memory_grow(arg0, delta)  # type: ignore

class wasm_extern_t(Structure):
    pass

_wasm_extern_delete = dll.wasm_extern_delete
_wasm_extern_delete.restype = None
_wasm_extern_delete.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_delete(arg0: Any) -> None:
    return _wasm_extern_delete(arg0)  # type: ignore

_wasm_extern_copy = dll.wasm_extern_copy
_wasm_extern_copy.restype = POINTER(wasm_extern_t)
_wasm_extern_copy.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_copy(arg0: Any) -> pointer:
    return _wasm_extern_copy(arg0)  # type: ignore

_wasm_extern_same = dll.wasm_extern_same
_wasm_extern_same.restype = c_bool
_wasm_extern_same.argtypes = [POINTER(wasm_extern_t), POINTER(wasm_extern_t)]
def wasm_extern_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_extern_same(arg0, arg1)  # type: ignore

_wasm_extern_get_host_info = dll.wasm_extern_get_host_info
_wasm_extern_get_host_info.restype = c_void_p
_wasm_extern_get_host_info.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_get_host_info(arg0: Any) -> pointer:
    return _wasm_extern_get_host_info(arg0)  # type: ignore

_wasm_extern_set_host_info = dll.wasm_extern_set_host_info
_wasm_extern_set_host_info.restype = None
_wasm_extern_set_host_info.argtypes = [POINTER(wasm_extern_t), c_void_p]
def wasm_extern_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_extern_set_host_info(arg0, arg1)  # type: ignore

_wasm_extern_set_host_info_with_finalizer = dll.wasm_extern_set_host_info_with_finalizer
_wasm_extern_set_host_info_with_finalizer.restype = None
_wasm_extern_set_host_info_with_finalizer.argtypes = [POINTER(wasm_extern_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_extern_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_extern_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

_wasm_extern_as_ref = dll.wasm_extern_as_ref
_wasm_extern_as_ref.restype = POINTER(wasm_ref_t)
_wasm_extern_as_ref.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_ref(arg0: Any) -> pointer:
    return _wasm_extern_as_ref(arg0)  # type: ignore

_wasm_extern_as_ref_const = dll.wasm_extern_as_ref_const
_wasm_extern_as_ref_const.restype = POINTER(wasm_ref_t)
_wasm_extern_as_ref_const.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_ref_const(arg0: Any) -> pointer:
    return _wasm_extern_as_ref_const(arg0)  # type: ignore

class wasm_extern_vec_t(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("data", POINTER(POINTER(wasm_extern_t))),
    ]

_wasm_extern_vec_new_empty = dll.wasm_extern_vec_new_empty
_wasm_extern_vec_new_empty.restype = None
_wasm_extern_vec_new_empty.argtypes = [POINTER(wasm_extern_vec_t)]
def wasm_extern_vec_new_empty(out: Any) -> None:
    return _wasm_extern_vec_new_empty(out)  # type: ignore

_wasm_extern_vec_new_uninitialized = dll.wasm_extern_vec_new_uninitialized
_wasm_extern_vec_new_uninitialized.restype = None
_wasm_extern_vec_new_uninitialized.argtypes = [POINTER(wasm_extern_vec_t), c_size_t]
def wasm_extern_vec_new_uninitialized(out: Any, arg1: Any) -> None:
    return _wasm_extern_vec_new_uninitialized(out, arg1)  # type: ignore

_wasm_extern_vec_new = dll.wasm_extern_vec_new
_wasm_extern_vec_new.restype = None
_wasm_extern_vec_new.argtypes = [POINTER(wasm_extern_vec_t), c_size_t, POINTER(POINTER(wasm_extern_t))]
def wasm_extern_vec_new(out: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_extern_vec_new(out, arg1, arg2)  # type: ignore

_wasm_extern_vec_copy = dll.wasm_extern_vec_copy
_wasm_extern_vec_copy.restype = None
_wasm_extern_vec_copy.argtypes = [POINTER(wasm_extern_vec_t), POINTER(wasm_extern_vec_t)]
def wasm_extern_vec_copy(out: Any, arg1: Any) -> None:
    return _wasm_extern_vec_copy(out, arg1)  # type: ignore

_wasm_extern_vec_delete = dll.wasm_extern_vec_delete
_wasm_extern_vec_delete.restype = None
_wasm_extern_vec_delete.argtypes = [POINTER(wasm_extern_vec_t)]
def wasm_extern_vec_delete(arg0: Any) -> None:
    return _wasm_extern_vec_delete(arg0)  # type: ignore

_wasm_extern_kind = dll.wasm_extern_kind
_wasm_extern_kind.restype = wasm_externkind_t
_wasm_extern_kind.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_kind(arg0: Any) -> wasm_externkind_t:
    return _wasm_extern_kind(arg0)  # type: ignore

_wasm_extern_type = dll.wasm_extern_type
_wasm_extern_type.restype = POINTER(wasm_externtype_t)
_wasm_extern_type.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_type(arg0: Any) -> pointer:
    return _wasm_extern_type(arg0)  # type: ignore

_wasm_func_as_extern = dll.wasm_func_as_extern
_wasm_func_as_extern.restype = POINTER(wasm_extern_t)
_wasm_func_as_extern.argtypes = [POINTER(wasm_func_t)]
def wasm_func_as_extern(arg0: Any) -> pointer:
    return _wasm_func_as_extern(arg0)  # type: ignore

_wasm_global_as_extern = dll.wasm_global_as_extern
_wasm_global_as_extern.restype = POINTER(wasm_extern_t)
_wasm_global_as_extern.argtypes = [POINTER(wasm_global_t)]
def wasm_global_as_extern(arg0: Any) -> pointer:
    return _wasm_global_as_extern(arg0)  # type: ignore

_wasm_table_as_extern = dll.wasm_table_as_extern
_wasm_table_as_extern.restype = POINTER(wasm_extern_t)
_wasm_table_as_extern.argtypes = [POINTER(wasm_table_t)]
def wasm_table_as_extern(arg0: Any) -> pointer:
    return _wasm_table_as_extern(arg0)  # type: ignore

_wasm_memory_as_extern = dll.wasm_memory_as_extern
_wasm_memory_as_extern.restype = POINTER(wasm_extern_t)
_wasm_memory_as_extern.argtypes = [POINTER(wasm_memory_t)]
def wasm_memory_as_extern(arg0: Any) -> pointer:
    return _wasm_memory_as_extern(arg0)  # type: ignore

_wasm_extern_as_func = dll.wasm_extern_as_func
_wasm_extern_as_func.restype = POINTER(wasm_func_t)
_wasm_extern_as_func.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_func(arg0: Any) -> pointer:
    return _wasm_extern_as_func(arg0)  # type: ignore

_wasm_extern_as_global = dll.wasm_extern_as_global
_wasm_extern_as_global.restype = POINTER(wasm_global_t)
_wasm_extern_as_global.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_global(arg0: Any) -> pointer:
    return _wasm_extern_as_global(arg0)  # type: ignore

_wasm_extern_as_table = dll.wasm_extern_as_table
_wasm_extern_as_table.restype = POINTER(wasm_table_t)
_wasm_extern_as_table.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_table(arg0: Any) -> pointer:
    return _wasm_extern_as_table(arg0)  # type: ignore

_wasm_extern_as_memory = dll.wasm_extern_as_memory
_wasm_extern_as_memory.restype = POINTER(wasm_memory_t)
_wasm_extern_as_memory.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_memory(arg0: Any) -> pointer:
    return _wasm_extern_as_memory(arg0)  # type: ignore

_wasm_extern_as_func_const = dll.wasm_extern_as_func_const
_wasm_extern_as_func_const.restype = POINTER(wasm_func_t)
_wasm_extern_as_func_const.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_func_const(arg0: Any) -> pointer:
    return _wasm_extern_as_func_const(arg0)  # type: ignore

_wasm_extern_as_global_const = dll.wasm_extern_as_global_const
_wasm_extern_as_global_const.restype = POINTER(wasm_global_t)
_wasm_extern_as_global_const.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_global_const(arg0: Any) -> pointer:
    return _wasm_extern_as_global_const(arg0)  # type: ignore

_wasm_extern_as_table_const = dll.wasm_extern_as_table_const
_wasm_extern_as_table_const.restype = POINTER(wasm_table_t)
_wasm_extern_as_table_const.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_table_const(arg0: Any) -> pointer:
    return _wasm_extern_as_table_const(arg0)  # type: ignore

_wasm_extern_as_memory_const = dll.wasm_extern_as_memory_const
_wasm_extern_as_memory_const.restype = POINTER(wasm_memory_t)
_wasm_extern_as_memory_const.argtypes = [POINTER(wasm_extern_t)]
def wasm_extern_as_memory_const(arg0: Any) -> pointer:
    return _wasm_extern_as_memory_const(arg0)  # type: ignore

class wasm_instance_t(Structure):
    pass

_wasm_instance_delete = dll.wasm_instance_delete
_wasm_instance_delete.restype = None
_wasm_instance_delete.argtypes = [POINTER(wasm_instance_t)]
def wasm_instance_delete(arg0: Any) -> None:
    return _wasm_instance_delete(arg0)  # type: ignore

_wasm_instance_copy = dll.wasm_instance_copy
_wasm_instance_copy.restype = POINTER(wasm_instance_t)
_wasm_instance_copy.argtypes = [POINTER(wasm_instance_t)]
def wasm_instance_copy(arg0: Any) -> pointer:
    return _wasm_instance_copy(arg0)  # type: ignore

_wasm_instance_same = dll.wasm_instance_same
_wasm_instance_same.restype = c_bool
_wasm_instance_same.argtypes = [POINTER(wasm_instance_t), POINTER(wasm_instance_t)]
def wasm_instance_same(arg0: Any, arg1: Any) -> c_bool:
    return _wasm_instance_same(arg0, arg1)  # type: ignore

_wasm_instance_get_host_info = dll.wasm_instance_get_host_info
_wasm_instance_get_host_info.restype = c_void_p
_wasm_instance_get_host_info.argtypes = [POINTER(wasm_instance_t)]
def wasm_instance_get_host_info(arg0: Any) -> pointer:
    return _wasm_instance_get_host_info(arg0)  # type: ignore

_wasm_instance_set_host_info = dll.wasm_instance_set_host_info
_wasm_instance_set_host_info.restype = None
_wasm_instance_set_host_info.argtypes = [POINTER(wasm_instance_t), c_void_p]
def wasm_instance_set_host_info(arg0: Any, arg1: Any) -> None:
    return _wasm_instance_set_host_info(arg0, arg1)  # type: ignore

_wasm_instance_set_host_info_with_finalizer = dll.wasm_instance_set_host_info_with_finalizer
_wasm_instance_set_host_info_with_finalizer.restype = None
_wasm_instance_set_host_info_with_finalizer.argtypes = [POINTER(wasm_instance_t), c_void_p, CFUNCTYPE(None, c_void_p)]
def wasm_instance_set_host_info_with_finalizer(arg0: Any, arg1: Any, arg2: Any) -> None:
    return _wasm_instance_set_host_info_with_finalizer(arg0, arg1, arg2)  # type: ignore

_wasm_instance_as_ref = dll.wasm_instance_as_ref
_wasm_instance_as_ref.restype = POINTER(wasm_ref_t)
_wasm_instance_as_ref.argtypes = [POINTER(wasm_instance_t)]
def wasm_instance_as_ref(arg0: Any) -> pointer:
    return _wasm_instance_as_ref(arg0)  # type: ignore

_wasm_instance_as_ref_const = dll.wasm_instance_as_ref_const
_wasm_instance_as_ref_const.restype = POINTER(wasm_ref_t)
_wasm_instance_as_ref_const.argtypes = [POINTER(wasm_instance_t)]
def wasm_instance_as_ref_const(arg0: Any) -> pointer:
    return _wasm_instance_as_ref_const(arg0)  # type: ignore

_wasm_instance_new = dll.wasm_instance_new
_wasm_instance_new.restype = POINTER(wasm_instance_t)
_wasm_instance_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_module_t), POINTER(POINTER(wasm_extern_t)), POINTER(POINTER(wasm_trap_t))]
def wasm_instance_new(arg0: Any, arg1: Any, imports: Any, arg3: Any) -> pointer:
    return _wasm_instance_new(arg0, arg1, imports, arg3)  # type: ignore

_wasm_instance_exports = dll.wasm_instance_exports
_wasm_instance_exports.restype = None
_wasm_instance_exports.argtypes = [POINTER(wasm_instance_t), POINTER(wasm_extern_vec_t)]
def wasm_instance_exports(arg0: Any, out: Any) -> None:
    return _wasm_instance_exports(arg0, out)  # type: ignore

class wasi_config_t(Structure):
    pass

_wasi_config_delete = dll.wasi_config_delete
_wasi_config_delete.restype = None
_wasi_config_delete.argtypes = [POINTER(wasi_config_t)]
def wasi_config_delete(arg0: Any) -> None:
    return _wasi_config_delete(arg0)  # type: ignore

_wasi_config_new = dll.wasi_config_new
_wasi_config_new.restype = POINTER(wasi_config_t)
_wasi_config_new.argtypes = []
def wasi_config_new() -> pointer:
    return _wasi_config_new()  # type: ignore

_wasi_config_set_argv = dll.wasi_config_set_argv
_wasi_config_set_argv.restype = None
_wasi_config_set_argv.argtypes = [POINTER(wasi_config_t), c_int, POINTER(POINTER(c_char))]
def wasi_config_set_argv(config: Any, argc: Any, argv: Any) -> None:
    return _wasi_config_set_argv(config, argc, argv)  # type: ignore

_wasi_config_inherit_argv = dll.wasi_config_inherit_argv
_wasi_config_inherit_argv.restype = None
_wasi_config_inherit_argv.argtypes = [POINTER(wasi_config_t)]
def wasi_config_inherit_argv(config: Any) -> None:
    return _wasi_config_inherit_argv(config)  # type: ignore

_wasi_config_set_env = dll.wasi_config_set_env
_wasi_config_set_env.restype = None
_wasi_config_set_env.argtypes = [POINTER(wasi_config_t), c_int, POINTER(POINTER(c_char)), POINTER(POINTER(c_char))]
def wasi_config_set_env(config: Any, envc: Any, names: Any, values: Any) -> None:
    return _wasi_config_set_env(config, envc, names, values)  # type: ignore

_wasi_config_inherit_env = dll.wasi_config_inherit_env
_wasi_config_inherit_env.restype = None
_wasi_config_inherit_env.argtypes = [POINTER(wasi_config_t)]
def wasi_config_inherit_env(config: Any) -> None:
    return _wasi_config_inherit_env(config)  # type: ignore

_wasi_config_set_stdin_file = dll.wasi_config_set_stdin_file
_wasi_config_set_stdin_file.restype = c_bool
_wasi_config_set_stdin_file.argtypes = [POINTER(wasi_config_t), POINTER(c_char)]
def wasi_config_set_stdin_file(config: Any, path: Any) -> c_bool:
    return _wasi_config_set_stdin_file(config, path)  # type: ignore

_wasi_config_inherit_stdin = dll.wasi_config_inherit_stdin
_wasi_config_inherit_stdin.restype = None
_wasi_config_inherit_stdin.argtypes = [POINTER(wasi_config_t)]
def wasi_config_inherit_stdin(config: Any) -> None:
    return _wasi_config_inherit_stdin(config)  # type: ignore

_wasi_config_set_stdout_file = dll.wasi_config_set_stdout_file
_wasi_config_set_stdout_file.restype = c_bool
_wasi_config_set_stdout_file.argtypes = [POINTER(wasi_config_t), POINTER(c_char)]
def wasi_config_set_stdout_file(config: Any, path: Any) -> c_bool:
    return _wasi_config_set_stdout_file(config, path)  # type: ignore

_wasi_config_inherit_stdout = dll.wasi_config_inherit_stdout
_wasi_config_inherit_stdout.restype = None
_wasi_config_inherit_stdout.argtypes = [POINTER(wasi_config_t)]
def wasi_config_inherit_stdout(config: Any) -> None:
    return _wasi_config_inherit_stdout(config)  # type: ignore

_wasi_config_set_stderr_file = dll.wasi_config_set_stderr_file
_wasi_config_set_stderr_file.restype = c_bool
_wasi_config_set_stderr_file.argtypes = [POINTER(wasi_config_t), POINTER(c_char)]
def wasi_config_set_stderr_file(config: Any, path: Any) -> c_bool:
    return _wasi_config_set_stderr_file(config, path)  # type: ignore

_wasi_config_inherit_stderr = dll.wasi_config_inherit_stderr
_wasi_config_inherit_stderr.restype = None
_wasi_config_inherit_stderr.argtypes = [POINTER(wasi_config_t)]
def wasi_config_inherit_stderr(config: Any) -> None:
    return _wasi_config_inherit_stderr(config)  # type: ignore

_wasi_config_preopen_dir = dll.wasi_config_preopen_dir
_wasi_config_preopen_dir.restype = c_bool
_wasi_config_preopen_dir.argtypes = [POINTER(wasi_config_t), POINTER(c_char), POINTER(c_char)]
def wasi_config_preopen_dir(config: Any, path: Any, guest_path: Any) -> c_bool:
    return _wasi_config_preopen_dir(config, path, guest_path)  # type: ignore

class wasi_instance_t(Structure):
    pass

_wasi_instance_delete = dll.wasi_instance_delete
_wasi_instance_delete.restype = None
_wasi_instance_delete.argtypes = [POINTER(wasi_instance_t)]
def wasi_instance_delete(arg0: Any) -> None:
    return _wasi_instance_delete(arg0)  # type: ignore

_wasi_instance_new = dll.wasi_instance_new
_wasi_instance_new.restype = POINTER(wasi_instance_t)
_wasi_instance_new.argtypes = [POINTER(wasm_store_t), POINTER(c_char), POINTER(wasi_config_t), POINTER(POINTER(wasm_trap_t))]
def wasi_instance_new(store: Any, name: Any, config: Any, trap: Any) -> pointer:
    return _wasi_instance_new(store, name, config, trap)  # type: ignore

_wasi_instance_bind_import = dll.wasi_instance_bind_import
_wasi_instance_bind_import.restype = POINTER(wasm_extern_t)
_wasi_instance_bind_import.argtypes = [POINTER(wasi_instance_t), POINTER(wasm_importtype_t)]
def wasi_instance_bind_import(instance: Any, arg1: Any) -> pointer:
    return _wasi_instance_bind_import(instance, arg1)  # type: ignore

class wasmtime_error_t(Structure):
    pass

_wasmtime_error_delete = dll.wasmtime_error_delete
_wasmtime_error_delete.restype = None
_wasmtime_error_delete.argtypes = [POINTER(wasmtime_error_t)]
def wasmtime_error_delete(arg0: Any) -> None:
    return _wasmtime_error_delete(arg0)  # type: ignore

_wasmtime_error_message = dll.wasmtime_error_message
_wasmtime_error_message.restype = None
_wasmtime_error_message.argtypes = [POINTER(wasmtime_error_t), POINTER(wasm_name_t)]
def wasmtime_error_message(error: Any, message: Any) -> None:
    return _wasmtime_error_message(error, message)  # type: ignore

wasmtime_strategy_t = c_uint8

wasmtime_opt_level_t = c_uint8

wasmtime_profiling_strategy_t = c_uint8

_wasmtime_config_debug_info_set = dll.wasmtime_config_debug_info_set
_wasmtime_config_debug_info_set.restype = None
_wasmtime_config_debug_info_set.argtypes = [POINTER(wasm_config_t), c_bool]
def wasmtime_config_debug_info_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_debug_info_set(arg0, arg1)  # type: ignore

_wasmtime_config_interruptable_set = dll.wasmtime_config_interruptable_set
_wasmtime_config_interruptable_set.restype = None
_wasmtime_config_interruptable_set.argtypes = [POINTER(wasm_config_t), c_bool]
def wasmtime_config_interruptable_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_interruptable_set(arg0, arg1)  # type: ignore

_wasmtime_config_max_wasm_stack_set = dll.wasmtime_config_max_wasm_stack_set
_wasmtime_config_max_wasm_stack_set.restype = None
_wasmtime_config_max_wasm_stack_set.argtypes = [POINTER(wasm_config_t), c_size_t]
def wasmtime_config_max_wasm_stack_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_max_wasm_stack_set(arg0, arg1)  # type: ignore

_wasmtime_config_wasm_threads_set = dll.wasmtime_config_wasm_threads_set
_wasmtime_config_wasm_threads_set.restype = None
_wasmtime_config_wasm_threads_set.argtypes = [POINTER(wasm_config_t), c_bool]
def wasmtime_config_wasm_threads_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_wasm_threads_set(arg0, arg1)  # type: ignore

_wasmtime_config_wasm_reference_types_set = dll.wasmtime_config_wasm_reference_types_set
_wasmtime_config_wasm_reference_types_set.restype = None
_wasmtime_config_wasm_reference_types_set.argtypes = [POINTER(wasm_config_t), c_bool]
def wasmtime_config_wasm_reference_types_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_wasm_reference_types_set(arg0, arg1)  # type: ignore

_wasmtime_config_wasm_simd_set = dll.wasmtime_config_wasm_simd_set
_wasmtime_config_wasm_simd_set.restype = None
_wasmtime_config_wasm_simd_set.argtypes = [POINTER(wasm_config_t), c_bool]
def wasmtime_config_wasm_simd_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_wasm_simd_set(arg0, arg1)  # type: ignore

_wasmtime_config_wasm_bulk_memory_set = dll.wasmtime_config_wasm_bulk_memory_set
_wasmtime_config_wasm_bulk_memory_set.restype = None
_wasmtime_config_wasm_bulk_memory_set.argtypes = [POINTER(wasm_config_t), c_bool]
def wasmtime_config_wasm_bulk_memory_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_wasm_bulk_memory_set(arg0, arg1)  # type: ignore

_wasmtime_config_wasm_multi_value_set = dll.wasmtime_config_wasm_multi_value_set
_wasmtime_config_wasm_multi_value_set.restype = None
_wasmtime_config_wasm_multi_value_set.argtypes = [POINTER(wasm_config_t), c_bool]
def wasmtime_config_wasm_multi_value_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_wasm_multi_value_set(arg0, arg1)  # type: ignore

_wasmtime_config_strategy_set = dll.wasmtime_config_strategy_set
_wasmtime_config_strategy_set.restype = POINTER(wasmtime_error_t)
_wasmtime_config_strategy_set.argtypes = [POINTER(wasm_config_t), wasmtime_strategy_t]
def wasmtime_config_strategy_set(arg0: Any, arg1: Any) -> pointer:
    return _wasmtime_config_strategy_set(arg0, arg1)  # type: ignore

_wasmtime_config_cranelift_debug_verifier_set = dll.wasmtime_config_cranelift_debug_verifier_set
_wasmtime_config_cranelift_debug_verifier_set.restype = None
_wasmtime_config_cranelift_debug_verifier_set.argtypes = [POINTER(wasm_config_t), c_bool]
def wasmtime_config_cranelift_debug_verifier_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_cranelift_debug_verifier_set(arg0, arg1)  # type: ignore

_wasmtime_config_cranelift_opt_level_set = dll.wasmtime_config_cranelift_opt_level_set
_wasmtime_config_cranelift_opt_level_set.restype = None
_wasmtime_config_cranelift_opt_level_set.argtypes = [POINTER(wasm_config_t), wasmtime_opt_level_t]
def wasmtime_config_cranelift_opt_level_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_cranelift_opt_level_set(arg0, arg1)  # type: ignore

_wasmtime_config_profiler_set = dll.wasmtime_config_profiler_set
_wasmtime_config_profiler_set.restype = POINTER(wasmtime_error_t)
_wasmtime_config_profiler_set.argtypes = [POINTER(wasm_config_t), wasmtime_profiling_strategy_t]
def wasmtime_config_profiler_set(arg0: Any, arg1: Any) -> pointer:
    return _wasmtime_config_profiler_set(arg0, arg1)  # type: ignore

_wasmtime_config_static_memory_maximum_size_set = dll.wasmtime_config_static_memory_maximum_size_set
_wasmtime_config_static_memory_maximum_size_set.restype = None
_wasmtime_config_static_memory_maximum_size_set.argtypes = [POINTER(wasm_config_t), c_uint64]
def wasmtime_config_static_memory_maximum_size_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_static_memory_maximum_size_set(arg0, arg1)  # type: ignore

_wasmtime_config_static_memory_guard_size_set = dll.wasmtime_config_static_memory_guard_size_set
_wasmtime_config_static_memory_guard_size_set.restype = None
_wasmtime_config_static_memory_guard_size_set.argtypes = [POINTER(wasm_config_t), c_uint64]
def wasmtime_config_static_memory_guard_size_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_static_memory_guard_size_set(arg0, arg1)  # type: ignore

_wasmtime_config_dynamic_memory_guard_size_set = dll.wasmtime_config_dynamic_memory_guard_size_set
_wasmtime_config_dynamic_memory_guard_size_set.restype = None
_wasmtime_config_dynamic_memory_guard_size_set.argtypes = [POINTER(wasm_config_t), c_uint64]
def wasmtime_config_dynamic_memory_guard_size_set(arg0: Any, arg1: Any) -> None:
    return _wasmtime_config_dynamic_memory_guard_size_set(arg0, arg1)  # type: ignore

_wasmtime_config_cache_config_load = dll.wasmtime_config_cache_config_load
_wasmtime_config_cache_config_load.restype = POINTER(wasmtime_error_t)
_wasmtime_config_cache_config_load.argtypes = [POINTER(wasm_config_t), POINTER(c_char)]
def wasmtime_config_cache_config_load(arg0: Any, arg1: Any) -> pointer:
    return _wasmtime_config_cache_config_load(arg0, arg1)  # type: ignore

_wasmtime_wat2wasm = dll.wasmtime_wat2wasm
_wasmtime_wat2wasm.restype = POINTER(wasmtime_error_t)
_wasmtime_wat2wasm.argtypes = [POINTER(wasm_byte_vec_t), POINTER(wasm_byte_vec_t)]
def wasmtime_wat2wasm(wat: Any, ret: Any) -> pointer:
    return _wasmtime_wat2wasm(wat, ret)  # type: ignore

_wasmtime_store_gc = dll.wasmtime_store_gc
_wasmtime_store_gc.restype = None
_wasmtime_store_gc.argtypes = [POINTER(wasm_store_t)]
def wasmtime_store_gc(store: Any) -> None:
    return _wasmtime_store_gc(store)  # type: ignore

class wasmtime_linker_t(Structure):
    pass

_wasmtime_linker_delete = dll.wasmtime_linker_delete
_wasmtime_linker_delete.restype = None
_wasmtime_linker_delete.argtypes = [POINTER(wasmtime_linker_t)]
def wasmtime_linker_delete(arg0: Any) -> None:
    return _wasmtime_linker_delete(arg0)  # type: ignore

_wasmtime_linker_new = dll.wasmtime_linker_new
_wasmtime_linker_new.restype = POINTER(wasmtime_linker_t)
_wasmtime_linker_new.argtypes = [POINTER(wasm_store_t)]
def wasmtime_linker_new(store: Any) -> pointer:
    return _wasmtime_linker_new(store)  # type: ignore

_wasmtime_linker_allow_shadowing = dll.wasmtime_linker_allow_shadowing
_wasmtime_linker_allow_shadowing.restype = None
_wasmtime_linker_allow_shadowing.argtypes = [POINTER(wasmtime_linker_t), c_bool]
def wasmtime_linker_allow_shadowing(linker: Any, allow_shadowing: Any) -> None:
    return _wasmtime_linker_allow_shadowing(linker, allow_shadowing)  # type: ignore

_wasmtime_linker_define = dll.wasmtime_linker_define
_wasmtime_linker_define.restype = POINTER(wasmtime_error_t)
_wasmtime_linker_define.argtypes = [POINTER(wasmtime_linker_t), POINTER(wasm_name_t), POINTER(wasm_name_t), POINTER(wasm_extern_t)]
def wasmtime_linker_define(linker: Any, module: Any, name: Any, item: Any) -> pointer:
    return _wasmtime_linker_define(linker, module, name, item)  # type: ignore

_wasmtime_linker_define_wasi = dll.wasmtime_linker_define_wasi
_wasmtime_linker_define_wasi.restype = POINTER(wasmtime_error_t)
_wasmtime_linker_define_wasi.argtypes = [POINTER(wasmtime_linker_t), POINTER(wasi_instance_t)]
def wasmtime_linker_define_wasi(linker: Any, instance: Any) -> pointer:
    return _wasmtime_linker_define_wasi(linker, instance)  # type: ignore

_wasmtime_linker_define_instance = dll.wasmtime_linker_define_instance
_wasmtime_linker_define_instance.restype = POINTER(wasmtime_error_t)
_wasmtime_linker_define_instance.argtypes = [POINTER(wasmtime_linker_t), POINTER(wasm_name_t), POINTER(wasm_instance_t)]
def wasmtime_linker_define_instance(linker: Any, name: Any, instance: Any) -> pointer:
    return _wasmtime_linker_define_instance(linker, name, instance)  # type: ignore

_wasmtime_linker_instantiate = dll.wasmtime_linker_instantiate
_wasmtime_linker_instantiate.restype = POINTER(wasmtime_error_t)
_wasmtime_linker_instantiate.argtypes = [POINTER(wasmtime_linker_t), POINTER(wasm_module_t), POINTER(POINTER(wasm_instance_t)), POINTER(POINTER(wasm_trap_t))]
def wasmtime_linker_instantiate(linker: Any, module: Any, instance: Any, trap: Any) -> pointer:
    return _wasmtime_linker_instantiate(linker, module, instance, trap)  # type: ignore

_wasmtime_linker_module = dll.wasmtime_linker_module
_wasmtime_linker_module.restype = POINTER(wasmtime_error_t)
_wasmtime_linker_module.argtypes = [POINTER(wasmtime_linker_t), POINTER(wasm_name_t), POINTER(wasm_module_t)]
def wasmtime_linker_module(linker: Any, name: Any, module: Any) -> pointer:
    return _wasmtime_linker_module(linker, name, module)  # type: ignore

_wasmtime_linker_get_default = dll.wasmtime_linker_get_default
_wasmtime_linker_get_default.restype = POINTER(wasmtime_error_t)
_wasmtime_linker_get_default.argtypes = [POINTER(wasmtime_linker_t), POINTER(wasm_name_t), POINTER(POINTER(wasm_func_t))]
def wasmtime_linker_get_default(linker: Any, name: Any, func: Any) -> pointer:
    return _wasmtime_linker_get_default(linker, name, func)  # type: ignore

_wasmtime_linker_get_one_by_name = dll.wasmtime_linker_get_one_by_name
_wasmtime_linker_get_one_by_name.restype = POINTER(wasmtime_error_t)
_wasmtime_linker_get_one_by_name.argtypes = [POINTER(wasmtime_linker_t), POINTER(wasm_name_t), POINTER(wasm_name_t), POINTER(POINTER(wasm_extern_t))]
def wasmtime_linker_get_one_by_name(linker: Any, module: Any, name: Any, item: Any) -> pointer:
    return _wasmtime_linker_get_one_by_name(linker, module, name, item)  # type: ignore

class wasmtime_caller_t(Structure):
    pass

wasmtime_func_callback_t = CFUNCTYPE(c_size_t, POINTER(wasmtime_caller_t), POINTER(wasm_val_t), POINTER(wasm_val_t))

wasmtime_func_callback_with_env_t = CFUNCTYPE(c_size_t, POINTER(wasmtime_caller_t), c_void_p, POINTER(wasm_val_t), POINTER(wasm_val_t))

_wasmtime_func_new = dll.wasmtime_func_new
_wasmtime_func_new.restype = POINTER(wasm_func_t)
_wasmtime_func_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_functype_t), wasmtime_func_callback_t]
def wasmtime_func_new(arg0: Any, arg1: Any, callback: Any) -> pointer:
    return _wasmtime_func_new(arg0, arg1, callback)  # type: ignore

_wasmtime_func_new_with_env = dll.wasmtime_func_new_with_env
_wasmtime_func_new_with_env.restype = POINTER(wasm_func_t)
_wasmtime_func_new_with_env.argtypes = [POINTER(wasm_store_t), POINTER(wasm_functype_t), wasmtime_func_callback_with_env_t, c_void_p, CFUNCTYPE(None, c_void_p)]
def wasmtime_func_new_with_env(store: Any, type: Any, callback: Any, env: Any, finalizer: Any) -> pointer:
    return _wasmtime_func_new_with_env(store, type, callback, env, finalizer)  # type: ignore

_wasmtime_func_as_funcref = dll.wasmtime_func_as_funcref
_wasmtime_func_as_funcref.restype = None
_wasmtime_func_as_funcref.argtypes = [POINTER(wasm_func_t), POINTER(wasm_val_t)]
def wasmtime_func_as_funcref(func: Any, funcrefp: Any) -> None:
    return _wasmtime_func_as_funcref(func, funcrefp)  # type: ignore

_wasmtime_funcref_as_func = dll.wasmtime_funcref_as_func
_wasmtime_funcref_as_func.restype = POINTER(wasm_func_t)
_wasmtime_funcref_as_func.argtypes = [POINTER(wasm_val_t)]
def wasmtime_funcref_as_func(val: Any) -> pointer:
    return _wasmtime_funcref_as_func(val)  # type: ignore

_wasmtime_caller_export_get = dll.wasmtime_caller_export_get
_wasmtime_caller_export_get.restype = POINTER(wasm_extern_t)
_wasmtime_caller_export_get.argtypes = [POINTER(wasmtime_caller_t), POINTER(wasm_name_t)]
def wasmtime_caller_export_get(caller: Any, name: Any) -> pointer:
    return _wasmtime_caller_export_get(caller, name)  # type: ignore

class wasmtime_interrupt_handle_t(Structure):
    pass

_wasmtime_interrupt_handle_delete = dll.wasmtime_interrupt_handle_delete
_wasmtime_interrupt_handle_delete.restype = None
_wasmtime_interrupt_handle_delete.argtypes = [POINTER(wasmtime_interrupt_handle_t)]
def wasmtime_interrupt_handle_delete(arg0: Any) -> None:
    return _wasmtime_interrupt_handle_delete(arg0)  # type: ignore

_wasmtime_interrupt_handle_new = dll.wasmtime_interrupt_handle_new
_wasmtime_interrupt_handle_new.restype = POINTER(wasmtime_interrupt_handle_t)
_wasmtime_interrupt_handle_new.argtypes = [POINTER(wasm_store_t)]
def wasmtime_interrupt_handle_new(store: Any) -> pointer:
    return _wasmtime_interrupt_handle_new(store)  # type: ignore

_wasmtime_interrupt_handle_interrupt = dll.wasmtime_interrupt_handle_interrupt
_wasmtime_interrupt_handle_interrupt.restype = None
_wasmtime_interrupt_handle_interrupt.argtypes = [POINTER(wasmtime_interrupt_handle_t)]
def wasmtime_interrupt_handle_interrupt(handle: Any) -> None:
    return _wasmtime_interrupt_handle_interrupt(handle)  # type: ignore

_wasmtime_trap_exit_status = dll.wasmtime_trap_exit_status
_wasmtime_trap_exit_status.restype = c_bool
_wasmtime_trap_exit_status.argtypes = [POINTER(wasm_trap_t), POINTER(c_int)]
def wasmtime_trap_exit_status(arg0: Any, status: Any) -> c_bool:
    return _wasmtime_trap_exit_status(arg0, status)  # type: ignore

_wasmtime_frame_func_name = dll.wasmtime_frame_func_name
_wasmtime_frame_func_name.restype = POINTER(wasm_name_t)
_wasmtime_frame_func_name.argtypes = [POINTER(wasm_frame_t)]
def wasmtime_frame_func_name(arg0: Any) -> pointer:
    return _wasmtime_frame_func_name(arg0)  # type: ignore

_wasmtime_frame_module_name = dll.wasmtime_frame_module_name
_wasmtime_frame_module_name.restype = POINTER(wasm_name_t)
_wasmtime_frame_module_name.argtypes = [POINTER(wasm_frame_t)]
def wasmtime_frame_module_name(arg0: Any) -> pointer:
    return _wasmtime_frame_module_name(arg0)  # type: ignore

_wasmtime_func_call = dll.wasmtime_func_call
_wasmtime_func_call.restype = POINTER(wasmtime_error_t)
_wasmtime_func_call.argtypes = [POINTER(wasm_func_t), POINTER(wasm_val_t), c_size_t, POINTER(wasm_val_t), c_size_t, POINTER(POINTER(wasm_trap_t))]
def wasmtime_func_call(func: Any, args: Any, num_args: Any, results: Any, num_results: Any, trap: Any) -> pointer:
    return _wasmtime_func_call(func, args, num_args, results, num_results, trap)  # type: ignore

_wasmtime_global_new = dll.wasmtime_global_new
_wasmtime_global_new.restype = POINTER(wasmtime_error_t)
_wasmtime_global_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_globaltype_t), POINTER(wasm_val_t), POINTER(POINTER(wasm_global_t))]
def wasmtime_global_new(store: Any, type: Any, val: Any, ret: Any) -> pointer:
    return _wasmtime_global_new(store, type, val, ret)  # type: ignore

_wasmtime_global_set = dll.wasmtime_global_set
_wasmtime_global_set.restype = POINTER(wasmtime_error_t)
_wasmtime_global_set.argtypes = [POINTER(wasm_global_t), POINTER(wasm_val_t)]
def wasmtime_global_set(arg0: Any, val: Any) -> pointer:
    return _wasmtime_global_set(arg0, val)  # type: ignore

_wasmtime_instance_new = dll.wasmtime_instance_new
_wasmtime_instance_new.restype = POINTER(wasmtime_error_t)
_wasmtime_instance_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_module_t), POINTER(POINTER(wasm_extern_t)), c_size_t, POINTER(POINTER(wasm_instance_t)), POINTER(POINTER(wasm_trap_t))]
def wasmtime_instance_new(store: Any, module: Any, imports: Any, num_imports: Any, instance: Any, trap: Any) -> pointer:
    return _wasmtime_instance_new(store, module, imports, num_imports, instance, trap)  # type: ignore

_wasmtime_module_new = dll.wasmtime_module_new
_wasmtime_module_new.restype = POINTER(wasmtime_error_t)
_wasmtime_module_new.argtypes = [POINTER(wasm_engine_t), POINTER(wasm_byte_vec_t), POINTER(POINTER(wasm_module_t))]
def wasmtime_module_new(engine: Any, binary: Any, ret: Any) -> pointer:
    return _wasmtime_module_new(engine, binary, ret)  # type: ignore

_wasmtime_module_validate = dll.wasmtime_module_validate
_wasmtime_module_validate.restype = POINTER(wasmtime_error_t)
_wasmtime_module_validate.argtypes = [POINTER(wasm_store_t), POINTER(wasm_byte_vec_t)]
def wasmtime_module_validate(store: Any, binary: Any) -> pointer:
    return _wasmtime_module_validate(store, binary)  # type: ignore

_wasmtime_funcref_table_new = dll.wasmtime_funcref_table_new
_wasmtime_funcref_table_new.restype = POINTER(wasmtime_error_t)
_wasmtime_funcref_table_new.argtypes = [POINTER(wasm_store_t), POINTER(wasm_tabletype_t), POINTER(wasm_func_t), POINTER(POINTER(wasm_table_t))]
def wasmtime_funcref_table_new(store: Any, element_ty: Any, init: Any, table: Any) -> pointer:
    return _wasmtime_funcref_table_new(store, element_ty, init, table)  # type: ignore

_wasmtime_funcref_table_get = dll.wasmtime_funcref_table_get
_wasmtime_funcref_table_get.restype = c_bool
_wasmtime_funcref_table_get.argtypes = [POINTER(wasm_table_t), wasm_table_size_t, POINTER(POINTER(wasm_func_t))]
def wasmtime_funcref_table_get(table: Any, index: Any, func: Any) -> c_bool:
    return _wasmtime_funcref_table_get(table, index, func)  # type: ignore

_wasmtime_funcref_table_set = dll.wasmtime_funcref_table_set
_wasmtime_funcref_table_set.restype = POINTER(wasmtime_error_t)
_wasmtime_funcref_table_set.argtypes = [POINTER(wasm_table_t), wasm_table_size_t, POINTER(wasm_func_t)]
def wasmtime_funcref_table_set(table: Any, index: Any, value: Any) -> pointer:
    return _wasmtime_funcref_table_set(table, index, value)  # type: ignore

_wasmtime_funcref_table_grow = dll.wasmtime_funcref_table_grow
_wasmtime_funcref_table_grow.restype = POINTER(wasmtime_error_t)
_wasmtime_funcref_table_grow.argtypes = [POINTER(wasm_table_t), wasm_table_size_t, POINTER(wasm_func_t), POINTER(wasm_table_size_t)]
def wasmtime_funcref_table_grow(table: Any, delta: Any, init: Any, prev_size: Any) -> pointer:
    return _wasmtime_funcref_table_grow(table, delta, init, prev_size)  # type: ignore

_wasmtime_externref_new = dll.wasmtime_externref_new
_wasmtime_externref_new.restype = None
_wasmtime_externref_new.argtypes = [c_void_p, POINTER(wasm_val_t)]
def wasmtime_externref_new(data: Any, valp: Any) -> None:
    return _wasmtime_externref_new(data, valp)  # type: ignore

wasmtime_externref_finalizer_t = CFUNCTYPE(None, c_void_p)

_wasmtime_externref_new_with_finalizer = dll.wasmtime_externref_new_with_finalizer
_wasmtime_externref_new_with_finalizer.restype = None
_wasmtime_externref_new_with_finalizer.argtypes = [c_void_p, wasmtime_externref_finalizer_t, POINTER(wasm_val_t)]
def wasmtime_externref_new_with_finalizer(data: Any, finalizer: Any, valp: Any) -> None:
    return _wasmtime_externref_new_with_finalizer(data, finalizer, valp)  # type: ignore

_wasmtime_externref_data = dll.wasmtime_externref_data
_wasmtime_externref_data.restype = c_bool
_wasmtime_externref_data.argtypes = [POINTER(wasm_val_t), POINTER(c_void_p)]
def wasmtime_externref_data(val: Any, datap: Any) -> c_bool:
    return _wasmtime_externref_data(val, datap)  # type: ignore

_wasmtime_module_serialize = dll.wasmtime_module_serialize
_wasmtime_module_serialize.restype = POINTER(wasmtime_error_t)
_wasmtime_module_serialize.argtypes = [POINTER(wasm_module_t), POINTER(wasm_byte_vec_t)]
def wasmtime_module_serialize(module: Any, ret: Any) -> pointer:
    return _wasmtime_module_serialize(module, ret)  # type: ignore

_wasmtime_module_deserialize = dll.wasmtime_module_deserialize
_wasmtime_module_deserialize.restype = POINTER(wasmtime_error_t)
_wasmtime_module_deserialize.argtypes = [POINTER(wasm_engine_t), POINTER(wasm_byte_vec_t), POINTER(POINTER(wasm_module_t))]
def wasmtime_module_deserialize(engine: Any, serialized: Any, ret: Any) -> pointer:
    return _wasmtime_module_deserialize(engine, serialized, ret)  # type: ignore
