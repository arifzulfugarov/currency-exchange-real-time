import streamlit as st
from converter import CurrencyConverter

st.set_page_config(page_title="Currency Converter", page_icon="🌍")

st.title("🌍 Real-Time Currency Converter")

# Use Streamlit secrets in real projects
APP_ID = "1b6f163b75084ce4b7a6bf0eb4282839"

# Initialize converter once
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

    from_default = currencies.index("USD") if "USD" in currencies else 0
    to_default = currencies.index("AZN") if "AZN" in currencies else 0

    amount = st.number_input(
        "Amount to convert",
        min_value=0.0,
        value=1.0,
        step=1.0
    )

    from_cur = st.selectbox(
        "1. Convert From",
        currencies,
        index=from_default
    )

    to_cur = st.selectbox(
        "2. Convert To",
        currencies,
        index=to_default
    )

    try:
        
        result = cnc.convert(amount, from_cur, to_cur, save_to_history=False)
        rate = cnc.convert(1, from_cur, to_cur, save_to_history=False)

        st.metric(
            label=f"{amount:.2f} {from_cur}",
            value=f"{result:.2f} {to_cur}"
        )

        st.caption(f"1 {from_cur} = {rate:.4f} {to_cur}")

    except Exception as e:
        st.error(f"Conversion failed: {e}")
else:
    st.error("Could not load currencies. Check your API key.")

# Sidebar history
st.sidebar.header("Transaction History")
for item in reversed(cnc.get_history()):
    st.sidebar.write(item)