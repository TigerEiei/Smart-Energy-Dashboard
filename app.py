# =====================================================
# SMART ENERGY DASHBOARD
# ปริศนาค่าไฟฟ้าที่เพิ่มสูงขึ้น
# =====================================================


# =====================================================
# 1. นำเข้าไลบรารี
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =====================================================
# 2. ตั้งค่าหน้าเว็บไซต์
# =====================================================

st.set_page_config(
    page_title="Smart Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)


# =====================================================
# 3. CSS ตกแต่งเว็บไซต์ (แก้ไขเรื่องกรอบกราฟตัดขอบ & Hover เรืองแสง)
# =====================================================

st.markdown("""
<style>

/* =========================================
   พื้นหลังหลัก
   ========================================= */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(59, 130, 246, 0.13),
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 80%,
            rgba(250, 204, 21, 0.10),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #071B33,
            #102C4A,
            #163A5F
        );

    background-attachment: fixed;
}

.block-container {
    position: relative;
    z-index: 2;
    padding-top: 2.5rem;
    padding-bottom: 2.5rem;
    max-width: 100%;
}

/* สีตัวหนังสือหลัก */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: #FACC15 !important;
}

.stApp [data-testid="stMarkdownContainer"] p, 
.stApp [data-testid="stMarkdownContainer"] li {
    color: #EAF4FF !important;
}

.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] * {
    color: #BFDBFE !important;
}

hr {
    border-color: rgba(255,255,255,0.2) !important;
}


/* =========================================
   Sidebar
   ========================================= */

section[data-testid="stSidebar"] {
    background: rgba(5,20,40,0.98);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FACC15 !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #EAF4FF !important;
}

section[data-testid="stSidebar"] [data-testid="stAlert"] {
    background-color: #EAF4FF !important;
    border: 1px solid #FACC15 !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] [data-testid="stAlert"] p,
section[data-testid="stSidebar"] [data-testid="stAlert"] span {
    color: #071B33 !important;
}


/* =========================================
   Dropdown / Selectbox
   ========================================= */

div[data-baseweb="select"] > div {
    background-color: #12314A !important;
    border-color: #FACC15 !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: #EAF4FF !important;
    -webkit-text-fill-color: #EAF4FF !important;
}

div[data-baseweb="popover"],
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li {
    background-color: #12314A !important;
    color: #EAF4FF !important;
}

div[data-baseweb="popover"] li *,
div[data-baseweb="popover"] [role="option"] * {
    color: #EAF4FF !important;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] [role="option"]:hover {
    background-color: #1E4260 !important;
}

div[data-baseweb="popover"] li:hover *,
div[data-baseweb="popover"] [role="option"]:hover * {
    color: #FACC15 !important;
}


/* =========================================
   การกำหนดสไตล์กรอบร่วมกัน (KPI, กราฟ Plotly, ตาราง)
   ========================================= */

/* ปรับระยะห่างภายนอกคอนเทนเนอร์เพื่อไม่ให้โดนขอบแอปตัดเวลา Hover */
[data-testid="stElementContainer"]:has(div[data-testid="stPlotlyChart"]) {
    padding: 6px 4px !important;
    margin-bottom: 15px !important;
}

div[data-testid="stMetric"],
div[data-testid="stPlotlyChart"],
.table-container {
    box-sizing: border-box !important;
    border: 1.5px solid rgba(250, 204, 21, 0.85) !important;
    border-radius: 15px !important;
    background: rgba(18, 49, 74, 0.94) !important;
    box-shadow:
        0 0 6px rgba(250, 204, 21, 0.30),
        0 0 15px rgba(250, 204, 21, 0.15),
        inset 0 0 8px rgba(250, 204, 21, 0.04) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease !important;
}

/* KPI Metric */
div[data-testid="stMetric"] {
    position: relative;
    width: 100% !important;
    padding: 18px !important;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] * {
    color: #FDE68A !important;
}

div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: #FACC15 !important;
}

div[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"] * {
    color: #EAF4FF !important;
}


/* =========================================
   ปรับแต่ง Plotly Chart โดยตรง
   ========================================= */

div[data-testid="stPlotlyChart"] {
    padding: 12px !important;
    overflow: visible !important;
}

div[data-testid="stPlotlyChart"] > div,
div[data-testid="stPlotlyChart"] .js-plotly-plot,
div[data-testid="stPlotlyChart"] .plot-container {
    border-radius: 10px !important;
    background: transparent !important;
}


/* =========================================
   ตาราง
   ========================================= */

.table-container {
    position: relative;
    display: block;
    width: 100%;
    max-width: 100%;
    overflow-x: auto;
    background: #0F2940 !important;
    margin-bottom: 20px;
}


/* =========================================
   เอฟเฟกต์ Hover เหมือนกันทุกกล่อง (เรืองแสงทองลอยขึ้น)
   ========================================= */

div[data-testid="stMetric"]:hover,
div[data-testid="stPlotlyChart"]:hover,
.table-container:hover {
    border-color: #FDE047 !important;
    box-shadow:
        0 0 12px rgba(250, 204, 21, 0.65),
        0 0 26px rgba(250, 204, 21, 0.35),
        inset 0 0 10px rgba(250, 204, 21, 0.08) !important;
    transform: translateY(-4px) !important;
}


/* =========================================
   ปุ่มดาวน์โหลด CSV
   ========================================= */

div[data-testid="stDownloadButton"] button {
    background: #12314A !important;
    color: #FACC15 !important;
    border: 2px solid #FACC15 !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    font-weight: bold !important;
    box-shadow: 0 0 8px rgba(250,204,21,0.35);
    transition: all 0.25s ease !important;
}

div[data-testid="stDownloadButton"] button,
div[data-testid="stDownloadButton"] button * {
    color: #FACC15 !important;
    font-weight: bold !important;
}

div[data-testid="stDownloadButton"] button:hover {
    background: #FACC15 !important;
    border-color: #FDE047 !important;
    color: #071B33 !important;
    transform: translateY(-2px);
}

div[data-testid="stDownloadButton"] button:hover * {
    color: #071B33 !important;
}


/* =========================================
   ตาราง Smart Energy
   ========================================= */

.energy-table {
    width: 100%;
    border-collapse: collapse;
    background-color: #0F2940;
    color: #EAF4FF;
    font-size: 14px;
}

.energy-table th {
    background-color: #12314A !important;
    color: #FACC15 !important;
    font-weight: bold;
    padding: 13px;
    text-align: center;
    border: 1px solid #526078;
    white-space: nowrap;
}

.energy-table td {
    background-color: #0F2940 !important;
    color: #EAF4FF !important;
    padding: 11px;
    text-align: center;
    border: 1px solid #29465E;
    white-space: nowrap;
}

.energy-table tbody tr:hover td {
    background-color: #1E4260 !important;
    color: #FFFFFF !important;
}


/* =========================================
   อีโมจิลอยด้านหลัง
   ========================================= */

@keyframes hoverFloat {
    0% { transform: translateY(0px) rotate(-8deg); }
    50% { transform: translateY(-45px) rotate(8deg); }
    100% { transform: translateY(0px) rotate(-8deg); }
}

.energy-float {
    position: fixed;
    z-index: 0;
    pointer-events: none;
    user-select: none;
    opacity: 0.13;
    animation: hoverFloat ease-in-out infinite;
}

.energy-1 { top: 10%; left: 2%; font-size: 180px; animation-duration: 8s; }
.energy-2 { top: 35%; left: 15%; font-size: 150px; animation-duration: 10s; }
.energy-3 { top: 12%; right: 2%; font-size: 200px; animation-duration: 9s; }
.energy-4 { top: 60%; right: 10%; font-size: 170px; animation-duration: 11s; }
.energy-5 { top: 78%; left: 5%; font-size: 190px; animation-duration: 9s; }
.energy-6 { top: 85%; right: 2%; font-size: 150px; animation-duration: 10s; }

</style>
""", unsafe_allow_html=True)

# =====================================================
# 4. อีโมจิลอยด้านหลัง
# =====================================================

st.markdown("""
<div class="energy-float energy-1">⚡</div>
<div class="energy-float energy-2">💡</div>
<div class="energy-float energy-3">🔌</div>
<div class="energy-float energy-4">🔋</div>
<div class="energy-float energy-5">⚡</div>
<div class="energy-float energy-6">✨</div>
""", unsafe_allow_html=True)


# =====================================================
# 5. ฟังก์ชันตกแต่งกราฟ
# =====================================================

def style_chart(fig):

    fig.update_layout(

        template="plotly_dark",

        autosize=True,

        width=None,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(18,49,74,0.85)",

        font=dict(
            family="Arial",
            color="#EAF4FF",
            size=12
        ),

        title_font=dict(
            color="#38BDF8",
            size=18
        ),

        xaxis=dict(
            color="#BFDBFE",
            gridcolor="#29465E",
            zerolinecolor="#29465E"
        ),

        yaxis=dict(
            color="#BFDBFE",
            gridcolor="#29465E",
            zerolinecolor="#29465E"
        ),

        legend=dict(
            font=dict(
                color="#EAF4FF"
            )
        ),

        margin=dict(
            l=45,
            r=35,
            t=65,
            b=45
        )
    )

    fig.update_traces(
        textfont_color="#FFFFFF",
        marker_line_color="#7DD3FC",
        marker_line_width=0.5
    )

    return fig


# =====================================================
# 6. ฟังก์ชันแสดงกราฟ
# =====================================================

def show_chart(fig, chart_key):

    fig = style_chart(fig)

    fig.update_layout(
        autosize=True,
        width=None,
        height=420,
        margin=dict(
            l=45,
            r=35,
            t=65,
            b=45
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "responsive": True,
            "displayModeBar": False,
            "staticPlot": False
        },
        key=chart_key
    )


# =====================================================
# 7. ฟังก์ชันแสดงตาราง
# =====================================================

def show_table(table):

    if table.empty:

        st.info("ไม่พบข้อมูลในตารางนี้")

        return

    html = table.to_html(
        index=False,
        border=0,
        classes="energy-table",
        escape=True
    )

    st.markdown(
        f"""
        <div class="table-container">
            {html}
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 8. ชื่อเว็บไซต์
# =====================================================

st.title("⚡ Smart Energy Dashboard")

st.subheader(
    "ปริศนาค่าไฟฟ้าที่เพิ่มสูงขึ้น"
)

st.write("""
ระบบวิเคราะห์ข้อมูลการใช้พลังงานไฟฟ้าของสถานศึกษา
เพื่อค้นหาห้องที่ใช้ไฟฟ้าสูง ตรวจสอบพฤติกรรมผิดปกติ
และสนับสนุนการลดต้นทุนพลังงาน
""")

st.caption(
    "ช่วงเวลาข้อมูล: 1 มกราคม – 31 ธันวาคม 2025"
)

st.divider()



# =====================================================
# 9. กำหนดตำแหน่งไฟล์ CSV
# =====================================================

DATA_DIR = Path(__file__).resolve().parent


# =====================================================
# 10. อ่านข้อมูล CSV
# =====================================================

@st.cache_data
def load_data():

    filenames = {
        "system": "system_summary.csv",
        "monthly": "monthly_energy.csv",
        "building": "building_dashboard.csv",
        "room": "room_dashboard.csv",
        "base": "base_load_dashboard.csv",
        "extreme": "extreme_events.csv",
        "unusual": "unusual_dashboard.csv",
        "missing": "missing_dashboard.csv",
        "priority": "priority_dashboard.csv"
    }

    # ค้นหาไฟล์ CSV ทั้งหมดในโฟลเดอร์โปรเจกต์
    available_files = {}

    for file_path in DATA_DIR.rglob("*.csv"):
        available_files[file_path.name.strip().lower()] = file_path

    data = {}
    missing_files = []

    for key, filename in filenames.items():

        file_path = available_files.get(filename.lower())

        if file_path is None:
            missing_files.append(filename)
            continue

        data[key] = pd.read_csv(file_path)

    # แจ้งชื่อไฟล์ที่หาไม่พบ
    if missing_files:

        raise FileNotFoundError(
            "ไม่พบไฟล์ต่อไปนี้: "
            + ", ".join(missing_files)
            + "\n\nไฟล์ CSV ที่พบในโปรเจกต์: "
            + ", ".join(sorted(available_files.keys()))
        )

    return data


# =====================================================
# ตรวจสอบและโหลดข้อมูล
# =====================================================

try:

    data = load_data()

except Exception as error:

    st.error(
        f"เกิดข้อผิดพลาดในการอ่านข้อมูล: {error}"
    )

    st.info("""
    กรุณาตรวจสอบว่าไฟล์ CSV ทั้ง 9 ไฟล์
    ถูกอัปโหลดขึ้น GitHub Repository แล้ว

    และตรวจสอบชื่อไฟล์ให้ตรงกับที่ระบบกำหนด
    """)

    st.stop()

# =====================================================
# 11. แยกข้อมูลแต่ละตาราง
# =====================================================

system = data["system"]
monthly = data["monthly"]
building = data["building"]
room = data["room"]
base = data["base"]
extreme = data["extreme"]
unusual = data["unusual"]
missing = data["missing"]
priority = data["priority"]


# =====================================================
# 12. ฟังก์ชันอ่านค่า KPI
# =====================================================

def get_value(name):

    result = system.loc[
        system["รายการ"] == name,
        "ค่า"
    ]

    if result.empty:
        return 0

    value = pd.to_numeric(
        result.iloc[0],
        errors="coerce"
    )

    return 0 if pd.isna(value) else value


total_energy = get_value("พลังงานไฟฟ้ารวม")

average_energy = get_value(
    "พลังงานเฉลี่ยต่อรายการ"
)

maximum_energy = get_value(
    "ค่าพลังงานสูงสุด"
)

total_buildings = get_value(
    "จำนวนอาคาร"
)

total_rooms = get_value(
    "จำนวนห้อง"
)

base_load_total = get_value(
    "พลังงานช่วงไม่มีผู้ใช้งาน"
)

base_load_percent = get_value(
    "สัดส่วน Base Load"
)


# =====================================================
# 13. ตัวกรองข้อมูล
# =====================================================

st.sidebar.title("🔎 ตัวกรองข้อมูล")

building_options = [
    "ทุกอาคาร"
] + sorted(
    building["building_id"].dropna().unique().tolist()
)

selected_building = st.sidebar.selectbox(
    "เลือกอาคาร",
    building_options
)


def filter_building(table):

    if selected_building == "ทุกอาคาร":
        return table.copy()

    if "building_id" not in table.columns:
        return table.copy()

    return table[
        table["building_id"] == selected_building
    ].copy()


filtered_room = filter_building(room)
filtered_base = filter_building(base)
filtered_extreme = filter_building(extreme)
filtered_unusual = filter_building(unusual)
filtered_missing = filter_building(missing)
filtered_priority = filter_building(priority)


st.sidebar.divider()

st.sidebar.info("""
**เกี่ยวกับ Dashboard**

ข้อมูลวิเคราะห์การใช้ไฟฟ้า
ของสถานศึกษา ประจำปี 2025
""")


# =====================================================
# 14. KPI ภาพรวมระบบ
# =====================================================

st.header("📊 ภาพรวมการใช้พลังงาน")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "พลังงานไฟฟ้ารวม",
    f"{total_energy:,.2f} kWh"
)

col2.metric(
    "พลังงานเฉลี่ย",
    f"{average_energy:,.2f} kWh"
)

col3.metric(
    "จำนวนอาคาร",
    f"{int(total_buildings)} อาคาร"
)

col4.metric(
    "จำนวนห้อง",
    f"{int(total_rooms)} ห้อง"
)


col5, col6, col7 = st.columns(3)

col5.metric(
    "Base Load รวม",
    f"{base_load_total:,.2f} kWh"
)

col6.metric(
    "สัดส่วน Base Load",
    f"{base_load_percent:.2f}%"
)

col7.metric(
    "พลังงานสูงสุด",
    f"{maximum_energy:,.2f} kWh"
)

st.divider()


# =====================================================
# 15. แนวโน้มการใช้ไฟฟ้ารายเดือน
# =====================================================

st.header("📈 แนวโน้มการใช้พลังงานรายเดือน")

fig_monthly = px.bar(
    monthly,
    x="month",
    y="total_energy_kwh",
    text_auto=".2s",
    title="พลังงานไฟฟ้ารวมรายเดือน",
    labels={
        "month": "เดือน",
        "total_energy_kwh": "พลังงาน (kWh)"
    },
    color_discrete_sequence=[
        "#38BDF8"
    ]
)

fig_monthly.update_layout(
    xaxis_title="เดือน",
    yaxis_title="พลังงาน (kWh)",
    showlegend=False,
    bargap=0.25
)

show_chart(fig_monthly, "monthly_chart")


# =====================================================
# 16. เปรียบเทียบการใช้พลังงานรายอาคาร
# =====================================================

st.header("🏢 เปรียบเทียบการใช้พลังงานรายอาคาร")

building_colors = [
    "#38BDF8",
    "#60A5FA",
    "#818CF8",
    "#FACC15",
    "#22D3EE"
]

fig_building = px.bar(
    building,
    x="building_id",
    y="total_energy_kwh",
    color="building_id",
    text_auto=".2s",
    title="พลังงานรวมแยกตามอาคาร",
    labels={
        "building_id": "อาคาร",
        "total_energy_kwh": "พลังงาน (kWh)"
    },
    color_discrete_sequence=building_colors
)

show_chart(fig_building, "building_chart")


fig_building_base = px.bar(
    building,
    x="building_id",
    y="base_load_share_percent",
    color="building_id",
    text_auto=".2f",
    title="สัดส่วน Base Load แยกตามอาคาร",
    labels={
        "building_id": "อาคาร",
        "base_load_share_percent": "Base Load (%)"
    },
    color_discrete_sequence=building_colors
)

show_chart(fig_building_base, "building_base_chart")


# =====================================================
# 17. จัดอันดับห้องที่ใช้ไฟสูง
# =====================================================

st.header("🚪 จัดอันดับห้องที่ใช้พลังงานสูง")

top_rooms = filtered_room.sort_values(
    "total_energy_kwh",
    ascending=False
).head(10)

fig_rooms = px.bar(
    top_rooms,
    x="room_id",
    y="total_energy_kwh",
    color="building_id",
    text_auto=".2s",
    title="10 อันดับห้องที่ใช้ไฟฟ้าสูงที่สุด",
    labels={
        "room_id": "ห้อง",
        "total_energy_kwh": "พลังงาน (kWh)",
        "building_id": "อาคาร"
    },
    color_discrete_sequence=building_colors
)

show_chart(fig_rooms, "top_rooms_chart")

show_table(top_rooms)


# =====================================================
# 18. วิเคราะห์ Base Load
# =====================================================

st.header("🔌 วิเคราะห์การใช้ไฟช่วงไม่มีผู้ใช้งาน")

top_base = filtered_base.sort_values(
    "base_load_share_percent",
    ascending=False
).head(10)

fig_base = px.bar(
    top_base,
    x="room_id",
    y="base_load_share_percent",
    color="building_id",
    text_auto=".2f",
    title="10 ห้องที่มีสัดส่วน Base Load สูงที่สุด",
    labels={
        "room_id": "ห้อง",
        "base_load_share_percent": "Base Load (%)",
        "building_id": "อาคาร"
    },
    color_discrete_sequence=building_colors
)

show_chart(fig_base, "top_base_chart")

show_table(top_base)


# =====================================================
# 19. ตรวจสอบค่าพลังงานสูงผิดปกติ
# =====================================================

st.header("⚠️ ตรวจสอบค่าพลังงานผิดปกติ")

st.subheader(
    "รายการที่ใช้ไฟเกิน 50 kWh ต่อชั่วโมง"
)

st.metric(
    "จำนวนรายการ",
    f"{len(filtered_extreme)} รายการ"
)

show_table(filtered_extreme)


st.subheader(
    "รายการผิดปกติด้วยวิธี IQR"
)

st.metric(
    "จำนวนรายการ",
    f"{len(filtered_unusual)} รายการ"
)

show_table(filtered_unusual)


# =====================================================
# 20. ตรวจสอบข้อมูลที่ขาดหาย
# =====================================================

st.header("🔍 ตรวจสอบข้อมูลมิเตอร์ที่ขาดหาย")

st.metric(
    "จำนวนช่วงเวลาที่ขาดหาย",
    f"{len(filtered_missing)} รายการ"
)

show_table(filtered_missing)


# =====================================================
# 21. จัดลำดับห้องที่ควรตรวจสอบ
# =====================================================

st.header("🎯 ห้องที่ควรให้ความสนใจในการตรวจสอบ")

st.caption("""
รายการนี้ใช้ประกอบการตัดสินใจตรวจสอบ
โดยพิจารณาจากพลังงานรวม Base Load และค่าผิดปกติ
ไม่ได้เป็นคะแนนความเสี่ยงที่ผ่านการรับรอง
""")

priority_display = filtered_priority.sort_values(
    "total_energy_kwh",
    ascending=False
)

show_table(priority_display)


# =====================================================
# 22. ตารางเปรียบเทียบอาคาร
# =====================================================

st.header("📋 สรุปข้อมูลการใช้พลังงานรายอาคาร")

show_table(building)


# =====================================================
# 23. ดาวน์โหลดข้อมูล
# =====================================================

st.header("📥 ดาวน์โหลดข้อมูล")

download_choice = st.selectbox(
    "เลือกตารางที่ต้องการดาวน์โหลด",
    [
        "monthly",
        "building",
        "room",
        "base",
        "extreme",
        "unusual",
        "missing",
        "priority"
    ]
)

download_names = {
    "monthly": "monthly_energy.csv",
    "building": "building_dashboard.csv",
    "room": "room_dashboard.csv",
    "base": "base_load_dashboard.csv",
    "extreme": "extreme_events.csv",
    "unusual": "unusual_dashboard.csv",
    "missing": "missing_dashboard.csv",
    "priority": "priority_dashboard.csv"
}

st.download_button(
    label="📥 ดาวน์โหลด CSV",
    data=data[download_choice].to_csv(
        index=False
    ).encode("utf-8-sig"),
    file_name=download_names[download_choice],
    mime="text/csv"
)


# =====================================================
# 24. ส่วนท้ายเว็บไซต์
# =====================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#BFDBFE;
    padding:20px;
">

⚡ <b>SMART ENERGY DASHBOARD</b>

<br><br>

ระบบวิเคราะห์และตรวจสอบพฤติกรรมการใช้พลังงานไฟฟ้า

<br>

ข้อมูลประจำปี 2025

<br>

จัดทำเพื่อสนับสนุนการลดต้นทุนพลังงานของสถานศึกษา

</div>
""", unsafe_allow_html=True)
