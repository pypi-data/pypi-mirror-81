"""This modules contains utilities to convert arbitrary type into JSON Class
field types object.
"""
from __future__ import annotations
from typing import (Any, TypeVar, Optional, Union, List, Dict, get_args,
                    get_origin, cast, TYPE_CHECKING)
from datetime import date, datetime
from re import match, split
from .class_graph import class_graph_map
if TYPE_CHECKING:
    from .types import Types
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


def str_to_types(argtype: str,
                 graph_sibling: type[T] = None,
                 optional: bool = False) -> Types:
    """Convert user specified string type to Types object."""
    from .types import types
    from .json_object import JSONObject
    if argtype == 'str':
        return types.str if optional else types.str.required
    elif argtype == 'int':
        return types.int if optional else types.int.required
    elif argtype == 'float':
        return types.float if optional else types.float.required
    elif argtype == 'bool':
        return types.bool if optional else types.bool.required
    elif argtype == 'date':
        return types.date if optional else types.date.required
    elif argtype == 'datetime':
        return types.datetime if optional else types.datetime.required
    elif argtype.startswith('Union['):
        match_data = match('Union\\[(.*)\\]', argtype)
        assert match_data is not None
        all_item_types = match_data.group(1)
        types_to_build_union = split(", *", all_item_types)  # TODO: Dict is not supported this way
        results = []
        for t in types_to_build_union:
            results.append(str_to_types(t, graph_sibling, True))
        oneoftype = types.oneoftype(results)
        return oneoftype if optional else oneoftype.required
    elif argtype.startswith('Optional['):
        match_data = match('Optional\\[(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        return str_to_types(item_type, graph_sibling, True)
    elif match('[Ll]ist\\[', argtype):
        match_data = match('[Ll]ist\\[(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        list_type = types.listof(str_to_types(item_type, graph_sibling))
        return list_type if optional else list_type.required
    elif match('[Dd]ict\\[', argtype):
        match_data = match('[Dd]ict\\[.+, ?(.*)\\]', argtype)
        assert match_data is not None
        item_type = match_data.group(1)
        dict_type = types.dictof(str_to_types(item_type, graph_sibling))
        return dict_type if optional else dict_type.required
    else:
        graph_name = cast(type[JSONObject], graph_sibling).config.graph
        cls = class_graph_map.graph(graph_name).get(argtype)
        instance_type = types.instanceof(cls)
        return instance_type if optional else instance_type.required


def to_types(argtype: Any,
             graph_sibling: Optional[type[T]] = None,
             optional: bool = False) -> Types:
    """Convert arbitrary user specified type to Types object."""
    from .json_object import JSONObject
    from .types import types
    if isinstance(argtype, str):
        return str_to_types(argtype, graph_sibling)
    elif argtype is str:
        return types.str if optional else types.str.required
    elif argtype is int:
        return types.int if optional else types.int.required
    elif argtype is float:
        return types.float if optional else types.float.required
    elif argtype is bool:
        return types.bool if optional else types.bool.required
    elif argtype is date:
        return types.date if optional else types.date.required
    elif argtype is datetime:
        return types.datetime if optional else types.datetime.required
    elif get_origin(argtype) == Union:
        required: bool = True
        types_to_build_union: List[Any] = []
        args = get_args(argtype)
        for arg in args:
            if type(None) == arg:
                required = False
            else:
                types_to_build_union.append(arg)
        if len(types_to_build_union) == 1:
            return to_types(types_to_build_union[0],
                            graph_sibling,
                            not required)
        else:
            results = []
            for t in types_to_build_union:
                results.append(to_types(t, graph_sibling, True))
            oneoftype = types.oneoftype(results)
            return oneoftype if not required else oneoftype.required
    elif get_origin(argtype) is list:
        list_type = types.listof(get_args(argtype)[0])
        return list_type if optional else list_type.required
    elif get_origin(argtype) is dict:
        dict_type = types.dictof(get_args(argtype)[1])
        return dict_type if optional else dict_type.required
    elif issubclass(argtype, JSONObject):
        instance_type = types.instanceof(argtype)
        return instance_type if optional else instance_type.required
    elif issubclass(argtype, dict):
        anno_dict: Dict[str, Any] = argtype.__annotations__
        item_types: Dict[str, Types] = {}
        for k, t in anno_dict.items():
            item_types[k] = to_types(t, graph_sibling)
        shape_types = types.shape(item_types)
        return shape_types if optional else shape_types.required
    else:
        raise ValueError(f'{argtype} is not a valid JSON Class type.')


def resolve_types(arbitrary_type: Any, graph_sibling: type[T] = None) -> Types:
    """Get desired JSON Class field types object from arbitrary types that
    users can specify.

    If the provided `arbitrary_type` is a `Types` object, itself is returned.
    Otherwise, a synthesized default types is returned.

    Returns:
        Types: A Types object dedicated for this provided type expression.
    """
    from .types import Types
    if isinstance(arbitrary_type, Types):
        return arbitrary_type
    return to_types(arbitrary_type, graph_sibling)
