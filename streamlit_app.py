import streamlit as st

# Define the menu items
menu_items = {
    "Burgers": ["Big Mac", "Quarter Pounder", "McChicken"],
    "Drinks": ["Coca-Cola", "Sprite", "Iced Tea"],
    "Desserts": ["Apple Pie", "Sundae", "McFlurry"]
}

# Initialize session state for order
if 'order' not in st.session_state:
    st.session_state.order = {}

# Function to add item to the order
def add_to_order(item):
    if item in st.session_state.order:
        st.session_state.order[item] += 1
    else:
        st.session_state.order[item] = 1

# Function to remove item from the order
def decrement_or_remove_item(item):
    if item in st.session_state.order:
        if st.session_state.order[item] > 1:
            st.session_state.order[item] -= 1
        else:
            del st.session_state.order[item]

# Sidebar for navigation
st.sidebar.title("McDonald's Menu")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# Main menu display
st.title(f"Menu - {selected_category}")
for item in menu_items[selected_category]:
    col1, col2 = st.columns([4, 1])  # Layout for item and button
    col1.write(item)
    if col2.button(f"Add", key=f"add_{item}"):
        add_to_order(item)

# Sidebar order summary
st.sidebar.header("Your Order")
if st.session_state.order:
    for item, quantity in list(st.session_state.order.items()):
        col1, col2, col3 = st.sidebar.columns([2, 1, 1])
        col1.write(f"{item} ({quantity})")
        if col2.button("+", key=f"inc_{item}"):
            add_to_order(item)
        if col3.button("-", key=f"dec_{item}"):
            decrement_or_remove_item(item)
else:
    st.sidebar.write("Your order is empty.")
