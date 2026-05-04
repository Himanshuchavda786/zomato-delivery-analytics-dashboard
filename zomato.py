import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("Zomato.csv")

    df.columns = df.columns.str.strip()

    df['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')
    df['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Ratings'], errors='coerce')

    df['Delivery_person_Age'].fillna(df['Delivery_person_Age'].mean(), inplace=True)
    df['Delivery_person_Ratings'].fillna(df['Delivery_person_Ratings'].mean(), inplace=True)

    df['Weather_conditions'].fillna("Unknown", inplace=True)
    df['Road_traffic_density'].fillna("Unknown", inplace=True)
    df['Festival'].fillna("No", inplace=True)

    df['Time_taken (min)'].fillna(df['Time_taken (min)'].median(), inplace=True)
    df = df.drop_duplicates()
    df["Order_Time"] = df["Time_Orderd"].astype(str).str.strip()

    df['City'] = df['City'].astype(str).str.strip().str.title()
    df["Order"] = df["Type_of_order"].astype(str).str.strip()
    df["Vehicle"] = df["Type_of_vehicle"].astype(str).str.strip()

    return df

df = load_data()

st.set_page_config(page_title="Zomato Data Analytics",layout="wide")

params = st.query_params

if "page" not in params:
    params["page"] = "Dataset"

current_page = params["page"]

st.markdown("""
<style>

/* =====================================================
   🍽️ ZOMATO SIDEBAR BACKGROUND
===================================================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #fff6f6 50%,
        #ffecec 100%
    ) !important;

    border-right: 1px solid #f1f1f1;
    padding-top: 10px;
}

/* remove blur */
section[data-testid="stSidebar"] > div {
    backdrop-filter: none !important;
}

/* =====================================================
   🔤 TEXT STYLE
===================================================== */
section[data-testid="stSidebar"] * {
    color: #2b2b2b !important;
    font-weight: 500;
}

/* =====================================================
   🎯 OPTION MENU FIX
===================================================== */

/* normal item */
.nav-link {
    font-size: 15px !important;
    text-align: left !important;
    margin: 6px 6px !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
    color: #555 !important;
    background-color: transparent !important;
    transition: all 0.25s ease !important;
}

/* hover */
.nav-link:hover {
    background-color: rgba(226, 55, 68, 0.08) !important;
    color: #e23744 !important;
}

/* selected item (IMPORTANT PART) */
.nav-link-selected {
    background-color: rgba(226, 55, 68, 0.15) !important; /* light red */
    color: #e23744 !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}

/* icons */
.nav-link svg {
    color: #777 !important;
}

.nav-link:hover svg,
.nav-link-selected svg {
    color: #e23744 !important;
}

/* =====================================================
   🍴 ZOMATO TITLE
===================================================== */
.zomato-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: 700;
    color: #e23744;
    padding: 12px 10px 18px 10px;
}

/* divider */
.sidebar-divider {
    height: 1px;
    background: #f1f1f1;
    margin: 5px 0 15px 0;
}


</style>
""", unsafe_allow_html=True)

with st.sidebar:

    # 🔴 ZOMATO TITLE WITH SVG LOGO
    st.markdown("""
    <div class="zomato-title">
        <svg width="26" height="26" viewBox="0 0 512 512">
            <path fill="#E23744" d="M256 32C132 32 32 132 32 256s100 224 224 224 224-100 224-224S380 32 256 32zm0 64c88 0 160 72 160 160s-72 160-160 160-160-72-160-160S168 96 256 96z"/>
        </svg>
        <span>Zomato Analytics</span>
    </div>

    <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)


    # 🎯 OPTION MENU
    selected = option_menu(
        menu_title=None,
        options=[
            "Dataset",
            "Overview",
            "Analytics Dashboard",
            "Data Assistant"
        ],
        icons=[
            "table",
            "eye",
            "graph-up",
            "robot"
        ],
        menu_icon="shop",
        default_index=[
            "Dataset",
            "Overview",
            "Analytics Dashboard",
            "Data Assistant"
        ].index(current_page),

        styles={

            # =========================
            # 📦 CONTAINER
            # =========================
            "container": {
                "padding": "10px",
                "background-color": "#ffffff",
                "border": "1.5px solid #000000",
                "border-radius": "14px",
                "box-shadow": "0 4px 12px rgba(0,0,0,0.05)"
            },

            # =========================
            # 🎯 ICON (BOLD LOOK)
            # =========================
            "icon": {
                "font-size": "19px",
                "color": "#444",
                "font-weight": "700",  # 🔥 bold icon
                "transition": "0.2s"
            },

            # =========================
            # 📌 NAV LINK (TEXT BOLD)
            # =========================
            "nav-link": {
                "font-size": "15.5px",
                "text-align": "left",
                "margin": "6px 4px",
                "padding": "11px 14px",
                "border-radius": "10px",
                "color": "#333",
                "font-weight": "600",  # 🔥 bold text
                "background-color": "transparent",
                "transition": "all 0.25s ease"
            },

            # =========================
            # 🔴 HOVER
            # =========================
            "nav-link:hover": {
                "background-color": "rgba(226, 55, 68, 0.08)",
                "color": "#E23744"
            },

            # =========================
            # 🔥 SELECTED (STRONG FOCUS)
            # =========================
            "nav-link-selected": {
                "background-color": "rgba(226, 55, 68, 0.15)",
                "color": "#E23744",
                "font-weight": "700"  # extra bold when active
            }
        }
    )

if current_page != selected:
    st.query_params["page"] = selected
    st.rerun()

st.markdown("""
<style>

/* =====================================================
   🍽️ ZOMATO DESIGN TOKENS
===================================================== */
:root {
    --bg-main: #fafafa;

    --card-bg: #ffffff;
    --card-hover: #fff1f1;

    --border: #eeeeee;
    --border-red: rgba(226,55,68,0.35);

    --primary: #E23744;
    --primary-soft: rgba(226,55,68,0.12);

    --text: #1c1c1c;
    --muted: #6b6b6b;

    --radius: 14px;
    --transition: 0.25s ease;
}

/* =====================================================
   🌤️ MAIN BACKGROUND
===================================================== */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #ffffff, #fafafa);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

/* =====================================================
   🧠 TEXT SYSTEM
===================================================== */
h1, h2, h3, h4 {
    color: var(--text) !important;
    font-weight: 600;
}

.caption {
    font-size: 13px;
    color: var(--muted);
}

/* =====================================================
   📏 DIVIDER
===================================================== */
.divider {
    height: 4px;
    background: linear-gradient(
        to right,
        transparent,
        rgba(226,55,68,0.25),
        transparent
    );
    border-radius: 4px;          
    margin: 22px 0;
}

/* =====================================================
   🎯 KPI CARDS (ZOMATO STYLE)
===================================================== */
.kpi-card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 18px;
    border: 1px solid var(--border);
    transition: var(--transition);
    cursor: pointer;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;

    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

/* hover */
.kpi-card:hover {
    background: var(--card-hover);
    transform: translateY(-3px);
}

/* 🔴 ACTIVE / SELECTED CARD */
.kpi-card:active {
    background: var(--primary-soft);
    border: 1px solid var(--border-red);
}

/* title */
.kpi-title {
    font-size: 13px;
    color: var(--muted);
}

/* value */
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    margin-top: 6px;
}

/* =====================================================
   📊 CHART CARDS
===================================================== */
.chart-card {
    background: #ffffff;
    border-radius: var(--radius);
    padding: 16px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    transition: all 0.25s ease;
}

/* 🔥 upgraded hover */
.chart-card:hover {
    border: 1px solid var(--border-red);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

/* =====================================================
   🔘 BUTTONS
===================================================== */
.stButton > button {
    background: var(--primary);
    color: white;
    font-weight: 600;
    border-radius: 999px;
    padding: 9px 20px;
    border: none;
    transition: 0.25s;
}

.stButton > button:hover {
    background: #ff4d5a;
    transform: scale(1.04);
}

/* =====================================================
   🧾 INPUTS
===================================================== */
input, textarea {
    background: #ffffff !important;
    color: #000 !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}

input:focus, textarea:focus {
    border: 1px solid var(--primary) !important;
}

/* =====================================================
   📊 DATAFRAME
===================================================== */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
}

/* =====================================================
   💬 CHAT UI
===================================================== */
[data-testid="stChatMessage"] {
    background: transparent !important;
}

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: var(--primary-soft);
    border-radius: 12px;
    padding: 10px;
}

[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: #f6f6f6;
    border-radius: 12px;
    padding: 10px;
}

section[data-testid="stChatInput"] {
    background: #ffffff;
    border-top: 1px solid var(--border);
}

/* =====================================================
   🏷️ TITLES
===================================================== */
.exec-title {
    font-size: 28px;
    font-weight: 700;
}

.exec-subtitle {
    font-size: 14px;
    color: var(--muted);
}

/* =====================================================
   🚨 ZOMATO ALERT SYSTEM
===================================================== */
[data-testid="stAlert"] {
    background: #ffffff !important;
    border-radius: 10px !important;
    padding: 12px !important;
    border: 1px solid #eeeeee !important;
}

/* remove icon */
[data-testid="stAlert"] svg {
    display: none !important;
}

/* text */
[data-testid="stAlert"] p {
    color: #333 !important;
    font-weight: 500;
}

/* 🔴 ERROR */
[data-testid="stAlert"][kind="error"] {
    border-left: 4px solid #E23744 !important;
}

/* 🟢 SUCCESS */
[data-testid="stAlert"][kind="success"] {
    border-left: 4px solid #16a34a !important;
}

/* 🔵 INFO */
[data-testid="stAlert"][kind="info"] {
    border-left: 4px solid #3b82f6 !important;
}

/* 🟡 WARNING */
[data-testid="stAlert"][kind="warning"] {
    border-left: 4px solid #f59e0b !important;
}

/* =========================
   🔴 DOWNLOAD BUTTON FIX
========================= */
.stDownloadButton > button {
    background-color: #E23744 !important;   /* Zomato red */
    color: #ffffff !important;             /* white text */
    font-weight: 600;
    border-radius: 10px;
    padding: 10px 18px;
    border: none;
    transition: all 0.25s ease;
}

/* hover */
.stDownloadButton > button:hover {
    background-color: #ff4d5a !important;
    color: #ffffff !important;
    transform: scale(1.04);
}

/* active click */
.stDownloadButton > button:active {
    background-color: #cc2f3c !important;
}

/* remove weird focus outline */
.stDownloadButton > button:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* =====================================================
   📂 EXPANDER HEADER FIX
===================================================== */

/* expander header text */
[data-testid="stExpander"] summary {
    color: #1c1c1c !important;   /* dark black */
    font-weight: 600;
}

/* arrow icon */
[data-testid="stExpander"] summary svg {
    color: #E23744 !important;   /* zomato red */
}

/* hover effect */
[data-testid="stExpander"] summary:hover {
    color: #E23744 !important;
}

/* =========================
   🔴 TABS FIX (ZOMATO STYLE)
========================= */
button[data-baseweb="tab"] {
    background-color: #ffffff !important;
    color: #444 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    margin-right: 6px !important;
    border: 1px solid #eee !important;
    font-weight: 600;
}

/* active tab */
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #E23744 !important;
    color: #ffffff !important;
    border: none !important;
}

/* hover */
button[data-baseweb="tab"]:hover {
    background-color: #ffecec !important;
    color: #E23744 !important;
}

/* =========================
   🔍 TEXT INPUT FIX
========================= */

/* input text color */
input[data-testid="stTextInput"] {
    color: #1c1c1c !important;
}

/* actual input field */
div[data-baseweb="input"] input {
    color: #1c1c1c !important;
    background-color: #ffffff !important;
}

/* placeholder color */
div[data-baseweb="input"] input::placeholder {
    color: #9ca3af !important;   /* soft gray */
}

/* border */
div[data-baseweb="input"] {
    border: 1px solid #eeeeee !important;
    border-radius: 10px !important;
}

/* focus state */
div[data-baseweb="input"]:focus-within {
    border: 1px solid #E23744 !important;
    box-shadow: 0 0 0 1px rgba(226,55,68,0.2);
}

/* =========================
   🔍 INPUT LABEL (STRONG)
========================= */
.input-label {
    font-size: 16px;
    font-weight: 600;
    color: #1c1c1c;   /* dark black */
    margin-bottom: 6px;  /* close to input */
}

/* =========================
   🔴 SUGGESTION CHIPS
========================= */
.suggest-chip {
    background: #fff5f5;
    color: #E23744;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid #ffe0e0;
    cursor: pointer;
    transition: all 0.2s ease;
}

/* hover */
.suggest-chip:hover {
    background: #E23744;
    color: white;
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

if current_page == "Dataset":

    # =========================
    # 🏷️ HEADER
    # =========================
    st.markdown('<div class="exec-title">📊 Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="exec-subtitle">Explore, filter and analyze your Zomato dataset efficiently</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 🎯 KPI CARDS
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Rows</div>
            <div class="kpi-value">{df.shape[0]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Columns</div>
            <div class="kpi-value">{df.shape[1]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Missing Values</div>
            <div class="kpi-value">{df.isna().sum().sum()}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 🔍 FILTER SECTION (CARD)
    # =========================
    with st.expander("Dataset Filtering & Exploration", expanded=True):
        # ---------------------
        # COLUMN SELECTION
        # ---------------------
        st.markdown("**Select Columns**")
        select_columns = st.multiselect(
            "Choose columns",
            df.columns,
            default=df.columns
        )

        filter_df = df[select_columns]

        # ---------------------
        # SEARCH
        # ---------------------
        st.markdown("**Search in Dataset**")
        search_value = st.text_input("Search keyword")

        if search_value:
            filter_df = filter_df[
                filter_df.astype(str).apply(
                    lambda row: row.str.contains(search_value, case=False).any(),
                    axis=1
                )
            ]

        # ---------------------
        # COLUMN FILTER
        # ---------------------
        st.markdown("**Column Filter**")
        col5, col6 = st.columns(2)

        with col5:
            filter_col = st.selectbox("Select Column", filter_df.columns)

        with col6:
            filter_value = st.selectbox(
                "Select Value",
                filter_df[filter_col].dropna().unique()
            )

        if st.button("Apply Filter"):
            filter_df = filter_df[filter_df[filter_col] == filter_value]

        # ---------------------
        # ROW CONTROL
        # ---------------------
        st.markdown("**Rows to Display**")
        row = st.slider("Select number of rows", 10, len(filter_df), min(100, len(filter_df)))

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 📊 DATA TABLE (CARD)
    # =========================

    st.subheader("📋 Zomato Dataset Table")
    st.dataframe(filter_df.head(row), use_container_width=True)

    if st.checkbox("Show Full Dataset"):
        st.dataframe(df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 📈 COLUMN STATS
    # =========================

    st.subheader("📈 Column Statistics")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select Numeric Column", numeric_cols)
        st.dataframe(filter_df[selected_col].describe().to_frame())

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 📥 DOWNLOAD
    # =========================

    st.subheader("📥 Download Data")

    csv = filter_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Filtered Dataset",
        csv,
        "zomato_filtered.csv",
        "text/csv"
    )

    st.markdown('</div>', unsafe_allow_html=True)

if current_page == "Overview":

    st.markdown('<div class="exec-title">Zomato Operations Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="exec-subtitle">Delivery performance, efficiency & operational insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 📊 KPI CALCULATIONS
    # =========================
    total_orders = len(df)
    avg_delivery_time = df["Time_taken (min)"].mean()
    avg_rating = df["Delivery_person_Ratings"].mean()
    total_delivery_partners = df["Delivery_person_ID"].nunique()
    festival_orders = df[df["Festival"] == "Yes"].shape[0]
    highest_order_type = df["Type_of_order"].mode()[0]

    # =========================
    # 🎯 KPI CARDS (CUSTOM UI)
    # =========================
    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi_card(title, value):
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    with k1:
        kpi_card("Delivery Partners", total_delivery_partners)

    with k2:
        kpi_card("Avg Rating", f"{avg_rating:.2f}")

    with k3:
        kpi_card("Avg Delivery Time", f"{avg_delivery_time:.1f} min")

    with k4:
        kpi_card("Festival Orders", festival_orders)

    with k5:
        kpi_card("Top Order Type", highest_order_type)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 🏙️ CITY PERFORMANCE
    # =========================
    st.subheader("City Tier Performance Overview")

    city = df[df['City'] != 'nan'].groupby('City').agg(
        Total_Orders=('ID', 'count'),
        Total_delivery_person=("Delivery_person_ID", "nunique"),
        Avg_delivery_person_Age=("Delivery_person_Age", "mean"),
        Avg_Delivery_Time=('Time_taken (min)', 'mean'),
        Avg_Rating=('Delivery_person_Ratings', 'mean')
    ).fillna(0)

    city['Volume Share %'] = (city['Total_Orders'] / total_orders) * 100

    st.dataframe(
        city.style.format({
            "Avg_delivery_person_Age": "{:.0f}",
            "Avg_Delivery_Time": "{:.1f} mins",
            "Avg_Rating": "{:.2f}",
            "Volume Share %": "{:.1f}%"
        }).background_gradient(subset=["Total_Orders", "Volume Share %"], cmap="Reds"),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 🚦 TRAFFIC & WEATHER
    # =========================
    col_t, col_w = st.columns(2)

    with col_t:
        st.subheader("Traffic Impact")

        df['Traffic'] = df['Road_traffic_density'].astype(str).str.strip()
        traffic_df = df[df['Traffic'] != 'nan'].groupby("Traffic").agg(
            Orders=('ID', 'count'),
            Avg_Time=('Time_taken (min)', 'mean')
        ).sort_values(by="Avg_Time", ascending=False)

        st.dataframe(
            traffic_df.style.format({"Avg_Time": "{:.1f} mins"}),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_w:
        st.subheader("Weather Impact")

        df['Weather'] = df['Weather_conditions'].astype(str).str.strip()
        weather_df = df[df['Weather'] != 'nan'].groupby("Weather").agg(
            Orders=('ID', 'count'),
            Avg_Time=('Time_taken (min)', 'mean')
        ).sort_values(by="Avg_Time", ascending=False)

        st.dataframe(
            weather_df.style.format({"Avg_Time": "{:.1f} mins"}),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 🚗 VEHICLE PERFORMANCE
    # =========================
    st.subheader("Vehicle Performance")

    df["Vehicle"] = df["Type_of_vehicle"].astype(str).str.strip()

    vehicle_df = df.groupby("Vehicle").agg(
        Total_Orders=("ID", "count"),
        Avg_Time=("Time_taken (min)", "mean"),
        Avg_Rating=("Delivery_person_Ratings", "mean")
    )

    st.dataframe(vehicle_df.style.background_gradient(subset=["Total_Orders"], cmap="Reds"),
                 use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # ⏱️ ORDERS + TYPE
    # =========================
    col_hour, col_order = st.columns([6,4])

    with col_order:
        st.subheader("Order Insights")

        df["Order_Type"] = df["Type_of_order"].astype(str).str.strip()
        order_df = (df["Order_Type"].value_counts(normalize=True) * 100).to_frame("Share %")

        st.dataframe(order_df.style.format("{:.1f}%"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_hour:
        st.subheader("Orders Per Hour")

        df["Order_Time"] = pd.to_datetime(df["Order_Time"], errors="coerce")
        df["Order_Hour"] = df["Order_Time"].dt.hour

        hour_df = df.groupby("Order_Hour").agg(
            Orders=("ID", "count"),
            Avg_Time=("Time_taken (min)", "mean")
        )

        st.dataframe(hour_df.style.format({"Avg_Time": "{:.1f} min"}),
                     use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 🎉 FESTIVAL + TOP DRIVERS
    # =========================
    st.subheader("Festival Impact")

    festival_df = df.groupby("Festival").agg(
        Orders=("ID", "count"),
        Avg_Time=("Time_taken (min)", "mean")
    )

    st.dataframe(festival_df.style.format({"Avg_Time": "{:.1f} min"}), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Top Delivery Persons")

    top_delivers = df.groupby("Delivery_person_ID").agg(
        Orders=("ID", "count"),
        Avg_Rating=("Delivery_person_Ratings", "mean"),
        Avg_Time=("Time_taken (min)", "mean")
    ).sort_values(by="Orders", ascending=False).head(5)

    st.dataframe(top_delivers, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # =========================
    # 🔍 DATA QUALITY
    # =========================
    with st.expander("Data Quality Check"):
        col_a, col_b = st.columns(2)


        def small_kpi(title, value):
            st.markdown(f"""
            <div class="kpi-card" style="padding:14px;">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)


        with col_a:
            small_kpi("Duplicate Rows", df.duplicated().sum())

        with col_b:
            small_kpi("Missing Values", df.isna().sum().sum())

        st.markdown("<br>", unsafe_allow_html=True)

        st.info("Missing values are normal in real-world delivery data")
        st.success("Overview generated successfully")

def zomato_chart(fig):
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",

        font=dict(
            color="#1c1c1c",
            size=13
        ),

        # ✅ CENTER TITLE (MAIN FIX)
        title=dict(
            x=0.5,
            xanchor='center',
            y=0.95,
            font=dict(size=16, color="#1c1c1c")
        ),

        xaxis=dict(
            title_font=dict(color="#333"),
            tickfont=dict(color="#333"),
            gridcolor="#f1f1f1"
        ),

        yaxis=dict(
            title_font=dict(color="#333"),
            tickfont=dict(color="#333"),
            gridcolor="#f1f1f1"
        ),

        legend=dict(
            font=dict(color="#333")
        ),

        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig

def chart_card(fig):
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div><div style="height:10px;"></div>', unsafe_allow_html=True)

if current_page == "Analytics Dashboard":
    st.markdown('<div class="exec-title">📊 Zomato Operations Intelligence Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="exec-subtitle">Real-time insights into delivery performance, customer behavior, and operational efficiency</div>',
        unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Executive Dashboard", "Advanced Insights"])

    # =====================================================
    # 📊 TAB 1
    # =====================================================
    with tab1:
        st.subheader("Executive Dashboard")

        col_1, col_2 = st.columns([5,6])

        # 📈 Demand Pattern
        with col_1:
            df["Order_Time"] = pd.to_datetime(df["Time_Orderd"], errors="coerce")
            df["Hour"] = df["Order_Time"].dt.hour

            hour_df = df.groupby("Hour").size().reset_index(name="Orders")

            fig = px.line(hour_df, x="Hour", y="Orders", markers=True,
                          title="Order Demand Pattern")
            fig.update_traces(line=dict(color="#E23744", width=3))

            chart_card(zomato_chart(fig))

        # 🥧 City Distribution
        with col_2:
            city = df['City'].value_counts()

            fig = px.pie(
                names=city.index,
                values=city.values,
                hole=0.4,
                title="City Performance Distribution",
                color_discrete_sequence=["#E23744","#ff6b6b","#ff9f9f","#ffd6d6"]
            )

            fig.update_traces(
                textfont=dict(color="#1c1c1c", size=13),  # 🔥 label visible
                insidetextorientation='radial'
            )

            chart_card(zomato_chart(fig))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        col_3, col_4 = st.columns(2)

        # 📊 Traffic Impact
        with col_3:
            t = df.groupby("Road_traffic_density")["Time_taken (min)"].mean()

            fig = px.bar(
                t, x=t.index, y=t.values,
                title="Traffic Impact on Delivery Time",
                color=t.values,
                color_continuous_scale=["#ffe5e5","#ff4d4d"],
                labels={"x":"Traffic Density","y":"Avg Time Taken"}
            )

            fig.update_traces(
                textfont=dict(color="#1c1c1c"),
                marker=dict(line=dict(color="#ffffff", width=1))
            )

            chart_card(zomato_chart(fig))

        # 📊 Weather Impact
        with col_4:
            w = df.groupby("Weather_conditions")["Time_taken (min)"].mean()

            fig = px.bar(
                w, x=w.index, y=w.values,
                title="Weather Impact on Delivery Time",
                color=w.values,
                color_continuous_scale=["#ffe5e5","#ff4d4d"]
            )

            fig.update_traces(
                textfont=dict(color="#1c1c1c"),
                marker=dict(line=dict(color="#ffffff", width=1))
            )

            chart_card(zomato_chart(fig))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        col_5, col_6 = st.columns(2)

        # 🚗 Vehicle
        with col_5:
            vehicle = df["Type_of_vehicle"].value_counts()

            fig = px.pie(
                names=vehicle.index,
                values=vehicle.values,
                hole=0.4,
                title="Vehicle Type Distribution",
                color_discrete_sequence=["#E23744","#ff6b6b","#ff9f9f","#ffd6d6"]
            )
            fig.update_traces(
                textfont=dict(color="#1c1c1c", size=13),  # 🔥 label visible
                insidetextorientation='radial'
            )
            chart_card(zomato_chart(fig))

        # 🧾 Order Type
        with col_6:
            order = df["Type_of_order"].value_counts()

            fig = px.pie(
                names=order.index,
                values=order.values,
                hole=0.4,
                title="Customer Order Type Distribution",
                color_discrete_sequence=["#E23744","#ff6b6b","#ff9f9f","#ffd6d6"]
            )
            fig.update_traces(
                textfont=dict(color="#1c1c1c", size=13),  # 🔥 label visible
                insidetextorientation='radial'
            )
            chart_card(zomato_chart(fig))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        col_7, col_8 = st.columns(2)

        # 🎉 Festival
        with col_7:
            festival = df["Festival"].value_counts()

            fig = px.pie(
                names=festival.index,
                values=festival.values,
                hole=0.4,
                title="Festival Impact on Orders",
                color_discrete_sequence=["#E23744","#ff6b6b","#ff9f9f","#ffd6d6"]
            )
            fig.update_traces(
                textfont=dict(color="#1c1c1c", size=13),  # 🔥 label visible
                insidetextorientation='radial'
            )
            chart_card(zomato_chart(fig))

        # 🏆 Top Delivery
        with col_8:
            top = df["Delivery_person_ID"].value_counts().head(5)

            fig = px.bar(
                top,
                x=top.index,
                y=top.values,
                color=top.values,
                title="Top Delivery Partners",
                color_continuous_scale=["#ffe5e5","#ff4d4d"]
            )

            fig.update_traces(
                textfont=dict(color="#1c1c1c"),
                marker=dict(line=dict(color="#ffffff", width=1))
            )

            chart_card(zomato_chart(fig))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # 📊 Histogram
        fig = px.histogram(
            df,
            x="Time_taken (min)",
            nbins=30,
            title="Delivery Time Distribution",
            color_discrete_sequence=["#E23744"]
        )

        fig.update_traces(
            textfont=dict(color="#1c1c1c"),
            marker=dict(line=dict(color="#ffffff", width=1))
        )

        chart_card(zomato_chart(fig))

    # =====================================================
    # 📊 TAB 2
    # =====================================================
    with tab2:
        # 🌞 Sunburst
        st.markdown("<h3>City Performance Analysis</h3>", unsafe_allow_html=True)

        fig = px.sunburst(
            df,
            path=["City","Type_of_order","Type_of_vehicle"],
            values="Time_taken (min)",
            color="Time_taken (min)",
            color_continuous_scale="Reds"
        )
        fig.update_layout(
            title=dict(
                text="City → Order Type → Vehicle Performance Flow",
            )
        )
        chart_card(zomato_chart(fig))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # 🌳 Treemap
        # 🔹 Subheader
        st.markdown("<h3>City Contribution Breakdown</h3>", unsafe_allow_html=True)

        co = df.groupby(["City", "Type_of_order"]).agg(Orders=("ID", "count")).reset_index()

        fig = px.treemap(
            co,
            path=["City", "Type_of_order"],
            values="Orders",
            color="Orders",
            color_continuous_scale="Reds"
        )

        fig.update_layout(
            title=dict(
                text="City vs Order Type Distribution",
                x=0.5,
                xanchor="center"
            )
        )

        chart_card(zomato_chart(fig))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # 📦 Box
        # 🔹 Subheader
        st.markdown("<h3>Delivery Time Consistency</h3>", unsafe_allow_html=True)

        fig = px.box(
            df,
            x="City",
            y="Time_taken (min)",
            color="City"
        )

        fig.update_layout(
            title=dict(
                text="Delivery Time Distribution Across Cities",
                x=0.5,
                xanchor="center"
            ),
            showlegend=False
        )

        chart_card(zomato_chart(fig))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # 🔥 Heatmap
        # 🔹 Subheader
        st.markdown("<h3>Traffic & Weather Impact</h3>", unsafe_allow_html=True)

        combo = df.groupby(
            ["Road_traffic_density", "Weather_conditions"]
        )["Time_taken (min)"].mean().reset_index(name="Avg_Time")

        fig = px.density_heatmap(
            combo,
            x="Road_traffic_density",
            y="Weather_conditions",
            z="Avg_Time",
            color_continuous_scale="Reds"
        )

        fig.update_layout(
            title=dict(
                text="Average Delivery Delay Heatmap",
                x=0.5,
                xanchor="center"
            )
        )

        chart_card(zomato_chart(fig))

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # 🔗 Sankey
        import plotly.graph_objects as go

        # ✅ SUBHEADER (SECTION TITLE)
        st.markdown("<h3>Order Flow Analysis</h3>", unsafe_allow_html=True)

        flow_df = df[["City", "Type_of_order", "Type_of_vehicle"]]

        labels = list(pd.concat([
            flow_df["City"],
            flow_df["Type_of_order"],
            flow_df["Type_of_vehicle"]
        ]).unique())

        l_map = {l: i for i, l in enumerate(labels)}

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                label=labels,
                pad=20,
                thickness=20,
                color="#E23744",
                line=dict(color="#ffffff", width=1.5),
                hovertemplate='%{label}<extra></extra>',
            ),
            link=dict(
                source=flow_df["City"].map(l_map),
                target=flow_df["Type_of_order"].map(l_map),
                value=[1] * len(flow_df),
                color="rgba(226,55,68,0.25)",
                hovertemplate='Flow: %{value}<extra></extra>'
            )
        )])

        # ✅ ADD CHART TITLE (CENTERED)
        fig.update_layout(
            title=dict(
                text="Order Flow Between City → Order Type → Vehicle",
                x=0.5,
                xanchor='center',
                font=dict(size=16, color="#1c1c1c")
            ),
            font=dict(color="#1c1c1c"),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            margin=dict(l=20, r=20, t=60, b=20)
        )

        # ✅ SHOW IN CARD
        chart_card(fig)

if current_page == "Data Assistant":

    st.markdown('<div class="exec-title">🍽️ Zomato Smart Data Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="exec-subtitle">Ask questions about delivery operations and get insights</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label">🔍 Ask your question</div>', unsafe_allow_html=True)

    user_question = st.text_input(
        "",
        placeholder="Type something like: total orders, best city, traffic impact..."
    )

    if user_question:
        q = user_question.lower()

        show_graph = st.button("📊 Show Graph")

        # =========================
        # 📦 TOTAL ORDERS
        # =========================
        if "total orders" in q:
            total = len(df)
            st.success(f"Total Orders: {total}")

            if show_graph:
                city = df["City"].value_counts()
                fig = px.bar(
                    x=city.index,
                    y=city.values,
                    title="Orders by City",
                    color=city.values,
                    color_continuous_scale=["#ffe5e5", "#ff4d4d"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # ⏱️ DELIVERY TIME
        # =========================
        elif "delivery time" in q or "average time" in q:
            avg_time = df["Time_taken (min)"].mean()
            st.success(f"Average Delivery Time: {avg_time:.1f} minutes")

            if show_graph:
                fig = px.histogram(
                    df,
                    x="Time_taken (min)",
                    nbins=30,
                    title="Delivery Time Distribution",
                    color_discrete_sequence=["#E23744"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # 🏙️ BEST CITY
        # =========================
        elif "best city" in q or "fastest city" in q:
            city = df.groupby("City")["Time_taken (min)"].mean()
            st.success(f"Fastest Delivery City: {city.idxmin()} ({city.min():.1f} min)")

            if show_graph:
                fig = px.bar(
                    x=city.index,
                    y=city.values,
                    title="City vs Avg Delivery Time",
                    color=city.values,
                    color_continuous_scale=["#ffe5e5", "#ff4d4d"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # 🛵 DELIVERY PARTNER
        # =========================
        elif "top delivery" in q or "best delivery boy" in q:
            top = df["Delivery_person_ID"].value_counts().head(10)
            st.success(f"Top Delivery Partner: {top.idxmax()} ({top.max()} orders)")

            if show_graph:
                fig = px.bar(
                    x=top.index,
                    y=top.values,
                    title="Top Delivery Partners",
                    color=top.values,
                    color_continuous_scale=["#ffe5e5", "#ff4d4d"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # 🚦 TRAFFIC
        # =========================
        elif "traffic" in q:
            traffic = df.groupby("Road_traffic_density")["Time_taken (min)"].mean()
            st.success("Traffic impact on delivery time shown below")

            if show_graph:
                fig = px.bar(
                    x=traffic.index,
                    y=traffic.values,
                    title="Traffic vs Delivery Time",
                    color=traffic.values,
                    color_continuous_scale=["#ffe5e5", "#ff4d4d"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # 🌦️ WEATHER
        # =========================
        elif "weather" in q:
            weather = df.groupby("Weather_conditions")["Time_taken (min)"].mean()
            st.success("Weather impact on delivery time shown below")

            if show_graph:
                fig = px.bar(
                    x=weather.index,
                    y=weather.values,
                    title="Weather vs Delivery Time",
                    color=weather.values,
                    color_continuous_scale=["#ffe5e5", "#ff4d4d"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # 🍕 ORDER TYPE
        # =========================
        elif "order type" in q:
            order = df["Type_of_order"].value_counts()
            st.success(f"Most Popular Order Type: {order.idxmax()}")

            if show_graph:
                fig = px.pie(
                    names=order.index,
                    values=order.values,
                    title="Order Type Distribution",
                    hole=0.4,
                    color_discrete_sequence=["#E23744","#ff6b6b","#ff9f9f","#ffd6d6"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # 🚗 VEHICLE
        # =========================
        elif "vehicle" in q:
            vehicle = df["Type_of_vehicle"].value_counts()
            st.success(f"Most Used Vehicle: {vehicle.idxmax()}")

            if show_graph:
                fig = px.bar(
                    x=vehicle.index,
                    y=vehicle.values,
                    title="Vehicle Usage",
                    color=vehicle.values,
                    color_continuous_scale=["#ffe5e5", "#ff4d4d"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # ⏰ PEAK HOURS
        # =========================
        elif "hour" in q or "peak time" in q:
            df["Order_Time"] = pd.to_datetime(df["Time_Orderd"], errors="coerce")
            df["Hour"] = df["Order_Time"].dt.hour
            hour = df["Hour"].value_counts().sort_index()

            st.success("Peak order hours shown below")

            if show_graph:
                fig = px.line(
                    x=hour.index,
                    y=hour.values,
                    markers=True,
                    title="Orders Per Hour"
                )
                fig.update_traces(line=dict(color="#E23744", width=3))
                chart_card(zomato_chart(fig))

        # =========================
        # 🎉 FESTIVAL
        # =========================
        elif "festival" in q:
            festival = df["Festival"].value_counts()
            st.success("Festival vs Non-Festival orders")

            if show_graph:
                fig = px.pie(
                    names=festival.index,
                    values=festival.values,
                    title="Festival Impact",
                    hole=0.4,
                    color_discrete_sequence=["#E23744","#ff6b6b"]
                )
                chart_card(zomato_chart(fig))

        # =========================
        # ❗ UNKNOWN
        # =========================
        else:
            st.subheader("💡 Suggested Questions")
            st.markdown("""
            <div style="margin-top:8px; display:flex; flex-wrap:wrap; gap:8px;">

            <span class="suggest-chip">Total Orders</span>
            <span class="suggest-chip">Average Delivery Time</span>
            <span class="suggest-chip">Best City</span>
            <span class="suggest-chip">Traffic Impact</span>
            <span class="suggest-chip">Weather Impact</span>
            <span class="suggest-chip">Order Type</span>
            <span class="suggest-chip">Vehicle Usage</span>
            <span class="suggest-chip">Peak Hours</span>
            <span class="suggest-chip">Festival Impact</span>

            </div>
            """, unsafe_allow_html=True)