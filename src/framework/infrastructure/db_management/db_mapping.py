from typing import List


def map_from_to(
    original_object: object, from_attrs: List, to_attrs: List, ignores=[]
) -> dict:
    mapped = {t: getattr(original_object, f) for t, f in zip(to_attrs, from_attrs)}

    return mapped
