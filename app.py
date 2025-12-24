import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة الأساسية لمنع التداخل في الجوال
st.set_page_config(page_title="نظام اللجان", layout="wide", initial_sidebar_state="collapsed")

# 2. كود CSS "قوي" لإعادة ضبط الواجهة للجوال تماماً ومنع التداخل
st.markdown("""
    <style>
    /* إخفاء شعارات المنصة تماماً */
    #MainMenu, footer, header, .stDeployButton {display:none; visibility: hidden;}
    
    /* إلغاء حواف Streamlit التي تسبب ضغط التصميم وتداخل الكلمات */
    .block-container { padding: 0 !important; max-width: 100% !important; }
    
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Tajawal', sans-serif; 
        direction: rtl; 
        text-align: right; 
        background-color: #f8f9fa; 
    }

    /* الهيدر العلوي المتدرج مثل صورة مدرستي تماماً */
    .custom-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; padding: 45px 20px;
        border-radius: 0 0 45px 45px;
        text-align: center; margin-bottom: 25px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }

    /* حاوية البطاقات (Grid) تظهر 2 في كل صف بالجوال بشكل مرتب */
    .grid-wrapper {
        display: grid; 
        grid-template-columns: repeat(2, 1fr); 
        gap: 15px; padding: 0 15px;
        margin-bottom: 25px;
    }

    .stat-card {
        background: white; border-radius: 20px; padding: 20px;
        text-align: center; box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        border-bottom: 5px solid #3b82f6;
    }

    .icon-box { font-size: 32px; margin-bottom: 8px; }

    /* تحسين شكل الجدول لمنع خروجه عن حدود الشاشة */
    .stTable { width: 100% !important; border-radius: 15px; overflow: hidden; }
    
    /* تنسيق الطباعة (يبقى ثابتاً لورق A4) */
    @media print {
        .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .label-grid { display: grid; grid-template-columns: repeat(3, 70mm); grid-template-rows: repeat(7, 42.3mm); }
        .label-box { width: 70mm; height: 42.3mm; border: 0.1mm solid #eee; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة البرنامج العلوية (Header)
st.markdown(f"""
    <div class="custom-header">
        <h2 style="margin:0; font-size: 24px;">نظام إدارة اللجان الذكي</h2>
        <p style="margin:8px 0 0 0; opacity:0.9; font-size: 15px;">متوسطة وثانوية ...</p>
    </div>
    """, unsafe_allow_html=True)

# 4. منطقة رفع الملف (تصميم نظيف)
st.markdown("<div style='padding:0 20px;'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📂 ارفع ملف الطلاب (Excel)", type=["xlsx"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df['رقم الجلوس'] = range(101, 101 + len(df)) # بداية تلقائية لأرقام الجلوس
    
    # 5. عرض البطاقات (2 في كل صف) كما في تصميمك المفضل
    st.markdown(f"""
    <div class="grid-wrapper no-print">
        <div class="stat-card">
            <div class="icon-box">👥</div>
            <div style="font-size:13px; color:#666;">إجمالي الطلاب</div>
            <div style="font-size:22px; font-weight:bold; color:#1e3a8a;">{len(df)}</div>
        </div>
        <div class="stat-card">
            <div class="icon-box">🏫</div>
            <div style="font-size:13px; color:#666;">عدد اللجان</div>
            <div style="font-size:22px; font-weight:bold; color:#10b981;">{math.ceil(len(df)/20)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. التبويبات (Tabs) لتقليل الزحمة في الجوال
    st.markdown("<div style='padding: 0 20px;'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📋 الكشوفات", "🏷️ الملصقات"])

    with tab1:
        st.markdown("### 📍 معاينة اللجان")
        for i in range(0, len(df), 20):
            chunk = df.iloc[i:i+20]
            with st.expander(f"اللجنة رقم {int(i/20)+1}"):
                # عرض اسم الطالب والسجل فقط للتبسيط في الجوال
                st.table(chunk.iloc[:, [0, 1]].rename(columns={chunk.columns[0]: 'الاسم', chunk.columns[1]: 'السجل'}))

    with tab2:
        st.info("الملصقات مصممة لورق A4 (3x7)")
        if st.button("🖨️ بدء تجهيز الملصقات للطباعة"):
            for p in range(0, len(df), 21):
                page = df.iloc[p:p+21]
                st.markdown('<div class="label-grid">', unsafe_allow_html=True)
                for idx, r in page.iterrows():
                    st.markdown(f"""
                    <div class="label-box">
                        <div style="font-size: 8pt; color: #888;">مدرسة ...</div>
                        <div style="font-size: 11pt; font-weight: bold;">{r.iloc[0]}</div>
                        <div style="font-size: 10pt; color: #1e3a8a;">جلوس: {r["رقم الجلوس"]}</div>
                        <div style="font-size: 9pt;">لجنة: {int(idx/20)+1}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # رسالة الترحيب بتصميم هادئ
    st.markdown("""
    <div style="margin:20px; padding:40px; background:white; border-radius:25px; text-align:center; border:1px solid #eee; color:#999;">
        <p>يرجى رفع ملف Excel من نظام نور للبدء</p>
    </div>
    """, unsafe_allow_html=True)
