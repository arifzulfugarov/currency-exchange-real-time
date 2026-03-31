import streamlit as st
from converter import CurrencyConverter
from debounced_input import debounced_input

st.set_page_config(page_title="Currency Converter", page_icon="🌍")

st.title("🌍 Real-Time Currency Converter")

APP_ID = "1b6f163b75084ce4b7a6bf0eb4282839" # better than hardcoding

if "cnc" not in st.session_state:
    st.session_state.cnc = CurrencyConverter()
    try:
        with st.spinner("Fetching global currency data..."):
            st.session_state.cnc.fetch_rates(APP_ID)
    except Exception as e:
        st.error(f"Failed to fetch currency data: {e}")

cnc = st.session_state.cnc

if cnc.available_currencies:
    currencies = cnc.available_currencies

    if "amount_text" not in st.session_state:
        st.session_state.amount_text = "0"
    if "from_cur" not in st.session_state:
        st.session_state.from_cur = "EUR" if "EUR" in currencies else currencies[0]
    if "to_cur" not in st.session_state:
        st.session_state.to_cur = "HUF" if "HUF" in currencies else currencies[0]

    if st.session_state.from_cur not in currencies:
        st.session_state.from_cur = currencies[0]
    if st.session_state.to_cur not in currencies:
        st.session_state.to_cur = currencies[0]

    advanced_mode = st.toggle(
        "Advanced input mode",
        help="Updates the conversion 1 second after typing stops.",
    )

    if advanced_mode:
        amount_text = debounced_input(
            "Amount to convert",
            value=st.session_state.amount_text,
            debounce_ms=1000,
            key="amount_debounced",
        )
    else:
        amount_text = st.text_input(
            "Amount to convert",
            value=st.session_state.amount_text,
            key="amount_basic",
        )

    st.session_state.amount_text = amount_text

    from_col, swap_col, to_col = st.columns([1, 0.35, 1])

    with from_col:
        from_cur = st.selectbox(
            "1. Convert From",
            currencies,
            index=currencies.index(st.session_state.from_cur),
            key="from_cur",
        )

    with swap_col:
        st.write("")
        st.write("")
        if st.button("Reverse", use_container_width=True):
            st.session_state.from_cur, st.session_state.to_cur = (
                st.session_state.to_cur,
                st.session_state.from_cur,
            )
            st.rerun()

    with to_col:
        to_cur = st.selectbox(
            "2. Convert To",
            currencies,
            index=currencies.index(st.session_state.to_cur),
            key="to_cur",
        )

    try:
        amount = float(amount_text.strip()) if amount_text.strip() else 0.0

        result = cnc.convert(amount, from_cur, to_cur, save_to_history=False)
        rate = cnc.convert(1, from_cur, to_cur, save_to_history=False)

        st.metric(
            label=f"{amount:.2f} {from_cur}",
            value=f"{result:.2f} {to_cur}"
        )

        st.caption(f"1 {from_cur} = {rate:.4f} {to_cur}")

    except ValueError:
        st.warning("Please enter a valid number.")
    except Exception as e:
        st.error(f"Conversion failed: {e}")
else:
    st.error("Could not load currencies. Check your API key.")
