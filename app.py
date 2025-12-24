import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="نظام اللجان الذكي", layout="wide", initial_sidebar_state="collapsed")

# 2. كود CSS لبناء البطاقات والأيقونات (Mobile Responsive)
st.markdown("""
    <style>
    /* إخفاء الزوائد */
    #MainMenu, footer, header, .stDeployButton {display:none; visibility: hidden;}
    .block-container { padding: 0 !important; max-width: 100% !important; }
    
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; background-color: #f0f4f8; }

    /* الهيدر العلوي */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; padding: 40px 20px; text-align: center;
        border-radius: 0 0 35px 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* حاوية الأيقونات (2 في كل صف للجوال) */
    .icon-grid {
        display: grid; grid-template-columns: repeat(2, 1fr);
        gap: 15px; padding: 20px;
    }

    .menu-card {
        background: white; border-radius: 20px; padding: 20px;
        text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-bottom: 4px solid #3b82f6; cursor: pointer;
        transition: 0.3s; height: 140px; display: flex;
        flex-direction: column; justify-content: center; align-items: center;
    }
    
    .card-icon { font-size: 35px; margin-bottom: 10px; }
    .card-title { font-size: 14px; font-weight: bold; color: #333; }
    .card-desc { font-size: 10px; color: #888; margin-top: 5px; }

    /* تنسيق الطباعة */
    @media print {
        .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .label-grid { display: grid; grid-template-columns: repeat(3, 70mm); grid-template-rows: repeat(7, 42.3mm); }
        .label-box { width: 70mm; height: 42.3mm; border: 0.1mm solid #eee; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة التنقل بين الصفحات داخل التطبيق
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'data' not in st.session_state:
    st.session_state.data = None

# الهيدر العلوي ثابت
st.markdown(f"""
    <div class="main-header">
        <h2 style="margin:0;">نظام الاختبارات الذكي</h2>
        <p style="margin:5px 0 0 0; opacity:0.8;">لوحة التحكم الشاملة للمدرسة</p>
    </div>
    """, unsafe_allow_html=True)

# الصفحة الرئيسية (الشبكة الأيقونية)
if st.session_state.page == 'main':
    st.markdown('<div class="icon-grid">', unsafe_allow_html=True)
    
    # تعريف البطاقات
    menu_items = [
        {"id": "upload", "icon": "📁", "title": "رفع البيانات", "desc": "استيراد ملف نور"},
        {"id": "settings", "icon": "⚙️", "title": "الإعدادات", "desc": "تنسيق اللجان والخط"},
        {"id": "lists", "icon": "📋", "title": "كشوف المناداة", "desc": "قوائم التحضير"},
        {"id": "labels", "icon": "🏷️", "title": "ملصقات الطاولات", "desc": "استيكرات الجلوس"},
        {"id": "control", "icon": "📂", "title": "نماذج الكنترول", "desc": "محاضر الفتح والغلق"},
        {"id": "stats", "icon": "📊", "title": "الإحصائيات", "desc": "بيانات الطلاب واللجان"}
    ]

    # عرض البطاقات كأزرار Streamlit بستايل مخصص
    cols = st.columns(2)
    for idx, item in enumerate(menu_items):
        with cols[idx % 2]:
            if st.button(f"{item['icon']}\n\n{item['title']}", key=item['id'], use_container_width=True):
                st.session_state.page = item['id']
                st.rerun()

# --- صفحات الوظائف ---

# صفحة رفع الملف
if st.session_state.page == 'upload':
    if st.button("⬅️ العودة للرئيسية"):
        st.session_state.page = 'main'
        st.rerun()
    st.subheader("📁 رفع ملف الطلاب")
    file = st.file_uploader("اختر ملف Excel", type=["xlsx"])
    if file:
        st.session_state.data = pd.read_excel(file)
        st.success("تم رفع البيانات بنجاح!")

# صفحة الإعدادات
if st.session_state.page == 'settings':
    if st.button("⬅️ العودة"):
        st.session_state.page = 'main'
        st.rerun()
    st.subheader("⚙️ إعدادات التنسيق")
    school_name = st.text_input("اسم المدرسة", "مدرسة ...")
    c_size = st.number_input("سعة اللجنة", value=20)
    font_size = st.slider("حجم الخط في الملصقات", 10, 20, 13)
    st.info("سيتم تطبيق هذه الإعدادات على جميع المطبوعات")

# صفحة الكشوف
if st.session_state.page == 'lists':
    if st.button("⬅️ العودة"):
        st.session_state.page = 'main'
        st.rerun()
    if st.session_state.data is not None:
        st.subheader("📋 كشوف المناداة")
        df = st.session_state.data
        for i in range(0, len(df), 20):
            st.write(f"اللجنة رقم {int(i/20)+1}")
            st.table(df.iloc[i:i+20, [0, 1]])
    else:
        st.warning("يرجى رفع ملف البيانات أولاً من أيقونة 'رفع البيانات'")

# صفحة الملصقات
if st.session_state.page == 'labels':
    if st.button("⬅️ العودة"):
        st.session_state.page = 'main'
        st.rerun()
    if st.session_state.data is not None:
        st.subheader("🏷️ ملصقات الطاولات")
        if st.button("🖨️ عرض بصيغة الطباعة"):
            df = st.session_state.data
            for p in range(0, len(df), 21):
                page = df.iloc[p:p+21]
                st.markdown('<div class="label-grid">', unsafe_allow_html=True)
                for idx, r in page.iterrows():
                    st.markdown(f'<div class="label-box"><b>{r.iloc[0]}</b><br>جلوس: {100+idx}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("يرجى رفع ملف البيانات أولاً")
