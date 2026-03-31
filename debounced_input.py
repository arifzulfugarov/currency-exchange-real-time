import streamlit as st


_DEBOUNCED_INPUT = st.components.v2.component(
    "debounced_number_input",
    html="""
    <label class="debounced-input__label" for="debounced-input"></label>
    <input id="debounced-input" class="debounced-input__field" type="number" step="any" />
    """,
    css="""
    :host {
        display: block;
    }

    .debounced-input__label {
        display: block;
        margin-bottom: 0.35rem;
        font-family: var(--st-font);
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--st-text-color);
    }

    .debounced-input__field {
        width: 100%;
        box-sizing: border-box;
        min-height: 2.5rem;
        padding: 0.5rem 0.75rem;
        border: 1px solid var(--st-border-color);
        border-radius: 0.5rem;
        background: var(--st-bg-color);
        color: var(--st-text-color);
        font-family: var(--st-font);
        font-size: 1rem;
        outline: none;
    }

    .debounced-input__field:focus {
        border-color: var(--st-primary-color);
        box-shadow: 0 0 0 1px var(--st-primary-color);
    }
    """,
    js="""
    export default function(component) {
        const { data, parentElement, setStateValue } = component;
        const input = parentElement.querySelector("#debounced-input");
        const label = parentElement.querySelector(".debounced-input__label");
        const debounceMs = data?.debounce_ms ?? 1000;
        const nextValue = data?.value ?? "";

        label.textContent = data?.label ?? "";

        if (input.value !== String(nextValue)) {
            input.value = nextValue;
        }

        if (!input.dataset.bound) {
            let timeoutId = null;

            input.addEventListener("input", (event) => {
                const typedValue = event.target.value;
                window.clearTimeout(timeoutId);
                timeoutId = window.setTimeout(() => {
                    setStateValue("value", typedValue);
                }, debounceMs);
            });

            input.dataset.bound = "true";
        }
    }
    """,
)


def debounced_input(label, value="0", debounce_ms=1000, key=None):
    if key is not None:
        component_state = st.session_state.get(key, {})
        current_value = component_state.get("value", value)
    else:
        current_value = value

    result = _DEBOUNCED_INPUT(
        data={
            "label": label,
            "value": current_value,
            "debounce_ms": debounce_ms,
        },
        default={"value": current_value},
        key=key,
        on_value_change=lambda: None,
    )
    return result.value
