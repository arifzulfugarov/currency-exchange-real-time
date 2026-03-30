import streamlit as st
from converter import CurrencyConverter

st.title("🌍 Real-Time Currency Converter")

# Initialize our class
# Initialize our class AND fetch initial data for the full list
if 'cnc' not in st.session_state:
    st.session_state.cnc = CurrencyConverter()
    # Fetch once automatically so the dropdowns have all countries immediately
    st.session_state.cnc.fetch_rates("EUR")

st.title("🌍 Real-Time Currency Converter")

# 1. Setup Base Currency with THE FULL LIST
# Now we use the list we just fetched automatically!
base = st.selectbox(
    "1. Select Base Currency", 
    st.session_state.cnc.available_currencies,
    index=st.session_state.cnc.available_currencies.index("EUR") # Default to EUR
)


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
    # 1. Fetch the LATEST rates for the base the user JUST picked
    with st.spinner(f"Fetching latest rates for {base}..."):
        st.session_state.cnc.fetch_rates(base)
    
    # 2. Now perform the math with the correct board
    result = st.session_state.cnc.convert(amount, base, to_cur)
    
    # 3. Display and celebrate
    st.metric(label=f"Result ({to_cur})", value=f"{result:.2f}")
    st.balloons()

# --- SCROLLING LOGIC END ---

# 4. History Sidebar
st.sidebar.header("Transaction History")
for item in reversed(st.session_state.cnc.get_history()):
    st.sidebar.write(item)
