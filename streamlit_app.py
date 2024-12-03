import streamlit as st

# Initialize an empty order list in session state
if 'order' not in st.session_state:
    st.session_state.order = []

# Set up the sidebar for navigation
st.sidebar.title("McDonald's Menu")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# Display the selected category
st.title(selected_category)

# Display the items in the selected category
for item in menu_items[selected_category]:
    if st.button(f"Add {item} to Order"):
        st.session_state.order.append(item)
        st.success(f"{item} has been added to your order.")

# Show the current order
st.sidebar.header("Your Order")
if st.session_state.order:
    for ordered_item in st.session_state.order:
        st.sidebar.write(ordered_item)
else:
    st.sidebar.write("Your order is empty.")
