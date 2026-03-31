import streamlit as st
from converter import CurrencyConverter

st.title("🌍 Real-Time Currency Converter")

# 1. Initialize our class with your App ID
# Get your ID from https://openexchangerates.org
amount = st.number_input("Amount to convert", min_value=0.0, value=1.0)
APP_ID = "1b6f163b75084ce4b7a6bf0eb4282839" 

if 'cnc' not in st.session_state:
    st.session_state.cnc = CurrencyConverter()
    # Fetch all rates once (relative to USD)
    with st.spinner("Fetching global currency data..."):
        st.session_state.cnc.fetch_rates(APP_ID)

# 2. Selectbox for "From" and "To"
# Since we have ALL rates (AZN, KZT, etc.) in the list, we just pick from them
if st.session_state.cnc.available_currencies:
    from_cur = st.selectbox(
        "1. Convert From", 
        st.session_state.cnc.available_currencies,
        index=st.session_state.cnc.available_currencies.index("USD")
    )
    
    to_cur = st.selectbox(
        "2. Convert To", 
        st.session_state.cnc.available_currencies,
        index=st.session_state.cnc.available_currencies.index("AZN")
    )
else:
    st.error("Could not load currencies. Check your API Key.")

# 3. Conversion Inputs

if st.button("Convert Now"):
    # We don't need to fetch_rates again here because we already have them all!
    # The math happens inside the converter class
    result = st.session_state.cnc.convert(amount, from_cur, to_cur)
    
    if result > 0:
        st.metric(label=f"Result ({to_cur})", value=f"{result:.2f}")
        st.balloons()
    else:
        st.error("Conversion failed. Please try again.")

# 4. History Sidebar
st.sidebar.header("Transaction History")
for item in reversed(st.session_state.cnc.get_history()):
    st.sidebar.write(item)
