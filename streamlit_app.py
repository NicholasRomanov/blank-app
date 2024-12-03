import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("McDonald's Menu", ["Burgers", "Drinks", "Desserts"],
        icons=['hamburger', 'cup', 'ice-cream'], menu_icon="cast", default_index=0)

if selected == "Burgers":
    st.title("Burgers")
    st.write("1. Big Mac")
    st.write("2. Quarter Pounder")
    st.write("3. McChicken")

elif selected == "Drinks":
    st.title("Drinks")
    st.write("1. Coca-Cola")
    st.write("2. Sprite")
    st.write("3. Iced Tea")

elif selected == "Desserts":
    st.title("Desserts")
    st.write("1. Apple Pie")
    st.write("2. Sundae")
    st.write("3. McFlurry")

if selected == "Burgers":
    quantity = st.number_input("Select quantity for Big Mac", min_value=0)
    if st.button("Order Big Mac"):
        st.success(f"You have ordered {quantity} Big Mac(s).")

streamlit run app.py
