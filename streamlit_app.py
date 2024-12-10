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

# order kosong
if 'order' not in st.session_state:
    st.session_state.order = {}

# sidebar menu
st.sidebar.title("McDonald's Menu")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# kategori makanan jadi title
st.subheader(f"Category: {selected_category}")

# display makanan pake gambar
for item, image_file in menu_items[selected_category].items():
    # path gambar
    image_path = os.path.join(img_folder, image_file)
    col1, col2 = st.columns([1, 3])  #layout kolom
    with col1:
        if os.path.exists(image_path):  # cek gambar ada ga
            st.image(image_path, width=100)  # nampilin gambar
        else:
            st.error(f"Image for {item} not found!")
    with col2:
        st.write(f"**{item}**")
        if st.button(f"Add {item} to Order", key=f"add_{item}"):
            st.session_state.order[item] = st.session_state.order.get(item, 0) + 1
            st.success(f"{item} has been added to your order!")

# order di sidebar
st.sidebar.header("Your Order")
if st.session_state.order:
    st.sidebar.subheader("Current Items:")
    items_to_remove = []  # list buat apus order
    for ordered_item, quantity in st.session_state.order.items():
        col1, col2 = st.sidebar.columns([2, 1])
        col1.write(f"{ordered_item} {quantity}x")
        if col2.button(f"Remove {ordered_item}", key=f"remove_{ordered_item}"):
            items_to_remove.append(ordered_item)  # buat marking apus order

    # yang kena marking diapus
    for item in items_to_remove:
        del st.session_state.order[item]

    # kalo order kosong ini
    if not st.session_state.order:
        st.sidebar.write("Your cart is now empty.")
else:
    st.sidebar.subheader("Your cart is empty. Start adding items!")

# Order Now button
if st.sidebar.button("Order Now"):
    if st.session_state.order:
        # Prepare the data for the Excel file
        order_data = [{"Item": item, "Quantity": quantity} for item, quantity in st.session_state.order.items()]
        # Add an order ID or timestamp to the data
        order_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in order_data:
            row["Order ID"] = order_id  # Assign the same order ID to all items in this order

        # Convert to DataFrame
        df = pd.DataFrame(order_data)

        try:
            if os.path.exists(excel_file_path):
                # Append to the existing Excel file
                with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    startrow = writer.sheets['Sheet1'].max_row  # Find the last row in the existing sheet
                    df.to_excel(writer, index=False, header=False, startrow=startrow)  # Append without headers
            else:
                # Create a new Excel file if it doesn't exist
                with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                    # Write with headers for a new file
                    df.to_excel(writer, index=False)

        except Exception as e:
            # Handle corrupted or invalid file
            st.error(f"An error occurred: {e}. Creating a new Orders.xlsx file.")
            # Create a new file
            wb = Workbook()
            wb.save(excel_file_path)
            with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

        # Notify the user
        st.sidebar.success("Your order has been placed and saved!")
        st.sidebar.markdown(f"[Download Orders Excel File](Orders.xlsx)")

        # Clear the current order
        st.session_state.order = {}

    else:
        st.sidebar.warning("Your cart is empty. Please add items before ordering.")
