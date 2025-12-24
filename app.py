import streamlit as st
import pandas as pd
import math

# إعداد الصفحة وتجميلها
st.set_page_config(page_title="نظام اللجان", layout="wide")

# CSS متطور يعمل على الجوال ويخفي زوائد المنصة
st.markdown("""
    <style>
    /* إخفاء عناصر Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* ضبط الخطوط لتناسب الجوال */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Tajawal', sans-serif; 
        text-align: right; 
        direction: rtl; 
    }
    
    /* منع تداخل النصوص في الجوال */
    .main .block-container { padding: 1rem; }
    
    /* تصميم البطاقات بشكل مرن */
    .metric-card {
        background: white; padding: 15px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-right: 4px solid #1e3a8a; margin-bottom: 10px;
    }

    /* تنسيق الطباعة (يبقى ثابتاً لورق A4) */
    @media print {
        .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .label-container { 
            display: grid; grid-template-columns: repeat(3, 70mm); 
            grid-template-rows: repeat(7, 42.3mm); 
        }
        .label-box {
            width: 70mm; height: 42.3mm; border: 0.1mm solid #eee;
            display: flex; flex-direction: column; justify-content: center;
            align-items: center; text-align: center; box-sizing: border-box;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# لوحة التحكم
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    school = st.text_input("اسم المدرسة", "المدرسة")
    dept = st.text_input("الإدارة", "تعليم ...")
    st.divider()
    c_size = st.number_input("سعة اللجنة", value=20)
    s_no = st.number_input("أرقام الجلوس تبدأ من", value=100)
    font_size = st.slider("حجم خط الاسم", 10, 20, 13)

# الواجهة الرئيسية
st.markdown(f"<h2 style='text-align: center; color: #1e3a8a;'>📑 نظام لجان الاختبارات</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{school}</p>", unsafe_allow_html=True)

file = st.file_uploader("ارفع ملف اكسل نور", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    df['رقم الجلوس'] = range(s_no, s_no + len(df))
    
    # بطاقات بسيطة لا تسبب تداخل في الجوال
    st.markdown(f"""
    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        <div class="metric-card" style="flex: 1; min-width: 120px;">طلاب: {len(df)}</div>
        <div class="metric-card" style="flex: 1; min-width: 120px;">لجان: {math.ceil(len(df)/c_size)}</div>
    </div>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["📋 الكشوف", "🏷️ الملصقات"])

    with t1:
        st.button("🖨️ طباعة الكشوف", on_click=None, help="استخدم Ctrl+P")
        for i in range(0, len(df), c_size):
            chunk = df.iloc[i:i+c_size]
            st.markdown(f"""
            <div style="padding: 10px; border: 1px solid #eee; margin-bottom: 20px; background: white;">
                <h4 style="text-align:center;">كشف لجنة {int(i/c_size)+1}</h4>
                <table style="width:100%; border-collapse:collapse; text-align:center;" border="1">
                    <tr style="background:#f8f9fa;"><th>م</th><th>الاسم</th><th>الجلوس</th></tr>
                    {"".join([f"<tr><td>{idx+1}</td><td>{r.iloc[0]}</td><td>{r['رقم الجلوس']}</td></tr>" for idx, r in chunk.iterrows()])}
                </table>
            </div>
            """, unsafe_allow_html=True)

    with t2:
        st.info("الطباعة مخصصة لورق فورماتك (3 أعمدة × 7 صفوف)")
        for p in range(0, len(df), 21):
            page = df.iloc[p:p+21]
            st.markdown('<div class="label-container">', unsafe_allow_html=True)
            for idx, r in page.iterrows():
                st.markdown(f"""
                <div class="label-box">
                    <div style="font-size: {font_size}pt; font-weight: bold;">{r.iloc[0]}</div>
                    <div style="font-size: 10pt;">رقم الجلوس: {r["رقم الجلوس"]}</div>
                    <div style="font-size: 9pt;">اللجنة: {int(idx/c_size)+1}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
