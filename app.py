import streamlit as st
from datetime import date
from hijri_converter import Hijri

# إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="حاسبة القبول المدرسي 2026", layout="centered")

# تصميم الواجهة باستخدام CSS
st.markdown("""
    <style>
    /* تنسيق الخلفية العامة */
    .stApp {
        background: linear-gradient(to bottom, #f0f4f8, #ffffff);
    }
    
    /* تنسيق العناوين */
    h1 {
        color: #004a99;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border-bottom: 3px solid #00a8e8;
        padding-bottom: 10px;
    }
    
    /* تنسيق الحاوية الرئيسية */
    .main {
        text-align: right;
        direction: rtl;
    }
    
    /* تنسيق الأزرار */
    .stButton>button {
        background-color: #004a99;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #003366;
        border: 1px solid #00a8e8;
    }

    /* التذييل (توقيع أ. خالد) */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #004a99;
        color: white;
        text-align: center;
        padding: 10px;
        font-family: 'Arial';
        font-size: 16px;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_index=True)

# محتوى الصفحة
st.title("🏫 حاسبة معايير القبول والسن النظامي")
st.write("<p style='text-align: center; color: #666;'>إدارة الاختبارات والقبول - منطقة مكة المكرمة</p>", unsafe_allow_index=True)

# تاريخ بداية العام الدراسي
START_DATE = date(2026, 8, 24)

# واجهة الإدخال
with st.container():
    st.markdown("### 🗓️ إدخال بيانات الطالب")
    calendar_type = st.radio("نوع التقويم:", ("هجري", "ميلادي"), horizontal=True)
    
    birth_date_final = None

    if calendar_type == "هجري":
        col1, col2, col3 = st.columns(3)
        with col1: day = st.number_input("اليوم", 1, 30, 1)
        with col2: month = st.number_input("الشهر", 1, 12, 1)
        with col3: year = st.number_input("السنة", 1430, 1448, 1442)
        try:
            birth_date_final = Hijri(year, month, day).to_gregorian()
        except:
            st.error("التاريخ الهجري غير دقيق")
    else:
        birth_date_final = st.date_input("تاريخ الميلاد الميلادي:", value=date(2020, 1, 1))

# زر الحساب
if st.button("تحليل الأهلية وتحديد الصف"):
    if birth_date_final:
        delta = START_DATE - birth_date_final
        years = delta.days // 365
        months = (delta.days % 365) // 30
        
        st.markdown(f"""
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 15px; border-right: 5px solid #004a99; text-align: right;">
            <h4 style="color: #004a99;">نتائج التحليل:</h4>
            <p style="font-size: 18px;">عمر الطالب: <b>{years} سنة و {months} شهر</b></p>
        </div>
        """, unsafe_allow_index=True)

        # منطق القبول المبسط
        if years < 5 or (years == 5 and months < 9):
            st.error("❌ دون سن القبول النظامي")
        elif years == 5 and months >= 9:
            st.warning("✅ يُقبل في (الأول ابتدائي) بشرط شهادة روضة معتمدة")
        elif 6 <= years <= 18:
            st.success(f"✅ الصف المستحق: بناءً على جدول التعادل (العمر {years} سنة)")
        else:
            st.info("⚠️ يوجه لتعليم الكبار")

# إضافة التوقيع في الأسفل
st.markdown("""
    <div class="footer">
        تصميم وتطوير: أ. خالد محمد الحربي © 2026
    </div>
    """, unsafe_allow_index=True)