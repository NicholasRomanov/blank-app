import os
import streamlit as st
import pandas as pd
from openpyxl import Workbook
from datetime import datetime

# Path to Excel file
excel_file_path = os.path.join(os.getcwd(), "Orders.xlsx")

# Menu items with images
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

# Initialize the order in session state
if 'order' not in st.session_state:
    st.session_state.order = {}

# Display a banner image
st.image("Img/BurgerBanner.jpg", use_container_width=True)

# Sidebar title
st.sidebar.title("McDonald's Menu")
selected_category = st.sidebar.radio("Select a category:", list(menu_items.keys()))

# Title for the selected category
st.title(selected_category)

# Display menu items with images and add-to-order buttons
for item, img_path in menu_items[selected_category]:
    col1, col2 = st.columns([1, 3])  # Two columns for image and name/button
    with col1:
        st.image(img_path, width=100)
    with col2:
        st.write(f"**{item}**")  # Display item name in bold
        if st.button(f"Add {item}", key=f"add-{item}"):  # Add unique keys for buttons
            if item in st.session_state.order:
                st.session_state.order[item] += 1
            else:
                st.session_state.order[item] = 1
            st.success(f"{item} added to your order!")

# Sidebar to show the current order
st.sidebar.header("Your Order")
if st.session_state.order:
    for ordered_item, quantity in st.session_state.order.items():
        col1, col2 = st.sidebar.columns([2, 1])
        col1.write(f"{ordered_item} {quantity}x")
        
        # Add unique key for each remove button
        if col2.button("Remove", key=f"remove-{ordered_item}"):
            del st.session_state.order[ordered_item]
            st.success(f"{ordered_item} has been removed from your order.")
            st.experimental_rerun()  # Refresh the app to update order display
else:
    st.sidebar.write("Your order is empty.")

# Order Now button at the bottom of the sidebar
if st.sidebar.button("Order Now"):
    if st.session_state.order:
        # Convert the order to a DataFrame and add a timestamp
        order_data = [{"Item": item, "Quantity": quantity} for item, quantity in st.session_state.order.items()]
        order_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in order_data:
            row["Order ID"] = order_id

        df = pd.DataFrame(order_data)

        # Append the order to an existing Excel file
        try:
            if os.path.exists(excel_file_path):
                with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    startrow = writer.sheets['Sheet1'].max_row
                    df.to_excel(writer, index=False, header=False, startrow=startrow)
            else:
                with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)

        except Exception as e:
            st.error(f"Error saving order: {e}. Creating a new file.")
            wb = Workbook()
            wb.save(excel_file_path)
            with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

        # Success message and clear the order
        st.sidebar.success("Your order has been placed!")
        st.sidebar.markdown(f"[Download Orders Excel File](Orders.xlsx)")
        st.session_state.order = {}
    else:
        st.sidebar.warning("Your cart is empty. Please add items before ordering.")
