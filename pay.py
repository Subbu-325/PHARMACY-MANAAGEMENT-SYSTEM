import streamlit as st
import pandas as pd

def billing_system():

    # ---------- SESSION STATE ----------
    if "bill_items" not in st.session_state:
        st.session_state.bill_items = []

    # ---------- LOAD MEDICINES ----------
    try:
        medicine_df = pd.read_excel("medicine_data.xlsx")
    except:
        medicine_df = pd.DataFrame(
            columns=["Name", "Category", "Price", "Quantity", "Expiry"]
        )

    # ---------- TITLE ----------
    st.title("💊 Medical Billing System")

    # ---------- CUSTOMER DETAILS ----------
    st.subheader("Customer Details")
    customer_name = st.text_input("Customer Name", key="billing_customer")
    st.divider()

    # ---------- MEDICINE DETAILS ----------
    st.subheader("Medicine Details")
    if medicine_df.empty:
        st.warning("No medicines available")
    else:
        medicine_list = medicine_df["Name"].tolist()
        selected_medicine = st.selectbox("Select Medicine", medicine_list)
        row = medicine_df[medicine_df["Name"] == selected_medicine].iloc[0]
        price = float(row["Price"])
        stock = int(row["Quantity"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Price", value=str(price), disabled=True)
        with col2:
            st.text_input("Available Stock", value=str(stock), disabled=True)
        with col3:
            qty = st.number_input("Quantity", min_value=1, max_value=max(stock, 1), value=1)

        if st.button("➕ Add To Bill", use_container_width=True):
            total = price * qty
            st.session_state.bill_items.append({
                "Medicine": selected_medicine,
                "Quantity": qty,
                "Price": price,
                "Total": total
            })
            st.success(f"{selected_medicine} added successfully")

    st.divider()

    # ---------- BILL ITEMS ----------
    st.subheader("Bill Items")
    bill_df = pd.DataFrame(st.session_state.bill_items)
    st.dataframe(bill_df, use_container_width=True)
    st.divider()

    # ---------- TOTALS ----------
    subtotal = bill_df["Total"].sum() if not bill_df.empty else 0
    gst = subtotal * 0.05
    grand_total = subtotal + gst

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Subtotal", f"₹{subtotal:.2f}")
    with col2:
        st.metric("GST (5%)", f"₹{gst:.2f}")
    with col3:
        st.metric("Grand Total", f"₹{grand_total:.2f}")

    st.divider()

    # ---------- ACTION BUTTONS ----------
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧾 Generate Bill", use_container_width=True):
            st.subheader("Invoice")
            st.write(f"Customer Name : {customer_name}")
            st.dataframe(bill_df, use_container_width=True)
            st.write(f"Subtotal : ₹{subtotal:.2f}")
            st.write(f"GST (5%) : ₹{gst:.2f}")
            st.write(f"Grand Total : ₹{grand_total:.2f}")
    with col2:
        if st.button("🗑️ Clear Bill", use_container_width=True):
            st.session_state.bill_items = []
            st.rerun()
