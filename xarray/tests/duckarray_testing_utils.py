import collections
import itertools
import re

import pytest

identifier_re = r"[a-zA-Z_][a-zA-Z0-9_]*"
variant_re = re.compile(
    rf"^(?P<name>{identifier_re}(?:(?:\.|::){identifier_re})*)(?:\[(?P<variant>[^]]+)\])?$"
)


def concat_mappings(mapping, *others, duplicates="error"):
    if not isinstance(mapping, dict):
        if others:
            raise ValueError("cannot pass both a iterable and multiple values")

        mapping, *others = mapping

    if duplicates == "error":
        all_keys = list(
            itertools.chain.from_iterable(m.keys() for m in [mapping] + others)
        )
        duplicates = {
            key: value
            for key, value in collections.Counter(all_keys).items()
            if value > 1
        }
        if duplicates:
            raise ValueError(f"duplicate keys found: {list(duplicates.keys())!r}")

    result = mapping.copy()
    for m in others:
        result.update(m)

    return result


def is_variant(k):
    return k.startswith("[") and k.endswith("]")


def process_spec(name, value):
    components, variant = parse_selector(name)

    if variant is not None and not isinstance(value, list):
        raise ValueError(f"invalid spec: {name} → {value}")
    elif isinstance(value, list):
        if variant is not None:
            value = {f"[{variant}]": value}

        yield components, value
    elif isinstance(value, dict) and all(is_variant(k) for k in value.keys()):
        yield components, value
    else:
        processed = itertools.chain.from_iterable(
            process_spec(name, value) for name, value in value.items()
        )

        yield from (
            (components + new_components, value) for new_components, value in processed
        )


def preprocess_marks(marks):
    flattened = itertools.chain.from_iterable(
        process_spec(name, value) for name, value in marks.items()
    )
    key = lambda x: x[0]
    grouped = itertools.groupby(sorted(flattened, key=key), key=key)
    result = [
        (components, concat_mappings(v for _, v in group))
        for components, group in grouped
    ]
    return result


def parse_selector(selector):
    match = variant_re.match(selector)
    if match is not None:
        groups = match.groupdict()
        variant = groups["variant"]
        name = groups["name"]
    else:
        raise ValueError(f"invalid test name: {name!r}")

    components = name.split(".")
    return components, variant


def get_test(module, components):
    *parent_names, name = components

    parent = module
    for parent_name in parent_names:
        parent = getattr(parent, parent_name)

    test = getattr(parent, name)

    return parent, test, name


def apply_marks(module, components, marks):
    parent, test, test_name = get_test(module, components)
    if isinstance(marks, list):
        # mark the whole test
        marked_test = test
        for mark in marks:
            marked_test = mark(marked_test)
    else:
        marked_test = pytest.mark.attach_marks(marks)(test)
    setattr(parent, test_name, marked_test)
