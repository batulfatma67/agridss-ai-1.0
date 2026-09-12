import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st


FARMER_PROFILES_FILE = Path(__file__).resolve().parent / "data" / "farmer_profiles.json"
FARM_SIZE_OPTIONS = list(range(0, 1001))
EXPERIENCE_OPTIONS = list(range(0, 101))
BACKGROUND_COLORS = {
    "Soft green": "#f0f7f1",
    "White": "#ffffff",
    "Light gray": "#f3f5f4",
    "Sky blue": "#e6f2ff",
    "Pale yellow": "#fff8db",
    "Peach": "#fff0e6",
    "Slate": "#e7edf2",
}
AGRICULTURE_HERO_IMAGE = (
    "https://images.unsplash.com/photo-1492496913980-501348b61469"
    "?auto=format&fit=crop&w=2400&q=95&dpr=2"
)


def load_farmer_profiles():
    if not FARMER_PROFILES_FILE.exists():
        return []

    try:
        with FARMER_PROFILES_FILE.open("r", encoding="utf-8") as file:
            profiles = json.load(file)
        return profiles if isinstance(profiles, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_farmer_profiles(profiles):
    FARMER_PROFILES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=FARMER_PROFILES_FILE.parent,
        delete=False,
    ) as temporary_file:
        json.dump(profiles, temporary_file, indent=2)
        temporary_file.write("\n")
        temporary_path = Path(temporary_file.name)

    temporary_path.replace(FARMER_PROFILES_FILE)


def hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[index:index + 2], 16) for index in (0, 2, 4))


def get_text_color(background_color, night_mode):
    if night_mode:
        return "#f8fafc"

    red, green, blue = hex_to_rgb(background_color)
    luminance = (0.299 * red) + (0.587 * green) + (0.114 * blue)
    return "#10251a" if luminance > 155 else "#f8fafc"


def darken_color(color, factor=0.68):
    red, green, blue = hex_to_rgb(color)
    target_red, target_green, target_blue = (31, 92, 58)
    return "#{:02x}{:02x}{:02x}".format(
        int((red * (1 - factor)) + (target_red * factor)),
        int((green * (1 - factor)) + (target_green * factor)),
        int((blue * (1 - factor)) + (target_blue * factor)),
    )


def apply_app_theme(background_color, night_mode, compact_page, home_page):
    app_background = "#252d33" if night_mode else background_color
    surface_color = "#303840" if night_mode else "#ffffff"
    sidebar_color = "#1c242a" if night_mode else darken_color(app_background)
    text_color = get_text_color(background_color, night_mode)
    if home_page:
        text_color = "#f8fafc" if night_mode else "#000000"
    sidebar_text_color = get_text_color(sidebar_color, night_mode)
    table_border_color = "#ffffff" if night_mode else "#b8c9bd"
    table_header_background = "#303840" if night_mode else "#f6faf7"
    hero_overlay_start = (
        "rgba(37, 45, 51, 0.96)" if night_mode else "rgba(240, 247, 241, 0.97)"
    )
    hero_overlay_mid = (
        "rgba(37, 45, 51, 0.82)" if night_mode else "rgba(240, 247, 241, 0.82)"
    )
    hero_overlay_end = (
        "rgba(37, 45, 51, 0.35)" if night_mode else "rgba(47, 125, 74, 0.22)"
    )
    compact_styles = """
            [data-testid="stMainBlockContainer"] {
                max-width: 1100px;
                padding-top: 2.75rem;
                padding-bottom: 1.25rem;
            }

            [data-testid="stVerticalBlock"] {
                gap: 0.75rem;
            }

            [data-testid="stHorizontalBlock"] {
                gap: 0.5rem;
            }
        """ if compact_page else ""

    st.markdown(
        f"""
        <style>
            :root {{
                --app-background: {app_background};
                --app-surface: {surface_color};
                --app-sidebar: {sidebar_color};
                --app-text: {text_color};
                --app-sidebar-text: {sidebar_text_color};
                --table-border: {table_border_color};
                --table-header-background: {table_header_background};
                --app-primary: #2f7d4a;
                --app-secondary: #1f5c3a;
                --app-accent: #d6a72c;
                --hero-overlay-start: {hero_overlay_start};
                --hero-overlay-mid: {hero_overlay_mid};
                --hero-overlay-end: {hero_overlay_end};
            }}

            [data-testid="stApp"],
            [data-testid="stAppViewContainer"],
            [data-testid="stAppViewContainer"] > .main,
            [data-testid="stMain"],
            [data-testid="stMainBlockContainer"] {{
                background-color: var(--app-background) !important;
            }}

            [data-testid="stSidebar"],
            [data-testid="stSidebarContent"] {{
                background: var(--app-sidebar) !important;
            }}

            [data-testid="stHeader"] {{
                background: transparent;
            }}

            [data-testid="stAppViewContainer"] .main {{
                color: var(--app-text) !important;
            }}

            [data-testid="stAppViewContainer"],
            [data-testid="stSidebar"] {{
                color: var(--app-text);
            }}

            [data-testid="stAppViewContainer"] .main * {{
                border-color: color-mix(in srgb, var(--app-text) 18%, transparent);
            }}

            [data-testid="stAppViewContainer"] h1,
            [data-testid="stAppViewContainer"] h2,
            [data-testid="stAppViewContainer"] h3,
            [data-testid="stAppViewContainer"] p,
            [data-testid="stAppViewContainer"] label,
            [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"],
            [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] *,
            [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"],
            [data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"] *,
            [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] *,
            [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {{
                color: var(--app-text) !important;
            }}

            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
            [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
            [data-testid="stSidebar"] [data-testid="stWidgetLabel"] * {{
                color: var(--app-sidebar-text) !important;
            }}

            [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {{
                font-size: 1rem;
                opacity: 0.9;
            }}

            [data-testid="stAppViewContainer"] button,
            [data-testid="stAppViewContainer"] [data-testid="stButton"] * {{
                color: var(--app-text) !important;
                background-color: var(--app-surface) !important;
                border-color: color-mix(in srgb, var(--app-text) 24%, transparent) !important;
            }}

            [data-testid="stSidebar"] button,
            [data-testid="stSidebar"] [data-testid="stRadio"] * {{
                color: var(--app-sidebar-text) !important;
            }}

            [data-testid="stAppViewContainer"] button:hover {{
                background-color: color-mix(in srgb, var(--app-primary) 14%, var(--app-surface)) !important;
            }}

            [data-testid="stAppViewContainer"] input,
            [data-testid="stAppViewContainer"] textarea,
            [data-testid="stAppViewContainer"] [data-baseweb="select"] {{
                color: var(--app-text);
                background-color: var(--app-surface);
            }}

            [data-testid="stSidebar"] input,
            [data-testid="stSidebar"] textarea,
            [data-testid="stSidebar"] [data-baseweb="select"] {{
                color: var(--app-sidebar-text);
                background-color: var(--app-surface);
            }}

            .home-clock {{
                color: var(--app-text);
                font-size: 0.85rem;
                line-height: 1.2;
                margin-bottom: 0.25rem;
                opacity: 0.72;
                text-align: right;
            }}

            .sidebar-appearance-spacer {{
                height: clamp(4rem, calc(100vh - 420px), 18rem);
                min-height: 4rem;
            }}

            .home-hero {{
                background-image: linear-gradient(
                    90deg,
                    var(--hero-overlay-start) 0%,
                    var(--hero-overlay-mid) 42%,
                    var(--hero-overlay-end) 100%
                ), url("{AGRICULTURE_HERO_IMAGE}");
                background-position: center right;
                background-size: cover;
                overflow: hidden;
                border: 1px solid rgba(30, 74, 48, 0.18);
                border-radius: 16px;
                min-height: 16rem;
                padding: 2rem 2.2rem;
                margin: 0.25rem 0 0.9rem;
            }}

            .home-kicker {{
                color: var(--app-primary);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
            }}

            .home-hero h1 {{
                color: var(--app-text);
                font-size: 38px;
                line-height: 0.9;
                margin: 0.1rem 0 0;
            }}

            .home-subtitle {{
                color: var(--app-text);
                font-size: 1rem;
                font-weight: 600;
                line-height: 1.1;
                margin: 0 0 0.35rem;
            }}

            .home-hero p {{
                color: var(--app-text);
                font-size: 1rem;
                line-height: 1.4;
                margin: 0;
                max-width: 780px;
                opacity: 0.82;
            }}

            .home-stat {{
                background: var(--app-surface);
                border-left: 4px solid var(--app-primary);
                border-radius: 8px;
                padding: 0.55rem 0.8rem;
            }}

            .home-stat strong {{
                color: var(--app-text);
                display: block;
                font-size: 1.2rem;
            }}

            .home-stat span {{
                color: var(--app-text);
                font-size: 0.76rem;
                opacity: 0.72;
            }}

            [data-testid="stAppViewContainer"] h2 {{
                font-size: 1.25rem;
                margin: 0.7rem 0 0.35rem;
            }}

            [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {{
                font-size: 0.78rem;
            }}

            .profile-table-header,
            .profile-table-row {{
                align-items: center;
                border: 1px solid var(--table-border);
                display: grid;
                gap: 0.75rem;
                grid-template-columns: minmax(130px, 1.2fr) minmax(110px, 1fr) minmax(120px, 1.1fr) minmax(100px, 1fr) minmax(120px, 1fr) minmax(145px, 0.9fr);
                min-height: 3.8rem;
                padding: 0.55rem 0.25rem;
            }}

            .profile-table-header {{
                background: var(--table-header-background);
                color: var(--app-text);
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.06em;
                opacity: 0.7;
                text-transform: uppercase;
            }}

            .profile-table-row {{
                border-top: 0;
                color: var(--app-text);
                font-size: 0.9rem;
            }}

            .profile-table-cell {{
                min-width: 0;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }}

            .profile-actions {{
                display: flex;
                gap: 0.35rem;
            }}

            [data-testid="stVerticalBlockBorderWrapper"] {{
                background: color-mix(in srgb, var(--app-surface) 72%, transparent) !important;
                border: 1px solid var(--table-border) !important;
                border-radius: 10px !important;
                box-shadow: 0 0 0 1px color-mix(in srgb, var(--table-border) 35%, transparent) inset !important;
                margin-bottom: 0.45rem;
            }}

            [data-testid="stVerticalBlockBorderWrapper"] > div {{
                border: 0 !important;
            }}

            .assistant-card {{
                background: var(--app-surface);
                border: 1px solid color-mix(in srgb, var(--app-text) 14%, transparent);
                border-radius: 12px;
                min-height: 9.5rem;
                padding: 1rem;
            }}

            .assistant-card-icon {{
                align-items: center;
                background: color-mix(in srgb, var(--app-primary) 18%, transparent);
                border-radius: 8px;
                color: var(--app-primary);
                display: flex;
                font-size: 1.2rem;
                height: 2.3rem;
                justify-content: center;
                width: 2.3rem;
            }}

            .material-symbols-rounded {{
                font-family: "Material Symbols Rounded";
                font-size: 1.25rem;
                font-weight: normal;
                line-height: 1;
            }}

            .assistant-card h3 {{
                color: var(--app-text);
                font-size: 0.92rem;
                font-weight: 650;
                margin: 0.8rem 0 0.35rem;
                text-transform: capitalize;
            }}

            .assistant-card p {{
                color: var(--app-text);
                font-size: 0.76rem;
                line-height: 1.4;
                margin: 0;
                opacity: 0.72;
            }}

            .assistant-action button {{
                font-size: 0.78rem;
                text-transform: capitalize;
            }}

            .question-list {{
                display: grid;
                gap: 0.35rem;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                margin: 0.8rem 0 1.2rem;
            }}

            .question-list p {{
                background: var(--app-surface);
                border: 1px solid color-mix(in srgb, var(--app-text) 14%, transparent);
                border-radius: 8px;
                color: var(--app-text);
                font-size: 0.9rem;
                margin: 0;
                padding: 0.65rem 0.8rem;
            }}

            {compact_styles}
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_openai_setting(name):
    try:
        openai_secrets = st.secrets.get("openai", {})
        if hasattr(openai_secrets, "get"):
            value = openai_secrets.get(name)
            if value:
                return value
        return st.secrets.get(name.upper()) or st.secrets.get(name)
    except FileNotFoundError:
        return None


def get_openai_api_key():
    return (
        get_openai_setting("api_key")
        or os.getenv("OPENAI_API_KEY")
        or st.session_state.get("openai_api_key_input")
    )


def get_openai_model():
    return get_openai_setting("model") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_ai_model(api_key):
    configured_model = get_openai_model()
    if api_key.startswith("gsk_") and configured_model == "gpt-4o-mini":
        return "openai/gpt-oss-120b"
    return configured_model


def get_ai_base_url(api_key):
    configured_base_url = (
        get_openai_setting("base_url") or os.getenv("OPENAI_BASE_URL")
    )
    if configured_base_url:
        return configured_base_url
    if api_key.startswith("gsk_"):
        return "https://api.groq.com/openai/v1"
    return None


def get_ai_response(messages):
    api_key = get_openai_api_key()
    if not api_key:
        return (
            "OpenAI is not configured yet. Add OPENAI_API_KEY to "
            ".streamlit/secrets.toml or your environment, then try again."
        )

    try:
        from openai import OpenAI

        client_options = {"api_key": api_key}
        base_url = get_ai_base_url(api_key)
        if base_url:
            client_options["base_url"] = base_url
        client = OpenAI(**client_options)
        response = client.chat.completions.create(
            model=get_ai_model(api_key),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert agricultural assistant. Give practical, "
                        "clear advice about crops, soil, irrigation, pests, diseases, "
                        "and farm planning. Mention when local expert advice is needed."
                    ),
                },
                *messages,
            ],
        )
        return response.choices[0].message.content
    except Exception as error:
        return f"I could not reach OpenAI right now: {error}"


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

if "farmer_profiles" not in st.session_state:
    st.session_state.farmer_profiles = load_farmer_profiles()
    if st.session_state.farmer_profiles:
        st.session_state.farmer_profile = st.session_state.farmer_profiles[-1]
elif not FARMER_PROFILES_FILE.exists() and st.session_state.farmer_profiles:
    save_farmer_profiles(st.session_state.farmer_profiles)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "navigation" not in st.session_state:
    st.session_state.navigation = "Home"

if "night_mode" not in st.session_state:
    st.session_state.night_mode = False

if "background_color" not in st.session_state:
    st.session_state.background_color = BACKGROUND_COLORS["Soft green"]

if "background_color_name" not in st.session_state:
    st.session_state.background_color_name = "Soft green"

if "editing_profile_index" not in st.session_state:
    st.session_state.editing_profile_index = None

if "show_background_picker" not in st.session_state:
    st.session_state.show_background_picker = False

if "compact_page" not in st.session_state:
    st.session_state.compact_page = False

if "selected_profile_index" not in st.session_state:
    st.session_state.selected_profile_index = (
        len(st.session_state.farmer_profiles) - 1
        if st.session_state.farmer_profiles
        else None
    )

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

if "show_farmer_form" not in st.session_state:
    st.session_state.show_farmer_form = False


def navigate_to(page_name):
    st.session_state.navigation = page_name


def select_example_question(question):
    st.session_state.selected_question = question


def close_background_picker():
    st.session_state.show_background_picker = False


def apply_selected_background_color():
    st.session_state.background_color = BACKGROUND_COLORS[
        st.session_state.background_color_name
    ]
    st.session_state.show_background_picker = False


def delete_farmer_profile(profile_index):
    st.session_state.farmer_profiles.pop(profile_index)
    save_farmer_profiles(st.session_state.farmer_profiles)
    editing_index = st.session_state.get("editing_profile_index")
    if editing_index == profile_index:
        st.session_state.editing_profile_index = None
    elif editing_index is not None and editing_index > profile_index:
        st.session_state.editing_profile_index = editing_index - 1
    selected_index = st.session_state.get("selected_profile_index")
    if selected_index == profile_index:
        st.session_state.selected_profile_index = (
            min(profile_index, len(st.session_state.farmer_profiles) - 1)
            if st.session_state.farmer_profiles
            else None
        )
    elif selected_index is not None and selected_index > profile_index:
        st.session_state.selected_profile_index = selected_index - 1
    st.session_state.farmer_profile = (
        st.session_state.farmer_profiles[-1]
        if st.session_state.farmer_profiles
        else {}
    )


def edit_farmer_profile(profile_index):
    profile = st.session_state.farmer_profiles[profile_index]
    st.session_state.editing_profile_index = profile_index
    st.session_state.show_farmer_form = True
    st.session_state.selected_profile_index = profile_index
    st.session_state.profile_farmer_name = profile.get("Farmer Name", "")
    st.session_state.profile_growth_stage = profile.get(
        "Crop Growth Stage", ""
    )
    st.session_state.profile_location = profile.get("Location", "")
    st.session_state.profile_farm_size = int(profile.get("Farm Size", 0))
    st.session_state.profile_crop = profile.get("Primary Crop", "Wheat")
    st.session_state.profile_irrigation = profile.get(
        "Irrigation", "Rain-fed"
    )
    st.session_state.profile_experience = profile.get("Experience", 0)
    st.session_state.profile_farm_type = profile.get(
        "Farm Type", "Small Farm"
    )
    st.session_state.profile_notes = profile.get("Notes", "")


def clear_profile_form():
    st.session_state.editing_profile_index = None
    st.session_state.profile_farmer_name = ""
    st.session_state.profile_growth_stage = ""
    st.session_state.profile_location = ""
    st.session_state.profile_farm_size = 0.0
    st.session_state.profile_crop = "Wheat"
    st.session_state.profile_irrigation = "Rain-fed"
    st.session_state.profile_experience = 0
    st.session_state.profile_farm_type = "Small Farm"
    st.session_state.profile_notes = ""


def start_new_farmer():
    clear_profile_form()
    st.session_state.show_farmer_form = True


def show_existing_farmers():
    st.session_state.show_farmer_form = False


def select_farmer_profile(profile_index):
    clear_profile_form()
    st.session_state.show_farmer_form = False
    st.session_state.selected_profile_index = profile_index
    st.session_state.farmer_profile = st.session_state.farmer_profiles[
        profile_index
    ]


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
    key="navigation",
    bind="query-params",
)

st.sidebar.markdown(
    '<div class="sidebar-appearance-spacer"></div>',
    unsafe_allow_html=True,
)
st.sidebar.subheader("Appearance")
st.sidebar.toggle("Night mode", key="night_mode")
st.sidebar.toggle("Compact page", key="compact_page")
st.sidebar.checkbox(
    "Background color",
    key="show_background_picker",
)
if st.session_state.show_background_picker:
    st.sidebar.selectbox(
        "Choose background color",
        list(BACKGROUND_COLORS),
        key="background_color_name",
        on_change=apply_selected_background_color,
    )

if get_openai_api_key():
    st.sidebar.caption("OpenAI API: configured")
else:
    st.sidebar.text_input(
        "OpenAI API key (optional)",
        type="password",
        key="openai_api_key_input",
        help="Used for this session only when no Streamlit secret or environment variable is configured.",
    )
    st.sidebar.caption("OpenAI API: not configured")

apply_app_theme(
    st.session_state.background_color,
    st.session_state.night_mode,
    st.session_state.compact_page,
    page == "Home",
)


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

if page == "Home":

    current_datetime = datetime.now().strftime("%A, %B %d, %Y · %I:%M %p")
    st.markdown(
        f'<div class="home-clock">{current_datetime}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="home-hero">
            <div class="home-kicker">Agricultural Decision Support System</div>
            <h1>AgriDSS AI</h1>
            <div class="home-subtitle">Generative AI Agronomist</div>
            <p>
                Practical farm intelligence in one calm workspace: keep farmer
                records organized and get clear guidance for crops, irrigation,
                pests, diseases, and planning.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.markdown(
            f'<div class="home-stat"><strong>{len(st.session_state.farmer_profiles)}</strong>'
            "<span>saved farmer profiles</span></div>",
            unsafe_allow_html=True,
        )
    with stat_col2:
        st.markdown(
            f'<div class="home-stat"><strong>{len(st.session_state.messages)}</strong>'
            "<span>chat messages</span></div>",
            unsafe_allow_html=True,
        )
    with stat_col3:
        st.markdown(
            '<div class="home-stat"><strong>1.0</strong>'
            "<span>MVP platform version</span></div>",
            unsafe_allow_html=True,
        )

    st.subheader("Start with a task")
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        st.button(
            "Create farmer profile",
            key="home_profile",
            width="stretch",
            on_click=navigate_to,
            args=("Farmer Profile",),
        )
        st.caption("Record farm details once and keep them easy to review.")
    with action_col2:
        st.button(
            "Open AI chat",
            key="home_chat",
            width="stretch",
            on_click=navigate_to,
            args=("AI Chat",),
        )
        st.caption("Ask practical questions and get model-powered guidance.")

    st.subheader("What the app does")
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.markdown("**Farmer records**  \nCapture contact, location, crop, irrigation, and farm size details.")
    with info_col2:
        st.markdown("**Agricultural guidance**  \nUse the AI assistant for focused questions about day-to-day farm decisions.")
    with info_col3:
        st.markdown("**Simple MVP workflow**  \nA lightweight starting point designed to grow with your farm data and needs.")


# ---------------------------------------------------------
# FARMER PROFILE
# ---------------------------------------------------------

elif page == "Farmer Profile":

    st.title("Farmer Profile")

    st.write(
        "Enter the farmer and farm information below."
    )

    if st.session_state.get("editing_profile_index") is None:
        add_col, existing_col = st.columns(2)
        with add_col:
            st.button(
                "Add new farmer",
                key="add_new_farmer",
                width="stretch",
                on_click=start_new_farmer,
            )
        with existing_col:
            st.button(
                "Existing farmers",
                key="existing_farmers",
                width="stretch",
                on_click=show_existing_farmers,
            )
    else:
        st.subheader("Edit farmer profile")

    if st.session_state.show_farmer_form:

        col1, col2 = st.columns(2)

        with col1:

            farmer_name = st.text_input("Farmer Name", key="profile_farmer_name")
            growth_stage = st.text_input(
                "Crop Growth Stage",
                key="profile_growth_stage",
            )
            location = st.text_input("Farm Location", key="profile_location")
            farm_size = st.selectbox(
                "Farm Size (acres)",
                FARM_SIZE_OPTIONS,
                key="profile_farm_size",
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
                key="profile_crop",
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
                key="profile_irrigation",
            )

            experience = st.selectbox(
                "Farming Experience (years)",
                EXPERIENCE_OPTIONS,
                key="profile_experience",
            )

            farm_type = st.selectbox(
                "Farm Type",
                [
                    "Small Farm",
                    "Medium Farm",
                    "Large Farm",
                    "Commercial Farm",
                ],
                key="profile_farm_type",
            )

        notes = st.text_area("Additional Information", key="profile_notes")

        st.caption("Profile data is saved only when you select Save Farmer Profile.")
        editing_index = st.session_state.get("editing_profile_index")
        submitted = st.button(
            "Update Farmer Profile" if editing_index is not None else "Save Farmer Profile",
            key="save_farmer_profile",
            width="stretch",
        )

        if submitted:

            profile = {
                "Farmer Name": farmer_name,
                "Crop Growth Stage": growth_stage,
                "Location": location,
                "Farm Size": farm_size,
                "Primary Crop": crop,
                "Irrigation": irrigation,
                "Experience": experience,
                "Farm Type": farm_type,
                "Notes": notes,
            }
            st.session_state.farmer_profile = profile
            if editing_index is None:
                st.session_state.farmer_profiles.append(profile)
                st.session_state.selected_profile_index = (
                    len(st.session_state.farmer_profiles) - 1
                )
                message = "Farmer profile saved successfully."
            else:
                st.session_state.farmer_profiles[editing_index] = profile
                st.session_state.selected_profile_index = editing_index
                st.session_state.editing_profile_index = None
                st.session_state.show_farmer_form = False
                message = "Farmer profile updated successfully."
            save_farmer_profiles(st.session_state.farmer_profiles)

            if editing_index is not None:
                st.rerun()

            st.success(message)

    if st.session_state.farmer_profiles:

        st.divider()

        st.subheader("Saved Farmer Profiles")
        table_columns = [
            "Farmer Name",
            "Crop Growth Stage",
            "Location",
            "Farm Size (acres)",
        ]
        with st.container(border=True):
            header_columns = st.columns(
                [1.3, 1.2, 1.3, 0.9, 1.25],
                gap="small",
            )
            for header_column, column_name in zip(header_columns, table_columns):
                header_column.markdown(f"**{column_name}**")
            header_columns[-1].markdown("**Actions**")

        for profile_index, saved_profile in enumerate(
            st.session_state.farmer_profiles
        ):
            profile_name = saved_profile.get("Farmer Name") or "Unnamed farmer"
            with st.container(border=True):
                row_columns = st.columns(
                    [1.3, 1.2, 1.3, 0.9, 1.25],
                    gap="small",
                )
                row_values = [
                    profile_name,
                    saved_profile.get("Crop Growth Stage", ""),
                    saved_profile.get("Location", ""),
                    f"{saved_profile.get('Farm Size', 0):g} acres",
                ]
                for row_column, value in zip(row_columns[:4], row_values):
                    row_column.write(value)

                select_col, edit_col, delete_col = row_columns[4].columns(
                    3,
                    gap="small",
                )
                with select_col:
                    st.button(
                        ":material/visibility:",
                        key=f"select_farmer_profile_{profile_index}",
                        help=f"Select {profile_name}",
                        on_click=select_farmer_profile,
                        args=(profile_index,),
                        width="content",
                    )
                with edit_col:
                    st.button(
                        ":material/edit:",
                        key=f"edit_farmer_profile_{profile_index}",
                        help=f"Edit {profile_name}",
                        on_click=edit_farmer_profile,
                        args=(profile_index,),
                        width="content",
                    )
                with delete_col:
                    st.button(
                        ":material/delete:",
                        key=f"delete_farmer_profile_{profile_index}",
                        help=f"Delete {profile_name}",
                        on_click=delete_farmer_profile,
                        args=(profile_index,),
                        width="content",
                    )

    if st.session_state.farmer_profile:

        st.subheader("Current Farmer Profile")

        selected_index = st.session_state.get("selected_profile_index")
        if selected_index is not None and selected_index < len(
            st.session_state.farmer_profiles
        ):
            profile = st.session_state.farmer_profiles[selected_index]
        else:
            profile = st.session_state.farmer_profile

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**Farmer:** {profile.get('Farmer Name', '')}"
            )
            st.write(
                f"**Crop Growth Stage:** {profile.get('Crop Growth Stage', '')}"
            )
            st.write(
                f"**Location:** {profile.get('Location', '')}"
            )
            st.write(
                f"**Farm Size:** {profile.get('Farm Size', ''):g} acres"
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
            st.write(
                f"**Notes:** {profile.get('Notes', '')}"
            )


# ---------------------------------------------------------
# AI CHAT
# ---------------------------------------------------------

elif page == "AI Chat":

    st.title("AI Agricultural Assistant")

    st.write(
        "Ask your AI Agronomist about crops, irrigation, fertilizer, pests, diseases, or crop management."
    )

    st.subheader("🌱 Ask Your AI Agronomist")
    st.write(
        "Ask about crops, irrigation, fertilizer, pests, diseases, or farm management."
    )

    example_questions = [
        ("💧", "When should I irrigate my wheat crop?"),
        ("🌾", "My wheat leaves are turning yellow. What should I check first?"),
        ("💧", "How often should I irrigate maize?"),
        ("🐛", "How can I identify common cotton pests?"),
    ]
    question_columns = st.columns(2, gap="small")
    for question_index, (icon, question) in enumerate(example_questions):
        with question_columns[question_index % 2]:
            st.button(
                f"{icon}  {question}",
                key=f"example_question_{question_index}",
                width="stretch",
                on_click=select_example_question,
                args=(question,),
            )

    if st.session_state.selected_question:
        st.info(
            f"Example selected: {st.session_state.selected_question}",
            icon=":material/chat:",
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

        response = get_ai_response(st.session_state.messages)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        with st.chat_message("assistant"):
            st.write(response)