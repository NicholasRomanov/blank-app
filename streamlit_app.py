import streamlit as st
import os
import pandas as pd
from openpyxl import Workbook
from datetime import datetime

st.title("Selamat datang Di Burger Hawktuah")

# ini buat folder gambar
img_folder = os.path.join(os.getcwd(), "Img")

# folder excel
excel_file_path = os.path.join(os.getcwd(), "Order.xlsx")

# ini gambar banner
banner_path = os.path.join(img_folder, "BurgerBanner.jpg")

# letak banner
if os.path.exists(banner_path):  # Check if the banner image exists
    st.image(banner_path, use_container_width=True)
else:
    st.error("Banner image not found!")

# isi menu ama gambarnya
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
        "Aer putih": "Aer.png"
    },
    "Snacks": {
        "Kebab": "Kebab.png",
        "Nugget": "Nugget.png",
        "Nugget (L)": "Lnugget.png",
        "Salad": "Salad.png",
        "Chicken Wings": "Wing.png"
    }
}

# ini tempat order kosong
if 'order' not in st.session_state:
    st.session_state.order = {}

# navigasi sidebar
st.sidebar.title("Menu List")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# category barang
st.title(selected_category)

# ni ngedisplay nama file ama gabar nya
for item, image_file in menu_items[selected_category].items():
    # ini folder path gambar menu
    image_path = os.path.join(img_folder, image_file)
    col1, col2 = st.columns([1, 3])  # layoutnya
    with col1:
        if os.path.exists(image_path):  # check gambar
            st.image(image_path, width=100)  # display
        else:
            st.error(f"Image for {item} not found!")
    with col2:
        st.write(f"**{item}**")
        if st.button(f"Add {item} to Order", key=f"add_{item}"):
            st.session_state.order[item] = st.session_state.order.get(item, 0) + 1
            st.success(f"{item} has been added to your order!")

# ngasih liat order di sidebar
st.sidebar.header("Your Order")
if st.session_state.order:
    items_to_remove = []  # list sementara buat diapus
    for ordered_item, quantity in st.session_state.order.items():
        col1, col2 = st.sidebar.columns([2, 1])
        col1.write(f"{ordered_item} {quantity}x")
        if col2.button(f"Remove", key=f"remove"):
            items_to_remove.append(ordered_item)  # ini buat remove item

    # buat ngapus order
    for item in items_to_remove:
        del st.session_state.order[item]

    # kalo koson ini keluar
    if not st.session_state.order:
        st.sidebar.write("Your cart is now empty.")
else:
    st.sidebar.write("Your cart is empty. Start adding items!")
