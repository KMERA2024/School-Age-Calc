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

st.title("🔢 حاسبة العمر وتحديد الصف الدراسي")

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

# زر الحساب
if st.button("احسب عمر الطالب وتحديد الصف"):
    if birth_date_final:
        delta = START_DATE - birth_date_final
        years = delta.days // 365
        months = (delta.days % 365) // 30
        
        # إظهار العمر
        st.markdown(f"""
            <div style="background-color: #f0f7fa; padding: 15px; border-radius: 10px; border-right: 5px solid #004a99; text-align: right; margin-bottom: 20px;">
                <p style="color: #004a99; font-size: 20px; margin: 0;">عمر الطالب هو: <b>{years} سنة و {months} شهر</b></p>
            </div>
        """, unsafe_allow_html=True)

        # منطق تحديد الصف الدراسي (بناءً على جدول الوزارة)
        total_months = (years * 12) + months
        suggested_grade = ""
        status_color = "info"

        if total_months < 69:
            suggested_grade = "دون سن القبول النظامي"
            st.error(f"⚠️ النتيجة: {suggested_grade}")
        elif 69 <= total_months < 72:
            suggested_grade = "الأول ابتدائي (بشرط شهادة روضة معتمدة)"
            st.warning(f"✅ النتيجة: {suggested_grade}")
        elif 72 <= total_months < 84:
            suggested_grade = "الصف الأول الابتدائي (مستجد)"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 84 <= total_months < 96:
            suggested_grade = "الصف الثاني الابتدائي"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 96 <= total_months < 108:
            suggested_grade = "الصف الثالث الابتدائي"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 108 <= total_months < 120:
            suggested_grade = "الصف الرابع الابتدائي"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 120 <= total_months < 132:
            suggested_grade = "الصف الخامس الابتدائي"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 132 <= total_months < 144:
            suggested_grade = "الصف السادس الابتدائي"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 144 <= total_months < 156:
            suggested_grade = "الصف الأول المتوسط"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 156 <= total_months < 168:
            suggested_grade = "الصف الثاني المتوسط"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 168 <= total_months < 180:
            suggested_grade = "الصف الثالث المتوسط"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 180 <= total_months < 192:
            suggested_grade = "الصف الأول الثانوي"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 192 <= total_months < 204:
            suggested_grade = "الصف الثاني الثانوي"
            st.success(f"✅ النتيجة: {suggested_grade}")
        elif 204 <= total_months <= 216:
            suggested_grade = "الصف الثالث الثانوي"
            st.success(f"✅ النتيجة: {suggested_grade}")
        else:
            suggested_grade = "يتجاوز السن النظامي (يوجه لتعليم الكبار/ليلي)"
            st.info(f"ℹ️ النتيجة: {suggested_grade}")

# التوقيع
st.markdown("""<div class="footer">تصميم وتطوير: أ. خالد محمد الحربي © 2026</div>""", unsafe_allow_html=True)