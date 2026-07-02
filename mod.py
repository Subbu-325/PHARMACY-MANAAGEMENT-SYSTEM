import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import date

def medicine_management():
    file = "medicine_data.xlsx"
    try:
        df = pd.read_excel(file)
    except:
        df = pd.DataFrame(columns=["Name", "Category", "Price", "Quantity", "Expiry"])

    with st.sidebar:
        select = option_menu(menu_title="MEDICINE",
                             options=["Add Medicine", "Update Medicine", "Delete Medicine", "View Medicine"],
                             icons=["plus-circle", "pencil-square", "trash", "eye"],
                             menu_icon="capsule")

    if select == "Add Medicine":
        st.title("ADD MEDICINE")
        name = st.text_input("Medicine Name")
        category = st.text_input("Category")
        price = st.number_input("Price", format="%.f")
        quantity = st.number_input("Quantity", format="%.f")
        expiry = st.date_input("Expiry Date")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            add_btn = st.button("Add Medicine", use_container_width=True, type="primary")
        if add_btn:
            if not name:
                st.warning("Please enter medicine name")
            elif not category:
                st.warning("Please enter category")
            elif price == 0.0:
                st.warning("Please enter price")
            elif quantity == 0.0:
                st.warning("Please enter quantity")
            elif expiry <= date.today():
                st.warning("Please enter valid expiry date")
            else:
                try:
                    df = pd.read_excel(file)
                except:
                    df = pd.DataFrame(columns=["Name", "Category", "Price", "Quantity", "Expiry"])
                if name in df["Name"].values:
                    st.error(f"{name} already exists in the records")
                else:
                    newdata = pd.DataFrame({"Name": [name], "Category": [category],
                                            "Price": [price], "Quantity": [quantity], "Expiry": [expiry]})
                    df = pd.concat([df, newdata])
                    df.to_excel(file, index=False)
                    st.toast(f"{name} Added Successfully!")
                    st.info("Medicine Added Successfully!")

    if select == "Update Medicine":
        st.title("Update Medicine")
        df = pd.read_excel(file)
        if df.empty:
            st.warning("No medicines available to update")
            st.stop()
        medlist = df["Name"].unique()
        selected = st.selectbox("Select medicine to update", medlist)
        for i in range(len(df)):
            if df["Name"][i] == selected:
                rownumber = i
                break
        name = df["Name"][rownumber]
        category = df["Category"][rownumber]
        price = float(df["Price"][rownumber])
        quantity = float(df["Quantity"][rownumber])
        expiry = df["Expiry"][rownumber]

        new_name = st.text_input("Medicine Name", name)
        new_category = st.text_input("Category", category)
        new_price = st.number_input("Price", value=float(price))
        new_quantity = st.number_input("Quantity", value=float(quantity))
        new_expiry = st.date_input("Expiry", expiry)

        if st.button("SAVE UPDATE", type="primary"):
            if not new_name:
                st.warning("Enter medicine name")
            elif not new_category:
                st.warning("Enter category")
            elif new_price == 0.0:
                st.warning("Enter price")
            elif new_quantity == 0.0:
                st.warning("Enter quantity")
            elif new_expiry <= date.today():
                st.warning("Enter valid expiry date")
            else:
                df.loc[rownumber, "Name"] = new_name
                df.loc[rownumber, "Category"] = new_category
                df.loc[rownumber, "Price"] = new_price
                df.loc[rownumber, "Quantity"] = new_quantity
                df.loc[rownumber, "Expiry"] = new_expiry
                df.to_excel(file, index=False)
                st.toast("Medicine updated successfully")
                st.info("Medicine updated successfully")

    if select == "Delete Medicine":
        st.title("Delete Medicine")
        df = pd.read_excel(file)
        st.subheader("Available Medicines")
        st.dataframe(df)
        if df.empty:
            st.warning("No medicines available to delete")
            st.stop()
        medlist = df["Name"].unique()
        selected = st.selectbox("Select medicine to delete", medlist)
        for i in range(len(df)):
            if df["Name"][i] == selected:
                rownumber = i
                break
        if st.button("Delete Medicine", type="primary"):
            df = df.drop(rownumber).reset_index(drop=True)
            df.to_excel(file, index=False)
            st.success("Medicine deleted successfully")
            st.toast("Medicine deleted successfully")

    if select == "View Medicine":
        st.title("View Medicine")
        df = pd.read_excel(file)
        st.subheader(f"Total Medicines: {len(df)}")
        st.dataframe(df)
