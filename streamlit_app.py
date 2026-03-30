import streamlit as st
from converter import CurrencyConverter

st.title("🌍 Real-Time Currency Converter")

# Initialize our class
if 'cnc' not in st.session_state:
    st.session_state.cnc = CurrencyConverter()

# 1. Setup Base Currency with a scrolling list
# We provide a few common ones so the user can scroll right away!
COMMON_CURRENCIES = ["EUR", "USD", "GBP", "JPY", "CAD", "AUD", "CHF", "HUF"]

base = st.selectbox("1. Select Base Currency", COMMON_CURRENCIES)

if st.button("Fetch Latest Rates"):
    st.session_state.cnc.fetch_rates(base)
    st.success(f"Rates loaded for {base}!")

# 2. Conversion Inputs
amount = st.number_input("Amount to convert", min_value=0.0, value=1.0, step=1.0)

# Check if we have currencies loaded
if st.session_state.cnc.available_currencies:
    # ADDED: key="selectbox_target"
    to_cur = st.selectbox(
        "3. Select Target Currency", 
        st.session_state.cnc.available_currencies,
        key="target_select" 
    )
else:
    # ADDED: key="text_target"
    to_cur = st.text_input(
        "Target Currency (e.g. USD)", 
        "USD", 
        key="target_text"
    ).upper()

if st.button("Convert Now"):
    result = st.session_state.cnc.convert(amount, base, to_cur)
    st.metric(label="Result", value=f"{result:.2f} {to_cur}")

# --- SCROLLING LOGIC END ---

# 4. History Sidebar
st.sidebar.header("Transaction History")
for item in reversed(st.session_state.cnc.get_history()):
    st.sidebar.write(item)
