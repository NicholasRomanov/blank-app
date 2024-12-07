import streamlit as st

# Define the menu items
menu = {
    "Burgers": ["Big Mac", "Quarter Pounder", "McChicken"],
    "Drinks": ["Coca-Cola", "Sprite", "Iced Tea"],
    "Desserts": ["Apple Pie", "Sundae", "McFlurry"],
}

# Initialize session state for order management
if "order" not in st.session_state:
    st.session_state.order = {}

# Function to add an item to the order
def add_item(item):
    if item in st.session_state.order:
        st.session_state.order[item] += 1
    else:
        st.session_state.order[item] = 1

# Function to remove or decrement an item in the order
def remove_item(item):
    if item in st.session_state.order:
        if st.session_state.order[item] > 1:
            st.session_state.order[item] -= 1
        else:
            del st.session_state.order[item]

# Sidebar: Menu categories
st.sidebar.title("McDonald's Menu")
category = st.sidebar.radio("Select a category:", menu.keys())

# Main Area: Display items in the selected category
st.title(f"Menu - {category}")
for item in menu[category]:
    col1, col2 = st.columns([4, 1])
    col1.write(item)
    if col2.button("Add", key=f"add_{item}"):
        add_item(item)

# Sidebar: Order summary
st.sidebar.header("Your Order")
if st.session_state.order:
    for item, quantity in st.session_state.order.items():
        col1, col2, col3 = st.sidebar.columns([3, 1, 1])
        col1.write(f"{item} ({quantity})")
        if col2.button("+", key=f"inc_{item}"):
            add_item(item)
        if col3.button("-", key=f"dec_{item}"):
            remove_item(item)
else:
    st.sidebar.write("Your order is empty.")
