import streamlit as st

# Define the menu items
menu_items = {
    "Burgers": ["Big Mac", "Quarter Pounder", "McChicken"],
    "Drinks": ["Coca-Cola", "Sprite", "Iced Tea"],
    "Desserts": ["Apple Pie", "Sundae", "McFlurry"]
}

# Initialize an empty order dictionary in session state
if 'order' not in st.session_state:
    st.session_state.order = {}

# Function to increment item quantity
def add_to_order(item):
    if item in st.session_state.order:
        st.session_state.order[item] += 1
    else:
        st.session_state.order[item] = 1

# Function to decrement item quantity
def remove_from_order(item):
    if item in st.session_state.order:
        if st.session_state.order[item] > 1:
            st.session_state.order[item] -= 1
        else:
            del st.session_state.order[item]

# Set up the sidebar for navigation
st.sidebar.title("McDonald's Menu")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# Display the selected category
st.title(selected_category)

# Display the it
