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

# Set up the sidebar for navigation
st.sidebar.title("McDonald's Menu")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# Display the selected category
st.title(selected_category)

# Display the items in the selected category
for item in menu_items[selected_category]:
    if st.button(f"Add {item} to Order"):
        # Increment the count of the item in the order
        if item in st.session_state.order:
            st.session_state.order[item] += 1
        else:
            st.session_state.order[item] = 1
        st.success(f"{item} has been added to your order.")

# Show the current order
st.sidebar.header("Your Order")
if st.session_state.order:
    for ordered_item, quantity in st.session_state.order.items():
        col1, col2 = st.sidebar.columns([2, 1])  # Create two columns in the sidebar
        col1.write(f"{ordered_item} {quantity}x")  # Display the item and quantity
        if col2.button(f"Remove {ordered_item}"):  # Button to remove the item
            del st.session_state.order[ordered_item]  # Remove the item from the order
            st.success(f"{ordered_item} has been removed from your order.")
else:
    st.sidebar.write("Your order is empty.")
