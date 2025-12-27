import re


def normalize_label(label: str) -> str:
    if not label:
        return ""
    label = label.lower().strip()
    label = re.sub(r"[^\w\s]", "", label)
    label = re.sub(r"\s+", "_", label)
    return label
