import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="نظام الاختبارات الذكي", layout="wide")

# 2. هندسة الواجهة الاحترافية (Custom CSS)
st.markdown("""
    <style>
    /* إخفاء هوية المنصة بالكامل */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display:none;}
    
    /* استدعاء خطوط احترافية */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    /* التصميم العام */
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; background-color: #f0f2f6; }
    
    /* تصميم البطاقات العصرية */
    .dashboard-card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #1e3a8a;
        margin-bottom: 15px; transition: 0.3s;
    }
    
    /* تحسين شكل الجداول في الجوال */
    .stTable { background: white; border-radius: 10px; overflow: hidden; }
    
    /* تنسيق الطباعة (منفصل تماماً عن العرض) */
    @media print {
        .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .label-grid { 
            display: grid; grid-template-columns: repeat(3, 70mm); 
            grid-template-rows: repeat(7, 42.3mm); gap: 0; 
        }
        .label-item {
            width: 70mm; height: 42.3mm; border: 0.05mm solid #eee;
            display: flex; flex-direction: column; justify-content: center;
            align-items: center; text-align: center; box-sizing: border-box;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية (بسيطة ومرتبة)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    school = st.text_input("اسم المدرسة", "مدرسة التميز")
    dept = st.text_input("الإدارة", "إدارة التعليم")
    st.divider()
    c_size = st.number_input("سعة اللجنة", value=20)
    s_no = st.number_input("بداية أرقام الجلوس", value=100)
    f_size = st.slider("حجم الخط", 10, 20, 14)

# 4. الواجهة الرئيسية (Dashboard)
st.markdown(f"<h1 style='text-align: center; color: #1e3a8a;'>🎓 نظام إدارة اللجان</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #666;'>{school} | {dept}</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df['رقم الجلوس'] = range(s_no, s_no + len(df))
    
    # بطاقات الإحصائيات (متجاوبة مع الجوال)
    st.markdown('<div class="no-print">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="dashboard-card"><h4>👥 إجمالي الطلاب</h4><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="dashboard-card"><h4>🏫 عدد اللجان</h4><h2>{math.ceil(len(df)/c_size)}</h2></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 الكشوفات", "🏷️ الملصقات"])

    with tab1:
        # عرض الكشوفات بأسلوب عصري
        for i in range(0, len(df), c_size):
            chunk = df.iloc[i:i+c_size]
            comm_no = int(i/c_size) + 1
            with st.expander(f"📍 لجنة رقم {comm_no}", expanded=True):
                # عرض جدول مبسط للجوال
                st.table(chunk.iloc[:, [0, 1]].rename(columns={chunk.columns[0]: 'الاسم', chunk.columns[1]: 'السجل'}))
                
            # نسخة الطباعة المخفية (تظهر فقط عند ضغط Print)
            st.markdown(f"""
            <div class="only-print page-break" style="display:none; direction:rtl; padding:20mm;">
                <h2 style="text-align:center;">كشف مناداة لجنة {comm_no}</h2>
                <p>{school} - {dept}</p>
                <table border="1" style="width:100%; text-align:center; border-collapse:collapse;">
                    <tr style="background:#f0f0f0;"><th>م</th><th>الاسم</th><th>الجلوس</th><th>السجل</th><th>التوقيع</th></tr>
                    {"".join([f"<tr><td>{idx+1}</td><td>{r.iloc[0]}</td><td>{r['رقم الجلوس']}</td><td>{r.iloc[1]}</td><td style='height:40px;'></td></tr>" for idx, r in chunk.iterrows()])}
                </table>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.warning("⚠️ ملصقات (3×7): للعرض الصحيح استخدم وضع 'العرض بالعرض' في الجوال، أو اطبع مباشرة.")
        # زر طباعة بستايل عصري
        st.markdown('<button class="no-print" onclick="window.print()" style="width:100%; padding:15px; background:#1e3a8a; color:white; border:none; border-radius:10px; font-weight:bold;">🖨️ ابدأ طباعة الملصقات</button>', unsafe_allow_html=True)
        
        # توزيع الملصقات
        for p in range(0, len(df), 21):
            page = df.iloc[p:p+21]
            st.markdown('<div class="label-grid page-break">', unsafe_allow_html=True)
            for idx, r in page.iterrows():
                st.markdown(f"""
                <div class="label-item">
                    <div style="font-size: 8pt; color: #888;">{school}</div>
                    <div style="font-size: {f_size}pt; font-weight: bold; margin: 1mm 0;">{r.iloc[0]}</div>
                    <div style="font-size: 10pt; color: #1e3a8a; font-weight:bold;">رقم الجلوس: {r["رقم الجلوس"]}</div>
                    <div style="font-size: 9pt;">لجنة: {int(idx/c_size)+1}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="dashboard-card" style="text-align:center;"><h3>👋 مرحباً بك في نظام اللجان</h3><p>الرجاء رفع ملف الطلاب للبدء</p></div>', unsafe_allow_html=True)
