import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AGRIDSS AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "farmer_profile" not in st.session_state:
    st.session_state.farmer_profile = {}

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------

st.sidebar.title("AGRIDSS AI")

st.sidebar.caption("Agricultural Decision Support System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Farmer Profile",
        "AI Chat",
    ],
)


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

if page == "Home":

    st.title("AGRIDSS AI")

    st.subheader(
        "AI-Powered Agricultural Decision Support"
    )

    st.write(
        """
        A simplified MVP for helping farmers access agricultural
        information, create farmer profiles, and interact with an
        AI agricultural assistant.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Farmer Profile")
        st.write(
            "Create and maintain basic farmer and farm information."
        )

        if st.button(
            "Create Farmer Profile",
            key="home_profile",
            use_container_width=True,
        ):
            st.session_state.selected_page = "Farmer Profile"
            st.rerun()

    with col2:
        st.subheader("AI Agricultural Assistant")
        st.write(
            "Ask questions about crops, farming practices, irrigation, "
            "pests, diseases, and agricultural planning."
        )

        if st.button(
            "Open AI Chat",
            key="home_chat",
            use_container_width=True,
        ):
            st.session_state.selected_page = "AI Chat"
            st.rerun()

    with col3:
        st.subheader("MVP Platform")
        st.write(
            "Simple Streamlit architecture designed for rapid "
            "validation before adding a database and advanced AI."
        )

    st.divider()

    st.info(
        "MVP Version 1.0 — Streamlit application"
    )


# ---------------------------------------------------------
# FARMER PROFILE
# ---------------------------------------------------------

elif page == "Farmer Profile":

    st.title("Farmer Profile")

    st.write(
        "Enter the farmer and farm information below."
    )

    with st.form("farmer_profile_form"):

        col1, col2 = st.columns(2)

        with col1:

            farmer_name = st.text_input(
                "Farmer Name"
            )

            phone = st.text_input(
                "Phone Number"
            )

            location = st.text_input(
                "Farm Location"
            )

            farm_size = st.number_input(
                "Farm Size (hectares)",
                min_value=0.0,
                step=0.1,
            )

        with col2:

            crop = st.selectbox(
                "Primary Crop",
                [
                    "Wheat",
                    "Maize",
                    "Rice",
                    "Vegetables",
                    "Fruits",
                    "Other",
                ],
            )

            irrigation = st.selectbox(
                "Irrigation Method",
                [
                    "Rain-fed",
                    "Drip Irrigation",
                    "Sprinkler",
                    "Flood Irrigation",
                    "Other",
                ],
            )

            experience = st.number_input(
                "Farming Experience (years)",
                min_value=0,
                step=1,
            )

            farm_type = st.selectbox(
                "Farm Type",
                [
                    "Small Farm",
                    "Medium Farm",
                    "Large Farm",
                    "Commercial Farm",
                ],
            )

        notes = st.text_area(
            "Additional Information"
        )

        submitted = st.form_submit_button(
            "Save Farmer Profile",
            use_container_width=True,
        )

    if submitted:

        st.session_state.farmer_profile = {
            "Farmer Name": farmer_name,
            "Phone": phone,
            "Location": location,
            "Farm Size": farm_size,
            "Primary Crop": crop,
            "Irrigation": irrigation,
            "Experience": experience,
            "Farm Type": farm_type,
            "Notes": notes,
        }

        st.success(
            "Farmer profile saved successfully."
        )

    if st.session_state.farmer_profile:

        st.divider()

        st.subheader("Current Farmer Profile")

        profile = st.session_state.farmer_profile

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**Farmer:** {profile.get('Farmer Name', '')}"
            )
            st.write(
                f"**Phone:** {profile.get('Phone', '')}"
            )
            st.write(
                f"**Location:** {profile.get('Location', '')}"
            )
            st.write(
                f"**Farm Size:** {profile.get('Farm Size', '')} hectares"
            )

        with col2:
            st.write(
                f"**Primary Crop:** {profile.get('Primary Crop', '')}"
            )
            st.write(
                f"**Irrigation:** {profile.get('Irrigation', '')}"
            )
            st.write(
                f"**Experience:** {profile.get('Experience', '')} years"
            )
            st.write(
                f"**Farm Type:** {profile.get('Farm Type', '')}"
            )


# ---------------------------------------------------------
# AI CHAT
# ---------------------------------------------------------

elif page == "AI Chat":

    st.title("AI Agricultural Assistant")

    st.write(
        "Ask questions about farming and agricultural practices."
    )

    # Display existing messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Ask an agricultural question..."
    )

    if prompt:

        # Store user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.write(prompt)

        # Temporary MVP response
        response = (
            "Thank you for your question. "
            "The AI agricultural assistant is currently running "
            "in MVP mode. The next step is to connect this chat "
            "interface to an AI model."
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        with st.chat_message("assistant"):
            st.write(response)