import streamlit as st
from datetime import date
from hijri_converter import Hijri

# إعدادات الهوية البصرية والتنسيق
st.set_page_config(page_title="حاسبة القبول - أ. خالد الحربي", layout="centered")

st.markdown("""
    <style>
    /* تنسيق الخلفية والعناصر */
    .stApp { background-color: #ffffff; }
    .main { text-align: right; direction: rtl; }
    
    /* تنسيق العناوين */
    h1 { color: #004a99; text-align: center; font-family: 'Arial'; border-bottom: 2px solid #00a8e8; padding-bottom: 10px; }
    h3 { color: #004a99; text-align: right; }
    
    /* تنسيق الزر */
    .stButton>button {
        background-color: #004a99;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 3em;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #003366; color: #00a8e8; }

    /* التذييل الخاص بالأستاذ خالد */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #004a99;
        color: white;
        text-align: center;
        padding: 8px;
        font-size: 14px;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_index=True)

st.title("🏫 حاسبة القبول والسن النظامي")
st.write("<p style='text-align: center; color: #555;'>وزارة التعليم - إدارة الاختبارات والقبول بمكة المكرمة</p>", unsafe_allow_index=True)

# تاريخ المرجع
START_DATE = date(2026, 8, 24)

# واجهة المدخلات
with st.container():
    st.markdown("### 🗓️ إدخال بيانات الميلاد")
    cal_type = st.radio("نوع التقويم:", ("هجري", "ميلادي"), horizontal=True)
    
    birth_date = None
    if cal_type == "هجري":
        c1, c2, c3 = st.columns(3)
        with c1: d = st.number_input("اليوم", 1, 30, 1)
        with c2: m = st.number_input("الشهر", 1, 12, 1)
        with c3: y = st.number_input("السنة", 1430, 1448, 1442)
        try:
            birth_date = Hijri(y, m, d).to_gregorian()
        except:
            st.error("التاريخ الهجري غير صحيح")
    else:
        birth_date = st.date_input("اختر التاريخ:", value=date(2020, 1, 1))

if st.button("تحليل الأهلية"):
    if birth_date:
        diff = START_DATE - birth_date
        years = diff.days // 365
        months = (diff.days % 365) // 30
        
        st.info(f"عمر الطالب في بداية العام: {years} سنة و {months} شهر")

        # منطق القبول (مبني على الجدول الورقي)
        if years < 5 or (years == 5 and months < 9):
            st.error("❌ دون سن القبول")
        elif years == 5 and months >= 9:
            st.warning("✅ يُقبل في الأول ابتدائي (بشرط شهادة روضة)")
        elif 6 <= years <= 11:
            st.success(f"✅ الصف المستحق: الابتدائي (العمر {years})")
        elif 12 <= years <= 14:
            st.success(f"✅ الصف المستحق: المتوسط")
        elif 15 <= years <= 18:
            st.success(f"✅ الصف المستحق: الثانوي")
        else:
            st.warning("⚠️ يتجاوز السن النظامي")

# التوقيع
st.markdown("""<div class="footer">تصميم وتطوير: أ. خالد محمد الحربي © 2026</div>""", unsafe_allow_index=True)