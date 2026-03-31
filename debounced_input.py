from pathlib import Path
from typing import Optional

import streamlit.components.v1 as components


_COMPONENT_DIR = Path(__file__).parent / "components" / "debounced_input"

_debounced_input_component = components.declare_component(
    "debounced_input",
    path=str(_COMPONENT_DIR),
)


def debounced_input(
    label: str,
    value: str = "",
    debounce_ms: int = 1000,
    key: Optional[str] = None,
) -> str:
    return _debounced_input_component(
        label=label,
        value=value,
        debounce_ms=debounce_ms,
        key=key,
        default=value,
    )
