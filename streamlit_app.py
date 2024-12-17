import streamlit as st
import pandas as pd
import os
from openpyxl import load_workbook
from datetime import datetime

# Define the menu items (nested dictionaries with item names and image paths)
menu_items = {
    "Burgers": {
        "Classic Burger": "images/Burger.png",
        "Cheese Burger": "images/CheeseBurger.png",
        "Chicken Burger": "images/ChickenBurger.png",
        "Double Cheese Burger": "images/DoubleCheese.png",
        "MEGA BURGER": "images/MEGABurger.png"
    },
    "Drinks": {
        "Coca-Cola": "images/CocaCola.png",
        "Sprite": "images/Sprite.png",
        "Lemon Tea": "images/LemonTea.png",
        "Milo": "images/Milo.png",
        "Aer putih": "images/Aer.png"
    },
    "Snacks": {
        "Kebab": "images/Kebab.png",
        "Nugget": "images/Nugget.png",
        "Nugget (L)": "images/Lnugget.png",
        "Salad": "images/Salad.png",
        "Chicken Wings": "images/Wing.png"
    }
}

# Initialize order in session state
if 'order' not in st.session_state:
    st.session_state.order = {}

# Banner
st.image("images/Banner.jpg", use_container_width=True)
st.title("Welcome to McDonald's App")

# Sidebar for Navigation
st.sidebar.title("Menu Categories")
selected_category = st.sidebar.radio("Choose a category:", list(menu_items.keys()))

# Display selected category items with images and buttons
st.header(f"{selected_category}")  # Header for the selected category
for item, img_path in menu_items[selected_category].items():
    col1, col2 = st.columns([1, 3])  # Two columns: image and text/button
    
    with col1:
        st.image(img_path, width=100)  # Display the item's image
    
    with col2:
        st.write(f"**{item}**")  # Display the item name in bold
        if st.button(f"Add {item}", key=f"add-{item}"):  # Unique key for each button
            if item in st.session_state.order:
                st.session_state.order[item] += 1  # Increment quantity
            else:
                st.session_state.order[item] = 1  # Add item to order
            st.success(f"{item} has been added to your order.")

# Sidebar: Display current order and removal buttons
st.sidebar.header("Your Order")
if st.session_state.order:
    for ordered_item, quantity in list(st.session_state.order.items()):
        col1, col2 = st.sidebar.columns([2, 1])  # Two columns for displaying and removing
        col1.write(f"{ordered_item} x{quantity}")  # Display item and quantity
        if col2.button("Remove", key=f"remove-{ordered_item}"):  # Unique key for removal
            del st.session_state.order[ordered_item]  # Remove the item
            st.experimental_rerun()  # Rerun app to reflect changes
else:
    st.sidebar.write("Your order is empty.")

# Button to finalize and export order to Excel
if st.sidebar.button("Place Order"):
    if st.session_state.order:
        # Prepare data for Excel
        order_data = [{"Item": item, "Quantity": quantity} for item, quantity in st.session_state.order.items()]
        df = pd.DataFrame(order_data)
        
        # Add a timestamped row to track each group order
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df["Order Time"] = current_time
        
        # Excel file path
        excel_file = "Order.xlsx"
        
        # Check if the file exists and update it, or create a new one
        if os.path.exists(excel_file):
            with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                workbook = load_workbook(excel_file)
                sheet = workbook.active
                start_row = sheet.max_row + 2  # Leave space between previous and new order
                df.to_excel(writer, index=False, header=False, startrow=start_row)
        else:
            df.to_excel(excel_file, index=False, engine="openpyxl")
        
        st.sidebar.success("Your order has been placed and saved to Excel!")
        st.session_state.order = {}  # Clear the order
        st.experimental_rerun()
    else:
        st.sidebar.warning("Your order is empty. Add some items before placing the order!")
