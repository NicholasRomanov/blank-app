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

# Sidebar for menu navigation
st.sidebar.title("McDonald's Menu")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# Display the selected category
st.title(selected_category)

# Display items and add buttons
for item in menu_items[selected_category]:
    col1, col2 = st.columns([3, 1])
    col1.write(item)
    if col2.button(f"Add {item}", key=f"add_{item}"):
        add_to_order(item)

# Sidebar order display with quantity controls
st.sidebar.header("Your Order")
if st.session_state.order:
    for ordered_item, quantity in list(st.session_state.order.items()):
        col1, col2, col3 = st.sidebar.columns([2, 1, 1])
        col1.write(f"{ordered_item}: {quantity}x")
        if col2.button("+", key=f"inc_{ordered_item}"):
            add_to_order(ordered_item)
        if col3.button("-", key=f"dec_{ordered_item}"):
            remove_from_order(ordered_item)
else:
    st.sidebar.write("Your order is empty.")
