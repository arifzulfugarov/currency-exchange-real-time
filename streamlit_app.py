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

# --- This part only appears AFTER you click the button above ---
if st.session_state.cnc.available_currencies:
    amount = st.number_input("2. Amount to convert", min_value=0.01, value=1.0)

    # This is your second scrolling list (the one from the API)
    to_cur = st.selectbox("3. Select Target Currency", st.session_state.cnc.available_currencies)

    if st.button("Convert"):
        result = st.session_state.cnc.convert(amount, base, to_cur)
        st.metric(label="Result", value=f"{result:.2f} {to_cur}")


# --- SCROLLING LOGIC START ---
# Only show the conversion tools if we have fetched the list
if st.session_state.cnc.available_currencies:
    
    # 2. Conversion Inputs
    amount = st.number_input("2. Amount to convert", min_value=0.0, value=1.0)

    # This creates the scrolling dropdown you wanted
    to_cur = st.selectbox("3. Select Target Currency", st.session_state.cnc.available_currencies)

    # 3. Perform Conversion
    if st.button("Convert"):
        result = st.session_state.cnc.convert(amount, base, to_cur)
        st.metric(label="Result", value=f"{result:.2f} {to_cur}")
        
else:
    # This shows until they click the first button
    st.info("Please click 'Fetch Latest Rates' to see the available currencies list.")
# --- SCROLLING LOGIC END ---

# 4. History Sidebar
st.sidebar.header("Transaction History")
for item in reversed(st.session_state.cnc.get_history()):
    st.sidebar.write(item)
