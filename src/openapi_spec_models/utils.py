from collections import abc, defaultdict, deque
from inspect import isclass
from typing import (
    AbstractSet,
    Any,
    DefaultDict,
    Deque,
    Dict,
    FrozenSet,
    List,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
    Set,
    Tuple,
    get_origin,
)

from typing_extensions import (
    Annotated,
    NotRequired,
    ReadOnly,
    Required,
    get_args,
    TypeGuard
)

wrapper_type_set = {Annotated, Required, NotRequired, ReadOnly}

instantiable_type_mapping = {
    AbstractSet: set,
    DefaultDict: defaultdict,
    Deque: deque,
    Dict: dict,
    FrozenSet: frozenset,
    List: list,
    Mapping: dict,
    MutableMapping: dict,
    MutableSequence: list,
    MutableSet: set,
    Sequence: list,
    Set: set,
    Tuple: tuple,
    abc.Mapping: dict,
    abc.MutableMapping: dict,
    abc.MutableSequence: list,
    abc.MutableSet: set,
    abc.Sequence: list,
    abc.Set: set,
    defaultdict: defaultdict,
    deque: deque,
    dict: dict,
    frozenset: frozenset,
    list: list,
    set: set,
    tuple: tuple,
}


def is_non_string_sequence(annotation: Any) -> TypeGuard[Sequence[Any]]:
    """Given a type annotation determine if the annotation is a sequence.

    Args:
    annotation: A type.

    Returns:
        A typeguard determining whether the type can be cast as :class:`Sequence <typing.Sequence>` that is not a string.
    """
    origin = get_origin_or_inner_type(annotation)
    if not origin and not isclass(annotation):
        return False
    try:
        return not issubclass(origin or annotation, (str, bytes)) and issubclass(
            origin or annotation,
            (  # type: ignore[arg-type]
                Tuple,
                List,
                Set,
                FrozenSet,
                Deque,
                Sequence,
                list,
                tuple,
                deque,
                set,
                frozenset,
            ),
        )
    except TypeError:  # pragma: no cover
        return False


def get_origin_or_inner_type(annotation: Any) -> Any:
    """Get origin or unwrap it. Returns None for non-generic types.

    Args:
        annotation: A type annotation.

        Returns:
                Any type.
    """
    origin = get_origin(annotation)
    if origin in wrapper_type_set:
        inner, _, _ = unwrap_annotation(annotation)
        # we need to recursively call here 'get_origin_or_inner_type' because we might be dealing
        # with a generic type alias e.g. Annotated[dict[str, list[int]]
        origin = get_origin_or_inner_type(inner)
        return instantiable_type_mapping.get(origin, origin)


def unwrap_annotation(annotation: Any) -> tuple[Any, tuple[Any, ...], set[Any]]:
    """Remove "wrapper" annotation types.

    Such as ``Annotated``, ``ReadOnly``, ``Required``, and ``NotRequired``.

    Note:
    ``annotation`` should have been retrieved from :func:`get_type_hints()` with ``include_extras=True``. This
    ensures that any nested ``Annotated`` types are flattened according to the PEP 593 specification.

    Args:
        annotation: A type annotation.

    Returns:
        A tuple of the unwrapped annotation and any ``Annotated`` metadata, and a set of any wrapper types encountered.
    """
    origin = get_origin(annotation)
    wrappers = set()
    metadata = []
    while origin in wrapper_type_set:
        wrappers.add(origin)
        annotation, *meta = get_args(annotation)
        metadata.extend(meta)
        origin = get_origin(annotation)
        return annotation, tuple(metadata), wrappers
