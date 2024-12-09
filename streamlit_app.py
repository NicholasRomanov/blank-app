import streamlit as st
import os

# Define the folder containing the images
img_folder = os.path.join(os.getcwd(), "Img")

# Banner setup: Define the path to the banner image
banner_path = os.path.join(img_folder, "BurgerBanner.jpg")

# Display the banner at the top
if os.path.exists(banner_path):  # Check if the banner image exists
    st.image(banner_path, use_container_width=True)
else:
    st.error("Banner image not found!")

# Define the menu items with corresponding image filenames
menu_items = {
    "Burgers": {
        "Classic Burger": "Burger.png",
        "Cheese Burger": "CheeseBurger.png",
        "Chicken Burger": "ChickenBurger.png",
        "Double Cheese Burger": "DoubleCheese.png",
        "MEGA BURGER": "MEGABurger.png"
    },
    "Drinks": {
        "Coca-Cola": "CocaCola.png",
        "Sprite": "Sprite.png",
        "Lemon Tea": "IcedTea.png",
        "Milo": "Milo.png",
        "Aer putih": "Aer.png"
    },
    "Snacks": {
        "Kebab": "kebab.png",
        "Nugget": "Nugget.png",
        "Nugget (L)": "LNugget.png",
        "Salad": "salad.png",
        "Chicken Wings": "Wing.png"
    }
}

# Initialize an empty order dictionary in session state
if 'order' not in st.session_state:
    st.session_state.order = {}

# Set up the sidebar for navigation
st.sidebar.title("McDonald's Menu")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# Display the selected category
st.title(selected_category)

# Display the items in the selected category with images
for item, image_file in menu_items[selected_category].items():
    # Construct the full image path
    image_path = os.path.join(img_folder, image_file)
    col1, col2 = st.columns([1, 3])  # Create columns for layout
    with col1:
        if os.path.exists(image_path):  # Check if the image exists
            st.image(image_path, width=100)  # Display the item image
        else:
            st.error(f"Image for {item} not found!")
    with col2:
        st.write(f"**{item}**")
        if st.button(f"Add {item} to Order", key=f"add_{item}"):
            st.session_state.order[item] = st.session_state.order.get(item, 0) + 1
            st.success(f"{item} has been added to your order!")

# Show the current order
st.sidebar.header("Your Order")
if st.session_state.order:
    items_to_remove = []  # Temporary list to track items to remove
    for ordered_item, quantity in st.session_state.order.items():
        col1, col2 = st.sidebar.columns([2, 1])
        col1.write(f"{ordered_item} {quantity}x")
        if col2.button(f"Remove {ordered_item}", key=f"remove_{ordered_item}"):
            items_to_remove.append(ordered_item)  # Mark the item for removal

    # Remove the marked items from the order
    for item in items_to_remove:
        del st.session_state.order[item]

    # Display a message if the order becomes empty
    if not st.session_state.order:
        st.sidebar.write("Your cart is now empty.")
else:
    st.sidebar.write("Your cart is empty. Start adding items!")
