import streamlit as st
from converter import CurrencyConverter

st.title("🌍 Real-Time Currency Converter")

# Initialize our class
if 'cnc' not in st.session_state:
    st.session_state.cnc = CurrencyConverter()

# 1. Setup Base Currency
base = st.text_input("Base Currency (e.g. EUR)", "EUR").upper()

if st.button("Fetch Latest Rates"):
    st.session_state.cnc.fetch_rates(base)
    st.success(f"Rates updated for {base}!")

options = st.session_state.cnc.available_currencies

# 2. Conversion Inputs
amount = st.number_input("Amount to convert", min_value=0.0, value=1.0)


if st.session_state.cnc.available_currencies:
    # Get the list only when we know it exists
    options = st.session_state.cnc.available_currencies
    to_cur = st.selectbox("Target Currency", options)
else:
    # Use the text input as a backup if they haven't fetched yet
    to_cur = st.text_input("Target Currency (e.g. USD)", "USD").upper()

# 3. Perform Conversion
if st.button("Convert"):
    result = st.session_state.cnc.convert(amount, base, to_cur)
    st.metric(label="Result", value=f"{result:.2f} {to_cur}")
    
# 4. History Sidebar
st.sidebar.header("Transaction History")
for item in st.session_state.cnc.get_history():
    st.sidebar.write(item)
