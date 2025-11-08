import streamlit as st
import pandas as pd
import os
from datetime import datetime
import streamlit as st

# ตั้งค่า PWA
st.set_page_config(
    page_title="พอร์ตส่วนตัว",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# เพิ่ม meta tags สำหรับ PWA
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="การเงิน">
""", unsafe_allow_html=True)

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="พอร์ตส่วนตัว", page_icon="💰", layout="wide")

# หัวเรื่อง
st.title("💰 พอร์ตส่วนตัว")
st.write("เวอร์ชันง่ายสุดสำหรับมือใหม่")

# ชื่อไฟล์สำหรับบันทึก
DATA_FILE = "asset.csv"

# โหลดข้อมูลจากไฟล์ (ถ้ามี)
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.session_state.asset = df.to_dict('records')
else:
    if 'asset' not in st.session_state:
        st.session_state.asset = [
            {"วันที่": "2025-10-31", "สินทรัพย์": "SPX", "เครื่องมือ": "VOO", "จำนวน": 1006719.31},
            {"วันที่": "2025-10-31", "สินทรัพย์": "SPX", "เครื่องมือ": "KKP US500-UH", "จำนวน": 2042936.00},
            {"วันที่": "2025-10-31", "สินทรัพย์": "NDQ", "เครื่องมือ": "QQQM", "จำนวน": 800608.20},
            {"วันที่": "2025-10-31", "สินทรัพย์": "NDQ", "เครื่องมือ": "KKP NDQ100-UH", "จำนวน": 1691686.70},
            {"วันที่": "2025-10-31", "สินทรัพย์": "USD", "เครื่องมือ": "Cash", "จำนวน": 1431398.55},
        ]

# แปลงเป็น DataFrame
df = pd.DataFrame(st.session_state.asset)

# คำนวณสรุป
total_spx = df[df['สินทรัพย์'] == 'SPX']['จำนวน'].sum()
total_ndq = df[df['สินทรัพย์'] == 'NDQ']['จำนวน'].sum()
total_gld = df[df['สินทรัพย์'] == 'GLD']['จำนวน'].sum()
total_usd = df[df['สินทรัพย์'] == 'USD']['จำนวน'].sum()
balance = total_spx + total_ndq + total_gld + total_usd

# แสดงสรุป
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("💙 SPX", f"฿{total_spx:,.2f}")
with col2:
    st.metric("❤️ NDQ", f"฿{total_ndq:,.2f}")
with col3:
    st.metric("💛 GLD", f"฿{total_gld:,.2f}")
with col4:
    st.metric("💚 USD", f"฿{total_usd:,.2f}")
with col5:
    st.metric("💰 Total", f"฿{balance:,.2f}")

# แสดงกราฟ
st.subheader("📈 กราฟสรุปสินทรัพย์")
col1, col2= st.columns(2)
with col1:
    # กรองเฉพาะสินทรัพย์
    asset_df = df[df['สินทรัพย์'] != '']

    if not asset_df.empty:
    # จัดกลุ่มตามสินทรัพย์
        asset_by_category = asset_df.groupby('สินทรัพย์')['จำนวน'].sum().reset_index()
    
    # สร้างกราฟ Pie Chart
        import plotly.express as px
        fig = px.pie(
            asset_by_category, 
            values='จำนวน', 
            names='สินทรัพย์',
            title='สัดส่วนสินทรัพย์',
            color_discrete_sequence=["#0070c0", "#d80000", "#ffab25", "#00a100"]
            #color_discrete_sequence=['#1f77b4', '#d62728', '#ff7f0e', '#2ca02c']

    )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ยังไม่มีข้อมูลสินทรัพย์")

with col2:
    # กรองเฉพาะเครื่องมือ
    asset_df = df[df['เครื่องมือ'] != '']

    if not asset_df.empty:
        # จัดกลุ่มตามเครื่องมือ
        asset_by_category = asset_df.groupby('เครื่องมือ')['จำนวน'].sum().reset_index()
    
        # สร้างกราฟ Pie Chart
        import plotly.express as px
        fig = px.pie(
            asset_by_category, 
            values='จำนวน', 
            names='เครื่องมือ',
            title='สัดส่วนเครื่องมือ',
            color_discrete_sequence=px.colors.qualitative.Set2
            #color_discrete_sequence=px.colors.qualitative.Pastel

        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ยังไม่มีข้อมูลเครื่องมือ")

# แสดงตาราง
st.subheader("📊 ประวัติรายการทั้งหมด")

for index, row in df.iterrows():
    col1, col2 = st.columns([9, 1])
    
    with col1:
        if row['สินทรัพย์'] == 'SPX':
            if row['จำนวน'] > 0:
                st.success(f"📅 {row['วันที่']} | 💙 {row['เครื่องมือ']} | ฿{row['จำนวน']:,.2f}")
            else:
                st.error(f"📅 {row['วันที่']} | 💙 {row['เครื่องมือ']} | ฿{row['จำนวน']:,.2f}")
        elif row['สินทรัพย์'] == 'NDQ':
            if row['จำนวน'] > 0:
                st.success(f"📅 {row['วันที่']} | ❤️ {row['เครื่องมือ']} | ฿{row['จำนวน']:,.2f}")
            else:
                st.error(f"📅 {row['วันที่']} | ❤️ {row['เครื่องมือ']} | ฿{row['จำนวน']:,.2f}")
        elif row['สินทรัพย์'] == 'GLD':
            if row['จำนวน'] > 0:
                st.success(f"📅 {row['วันที่']} | 💛 {row['เครื่องมือ']} | ฿{row['จำนวน']:,.2f}")
            else:
                st.error(f"📅 {row['วันที่']} | 💛 {row['เครื่องมือ']} | ฿{row['จำนวน']:,.2f}")
        else:
            if row['จำนวน'] > 0:
                st.success(f"📅 {row['วันที่']} | 💚 {row['เครื่องมือ']} | ฿{row['จำนวน']:,.2f}")
            else:
                st.error(f"📅 {row['วันที่']} | 💚 {row['เครื่องมือ']} | ฿{row['จำนวน']:,.2f}")
    
    with col2:
        if st.button("🗑️", key=f"delete_{index}"):
            # เก็บ index ที่จะลบใน session_state
            st.session_state.confirm_delete = index
            st.rerun()

# ถ้ามีการขอลบ แสดงข้อความยืนยัน
if 'confirm_delete' in st.session_state:
    index_to_delete = st.session_state.confirm_delete
    row_to_delete = df.iloc[index_to_delete]
    
    st.warning(f"⚠️ คุณแน่ใจหรือไม่ที่จะลบ: {row_to_delete['เครื่องมือ']} ฿{row_to_delete['จำนวน']:,.2f}?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ ยืนยันลบ", type="primary"):
            # ลบจริง
            st.session_state.asset.pop(index_to_delete)
            df_updated = pd.DataFrame(st.session_state.asset)
            df_updated.to_csv("asset.csv", index=False, encoding='utf-8-sig')
            
            # ลบ flag ยืนยัน
            del st.session_state.confirm_delete
            st.success("✅ ลบสำเร็จ!")
            st.rerun()
    
    with col2:
        if st.button("❌ ยกเลิก"):
            del st.session_state.confirm_delete
            st.rerun()

# ฟอร์มเพิ่มรายการ
st.subheader("➕ เพิ่มรายการใหม่")
col1, col2, col3, col4 = st.columns(4)

with col1:
    date = st.date_input("วันที่", datetime.today())
with col2:
    trans_type = st.selectbox("สินทรัพย์", ["SPX", "NDQ", "GLD", "USD"])
with col3:
    category = st.text_input("เครื่องมือ", value=None, placeholder="VOO, QQQM, etc.")
with col4:
    amount = st.number_input("จำนวนเงิน", value=None, placeholder="Type a number...")

if st.button("บันทึก", type="primary"):
    new_transaction = {
        "วันที่": date.strftime("%Y-%m-%d"),
        "สินทรัพย์": trans_type,
        "เครื่องมือ": category,
        "จำนวน": amount
    }
    st.session_state.asset.append(new_transaction)

    
    # บันทึกลงไฟล์
    df = pd.DataFrame(st.session_state.asset)
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

    # เก็บสถานะว่าเพิ่งบันทึกเสร็จ
    st.session_state.just_saved = True
    st.rerun()

# แสดงข้อความและลูกโป่งหลังรีเฟรช
if 'just_saved' in st.session_state and st.session_state.just_saved:
    st.success("✅ บันทึกสำเร็จ!")
    st.balloons()
    st.session_state.just_saved = False  # รีเซ็ตสถานะ
