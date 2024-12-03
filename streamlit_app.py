import streamlit as st

# Define the menu items
menu_items = {
    "Burgers": ["Big Mac", "Quarter Pounder", "McChicken"],
    "Drinks": ["Coca-Cola", "Sprite", "Iced Tea"],
    "Desserts": ["Apple Pie", "Sundae", "McFlurry"]
}

# Set up the sidebar for navigation
st.sidebar.title("Menu Mekdi")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# Display the selected category
st.title(selected_category)

# Display the items in the selected category
for item in menu_items[selected_category]:
    quantity = st.number_input(f"Select quantity for {item}", min_value=0)
    if st.button(f"Order {item}"):
        st.success(f"You have ordered {quantity} {item}(s).")
