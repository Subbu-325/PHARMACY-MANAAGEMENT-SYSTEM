import streamlit as st
from mod import medicine_management
from pay import billing_system


# --- Main App (shown after login) ---
def show_main_app():
    with st.sidebar:
        st.title("🏥 Pharmacy System")
        menu = st.radio(
            "Menu",
            [
                "🏠 Home",
                "💊 Medicine Management",
                "🧾 Billing",
                "🔐 Account"
            ]
        )
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.auth_page = "Login"
            st.rerun()

    if menu == "🏠 Home":
        st.title("🏥 PHARMACY MANAGEMENT SYSTEM")
        st.success("Welcome to Our Medical Shop")
        st.markdown(
            "## About Us\n\n"
            "Our pharmacy has been serving the community with a commitment to "
            "quality, affordability, and trust. We provide a wide range of "
            "genuine medicines and healthcare products, backed by an efficient "
            "inventory and billing management system that ensures accuracy, "
            "speed, and transparency in every transaction.\n\n"
            "We believe that good health begins with reliable access to the "
            "right medicines at the right time. That is why our system is "
            "designed to help our staff manage stock levels, track expiry "
            "dates, generate accurate bills, and maintain complete records so "
            "customers always get fast, dependable service."
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Medicines", "500+")
        with col2:
            st.metric("Customers", "2000+")
        with col3:
            st.metric("Orders", "1500+")
        st.markdown(
            "### 🕒 Store Timings\n"
            "- Monday - Saturday : 8:00 AM - 10:00 PM\n"
            "- Sunday : 9:00 AM - 8:00 PM\n"
            "- Emergency Services : 24/7\n\n"
            "### 💊 Our Services\n"
            "- **Medicine Sales** — Wide range of prescription and over-the-counter medicines\n"
            "- **Billing System** — Fast, accurate, and transparent billing for every purchase\n"
            "- **Inventory Management** — Real-time stock tracking to avoid shortages and expired stock\n"
            "- **Prescription Medicines** — Dispensed strictly as per valid prescriptions\n"
            "- **Healthcare Products** — Supplements, first-aid, and wellness essentials\n\n"
            "### 🌟 Why Choose Us\n"
            "- ✅ 100% Genuine Medicines\n"
            "- ✅ Trained Pharmacists on Staff\n"
            "- ✅ Quick & Accurate Billing\n"
            "- ✅ Home Delivery Available\n"
            "- ✅ Competitive & Transparent Pricing\n\n"
            "### 📞 Contact Us\n"
            "- **Phone:** +91 8688939860\n"
            "- **Email:** pharmacy@gmail.com\n"
            "- **Address:** Update with your store address here\n\n"
            "---\n"
            "*Use the menu on the left to manage medicines, generate bills, or view your account details.*"
        )

    elif menu == "💊 Medicine Management":
        medicine_management()

    elif menu == "🧾 Billing":
        billing_system()

    elif menu == "🔐 Account":
        st.title("🔐 My Account")
        tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "🔒 Change Password", "📧 Update Email", "🗑️ Delete Account"])

        with tab1:
            st.subheader("👤 Personal Information")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", value=st.session_state.get("user_name", ""))
                age = st.number_input("Age", min_value=1, max_value=120, value=st.session_state.get("user_age", 18))
                gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"],
                                      index=["Select", "Male", "Female", "Other"].index(
                                          st.session_state.get("user_gender", "Select")))
            with col2:
                phone = st.text_input("Phone Number", value=st.session_state.get("user_phone", ""))
                address = st.text_area("Address", value=st.session_state.get("user_address", ""))

            if st.button("💾 Save Profile", use_container_width=True):
                if not name or not phone:
                    st.error("Name and Phone Number are required.")
                elif gender == "Select":
                    st.error("Please select a gender.")
                else:
                    st.session_state.user_name = name
                    st.session_state.user_age = age
                    st.session_state.user_gender = gender
                    st.session_state.user_phone = phone
                    st.session_state.user_address = address
                    st.success("✅ Profile updated successfully!")

            st.divider()
            st.subheader("📋 Current Profile Details")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Name:** {st.session_state.get('user_name', 'Not set')}")
                st.info(f"**Age:** {st.session_state.get('user_age', 'Not set')}")
                st.info(f"**Gender:** {st.session_state.get('user_gender', 'Not set')}")
            with col2:
                st.info(f"**Phone:** {st.session_state.get('user_phone', 'Not set')}")
                st.info(f"**Email:** {st.session_state.get('user_email', 'Not set')}")
                st.info(f"**Address:** {st.session_state.get('user_address', 'Not set')}")

        with tab2:
            st.subheader("🔒 Change Password")
            current_password = st.text_input("Current Password", type="password", key="curr_pass")
            new_password = st.text_input("New Password", type="password", key="new_pass")
            confirm_password = st.text_input("Confirm New Password", type="password", key="conf_pass")
            if st.button("🔒 Update Password", use_container_width=True):
                if not current_password or not new_password or not confirm_password:
                    st.error("Please fill in all fields.")
                elif st.session_state.registered_users.get(st.session_state.user_email) != current_password:
                    st.error("❌ Current password is incorrect.")
                elif new_password != confirm_password:
                    st.error("New passwords do not match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    st.session_state.registered_users[st.session_state.user_email] = new_password
                    st.success("✅ Password updated successfully!")

        with tab3:
            st.subheader("📧 Update Email Address")
            st.info(f"**Current Email:** {st.session_state.get('user_email', 'Not set')}")
            new_email = st.text_input("New Email Address", key="new_email")
            confirm_email = st.text_input("Confirm New Email", key="conf_email")
            password_check = st.text_input("Enter Password to Confirm", type="password", key="email_pass")
            if st.button("📧 Update Email", use_container_width=True):
                if not new_email or not confirm_email or not password_check:
                    st.error("Please fill in all fields.")
                elif new_email != confirm_email:
                    st.error("Email addresses do not match.")
                elif "@" not in new_email:
                    st.error("Please enter a valid email address.")
                elif st.session_state.registered_users.get(st.session_state.user_email) != password_check:
                    st.error("❌ Incorrect password.")
                else:
                    old_email = st.session_state.user_email
                    pwd = st.session_state.registered_users.pop(old_email)
                    st.session_state.registered_users[new_email] = pwd
                    st.session_state.user_email = new_email
                    st.success(f"✅ Email updated to {new_email} successfully!")

        with tab4:
            st.subheader("🗑️ Delete Account")
            st.warning("⚠️ This action is permanent and cannot be undone.")
            confirm_delete = st.text_input("Type DELETE to confirm", key="delete_confirm")
            delete_password = st.text_input("Enter Password", type="password", key="delete_pass")
            if st.button("🗑️ Delete My Account", use_container_width=True):
                if not confirm_delete or not delete_password:
                    st.error("Please fill in all fields.")
                elif confirm_delete != "DELETE":
                    st.error("Please type DELETE exactly to confirm.")
                elif st.session_state.registered_users.get(st.session_state.user_email) != delete_password:
                    st.error("❌ Incorrect password.")
                else:
                    st.session_state.registered_users.pop(st.session_state.user_email, None)
                    st.session_state.logged_in = False
                    st.session_state.auth_page = "Login"
                    st.rerun()


# --- Login Page ---
def show_login():
    st.title("🏥 Pharmacy Management System")
    st.subheader("🔐 Login")

    if "registered_users" not in st.session_state:
        st.session_state.registered_users = {}

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("✅ Login", use_container_width=True):
        # TC-02: Empty fields
        if not email or not password:
            st.error("Please enter email and password.")
        # TC-01: Valid credentials check
        elif email not in st.session_state.registered_users:
            st.error("❌ Email not found. Please sign up first.")
        elif st.session_state.registered_users[email] != password:
            st.error("❌ Incorrect password. Please try again.")
        else:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("✅ Login successful! Redirecting...")
            st.rerun()


# --- Sign Up Page ---
def show_signup():
    st.title("🏥 Pharmacy Management System")
    st.subheader("📝 Sign Up")

    if "registered_users" not in st.session_state:
        st.session_state.registered_users = {}

    name = st.text_input("Full Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

    if st.button("🆕 Create Account", use_container_width=True):
        if not name or not email or not password or not confirm:
            st.error("Please fill in all fields.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        elif email in st.session_state.registered_users:
            st.error("❌ Email already registered. Please login.")
        # TC-03: Password mismatch
        elif password != confirm:
            st.error("Passwords do not match.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            st.session_state.registered_users[email] = password
            st.session_state.user_name = name
            st.success("✅ Account created successfully! Please login.")
            st.session_state.auth_page = "Login"
            st.rerun()


# --- Forgot Password Page ---
def show_forgot_password():
    st.title("🏥 Pharmacy Management System")
    st.subheader("🔑 Forgot Password")

    if "registered_users" not in st.session_state:
        st.session_state.registered_users = {}

    email = st.text_input("Enter your registered Email", key="forgot_email")
    new_pass = st.text_input("New Password", type="password", key="forgot_new_pass")
    confirm_pass = st.text_input("Confirm New Password", type="password", key="forgot_confirm_pass")

    if st.button("🔑 Reset Password", use_container_width=True):
        if not email or not new_pass or not confirm_pass:
            st.error("Please fill in all fields.")
        elif email not in st.session_state.registered_users:
            st.error("❌ Email not found. Please sign up first.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif len(new_pass) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            st.session_state.registered_users[email] = new_pass
            st.success("✅ Password reset successfully! Please login.")
            st.session_state.auth_page = "Login"
            st.rerun()


# =============================================
#           MAIN ENTRY POINT
# =============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "Login"

if "registered_users" not in st.session_state:
    st.session_state.registered_users = {}

# --- STEP 1: Show Login Page if not logged in ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🏥 Welcome to Pharmacy System</h2>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.auth_page = "Login"
    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state.auth_page = "Signup"
    with col3:
        if st.button("🔑 Forgot Password", use_container_width=True):
            st.session_state.auth_page = "Forgot"

    st.divider()

    if st.session_state.auth_page == "Login":
        show_login()
    elif st.session_state.auth_page == "Signup":
        show_signup()
    elif st.session_state.auth_page == "Forgot":
        show_forgot_password()

# --- STEP 2: Show Home Page after login ---
else:
    show_main_app()
