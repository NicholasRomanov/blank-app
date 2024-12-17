import streamlit as st
import os
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

# --- Title ---
st.title("Selamat Datang di DELIS BURGER")

# --- Define Image and Excel Directories ---
img_folder = os.path.join(os.getcwd(), "Img")  # Folder for images
excel_file_path = os.path.join(os.getcwd(), "Order.xlsx")  # Excel file for orders

# --- Banner Image ---
banner_path = os.path.join(img_folder, "Banner.jpg")
if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)
else:
    st.error("Banner image not found!")

# --- Menu Items and Images ---
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
        "Lemon Tea": "LemonTea.png",
        "Milo": "Milo.png",
        "Aer Putih": "Aer.png"
    },
    "Snacks": {
        "Kebab": "Kebab.png",
        "Nugget": "Nugget.png",
        "Nugget (L)": "Lnugget.png",
        "Salad": "Salad.png",
        "Chicken Wings": "Wing.png"
    }
}

# --- Initialize Order State ---
if 'order' not in st.session_state:
    st.session_state.order = {}

# --- Sidebar Navigation ---
st.sidebar.title("Menu List")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# --- Display Menu Category ---
st.title(selected_category)
for item, image_file in menu_items[selected_category].items():
    # Image path for each menu item
    image_path = os.path.join(img_folder, image_file)
    
    # Layout with columns
    col1, col2 = st.columns([1, 3])
    with col1:
        if os.path.exists(image_path):
            st.image(image_path, width=100)
        else:
            st.error(f"Image for {item} not found!")
    with col2:
        st.write(f"**{item}**")
        if st.button(f"Add {item} to Order", key=f"add_{item}"):
            st.session_state.order[item] = st.session_state.order.get(item, 0) + 1
            st.success(f"{item} has been added to your order!")

# --- Display Cart in Sidebar ---
st.sidebar.header("Your Order")
if st.session_state.order:
    for ordered_item, quantity in st.session_state.order.items():
        col1, col2 = st.sidebar.columns([2, 1])
        col1.write(f"{ordered_item} {quantity}x")
        
        # Button to remove an item
        if col2.button("Remove", key=f"remove_{ordered_item}"):
            del st.session_state.order[ordered_item]
            st.experimental_rerun()

    # Order button
    if st.sidebar.button("Place Order"):
        # Add order to Excel file
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_data = [{"Item": item, "Quantity": quantity, "Time": order_time} for item, quantity in st.session_state.order.items()]

        # Append to existing Excel file or create a new one
        if os.path.exists(excel_file_path):
            with pd.ExcelWriter(excel_file_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                pd.DataFrame(order_data).to_excel(writer, sheet_name="Orders", index=False, header=False, startrow=writer.sheets['Orders'].max_row)
        else:
            pd.DataFrame(order_data).to_excel(excel_file_path, sheet_name="Orders", index=False)

        # Clear the cart
        st.session_state.order = {}
        st.sidebar.success("Your order has been placed! Thank you!")

else:
    st.sidebar.write("Your cart is empty. Start adding items!")

# --- Footer ---
st.sidebar.write("---")
st.sidebar.write("Thank you for visiting DELIS BURGER!")
