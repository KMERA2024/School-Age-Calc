import streamlit as st
from datetime import date
from hijri_converter import Hijri

# إعدادات الصفحة
st.set_page_config(page_title="حاسبة العمر - أ. خالد الحربي", layout="centered")

# التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main { text-align: right; direction: rtl; }
    h1 { color: #004a99; text-align: center; border-bottom: 3px solid #00a8e8; padding-bottom: 10px; }
    .stButton>button {
        background-color: #004a99;
        color: white;
        border-radius: 10px;
        width: 100%;
        height: 3.5em;
        font-size: 18px;
        font-weight: bold;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #004a99;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 16px;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي الجديد
st.title("🔢 حاسبة العمر والسن النظامي")

# تاريخ المرجع لبداية العام الدراسي 2026
START_DATE = date(2026, 8, 24)

# واجهة المدخلات
calendar_type = st.radio("اختر نوع التقويم:", ("هجري", "ميلادي"), horizontal=True)

birth_date_final = None

if calendar_type == "هجري":
    col1, col2, col3 = st.columns(3)
    with col1: day = st.number_input("اليوم", 1, 30, 1)
    with col2: month = st.number_input("الشهر", 1, 12, 1)
    with col3: year = st.number_input("السنة", 1430, 1448, 1442)
    try:
        birth_date_final = Hijri(year, month, day).to_gregorian()
    except:
        st.error("يرجى التأكد من صحة التاريخ الهجري المدخل")
else:
    birth_date_final = st.date_input("تاريخ الميلاد الميلادي:", value=date(2020, 1, 1))

# زر الحساب المحدث
if st.button("احسب عمر الطالب"):
    if birth_date_final:
        delta = START_DATE - birth_date_final
        years = delta.days // 365
        months = (delta.days % 365) // 30
        
        st.markdown(f"""
            <div style="background-color: #f0f7fa; padding: 20px; border-radius: 10px; border-right: 5px solid #004a99; text-align: right;">
                <p style="color: #004a99; font-size: 20px; margin: 0;">عمر الطالب هو: <b>{years} سنة و {months} شهر</b></p>
                <p style="color: #555; font-size: 14px; margin-top: 10px;">(محسوب حتى تاريخ بداية العام الدراسي 2026/08/24م)</p>
            </div>
        """, unsafe_allow_html=True)

        # رسالة توضيحية بناءً على العمر
        if years < 5 or (years == 5 and months < 9):
            st.warning("تنبيه: الطالب دون سن القبول النظامي (أقل من 6 سنوات بـ 90 يوماً)")
        elif years >= 6:
            st.success("الطالب ضمن السن النظامي للقبول")

# التوقيع في أسفل الصفحة
st.markdown("""
    <div class="footer">
        تصميم وتطوير: أ. خالد محمد الحربي © 2026
    </div>
    """, unsafe_allow_html=True)