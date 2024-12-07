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

# Show the current order with quantity adjustments
st.sidebar.header("Your Order")
if st.session_state.order:
    for ordered_item, quantity in list(st.session_state.order.items()):
        col1, col2, col3 = st.sidebar.columns([2, 1, 1])  # Create three columns in the sidebar
        col1.write(f"{ordered_item} {quantity}x")  # Display the item and quantity
        if col2.button(f"+ {ordered_item}"):  # Increment button
            st.session_state.order[ordered_item] += 1
            st.experimental_rerun()  # Refresh the app to reflect the changes
        if col3.button(f"- {ordered_item}"):  # Decrement button
            if st.session_state.order[ordered_item] > 1:
                st.session_state.order[ordered_item] -= 1
            else:
                del st.session_state.order[ordered_item]  # Remove the item if quantity becomes 0
            st.experimental_rerun()  # Refresh the app to reflect the changes
else:
    st.sidebar.write("Your order is empty.")
