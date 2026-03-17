import streamlit as st
from datetime import date
from hijri_converter import Hijri

# إعدادات الهوية البصرية (أزرق وأبيض)
st.set_page_config(page_title="حاسبة القبول المدرسي 2026", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #004a99; text-align: right; }
    .stButton>button { background-color: #004a99; color: white; width: 100%; }
    .main { text-align: right; direction: rtl; }
    label { color: #004a99 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📑 حاسبة معايير القبول والسن النظامي")
st.subheader("إدارة الاختبارات والقبول - العام الدراسي 2026")

# تاريخ بداية العام الدراسي
START_DATE = date(2026, 8, 24)

# واجهة المدخلات
calendar_type = st.radio("نوع التقويم المدخل:", ("هجري", "ميلادي"), horizontal=True)

birth_date_final = None

if calendar_type == "هجري":
    col1, col2, col3 = st.columns(3)
    with col1: day = st.number_input("اليوم", 1, 30, 1)
    with col2: month = st.number_input("الشهر", 1, 12, 1)
    with col3: year = st.number_input("السنة", 1430, 1448, 1442)
    try:
        birth_date_final = Hijri(year, month, day).to_gregorian()
    except:
        st.error("التاريخ الهجري غير دقيق، تأكد من عدد أيام الشهر.")
else:
    birth_date_final = st.date_input("اختر تاريخ الميلاد:", value=date(2020, 1, 1))

if st.button("تحليل الأهلية والصف الدراسي"):
    if birth_date_final:
        # حساب العمر
        delta = START_DATE - birth_date_final
        years = delta.days // 365
        months = (delta.days % 365) // 30
        
        st.info(f"عمر الطالب عند بداية الدراسة: {years} سنة و {months} شهر")

        # منطق التسكين (بناءً على صورتك المرفقة)
        if years < 5 or (years == 5 and months < 9):
            st.error("❌ دون سن القبول (أصغر من 6 سنوات بـ 90 يوم)")
        elif years == 5 and months >= 9:
            st.success("✅ يقبل في الصف **الأول الابتدائي** (بشرط شهادة روضة معتمدة)")
        elif years == 6:
            st.success("✅ يقبل في الصف **الأول الابتدائي**")
        elif years == 7:
            st.success("✅ يقبل في الصف **الثاني الابتدائي**")
        elif 12 <= years <= 14:
            st.success(f"✅ يقبل في المرحلة المتوسطة - الصف {years-11} متوسط")
        else:
            st.warning("⚠️ يرجى مراجعة جدول التعادل للأعمار الكبيرة.")

st.write("---")
st.caption("برمجة أتمتة تعليمية - 2026")