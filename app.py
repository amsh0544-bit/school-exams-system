import streamlit as st
import pandas as pd
import math

# 1. إعداد الصفحة وإخفاء عناصر المنصة (GitHub/Streamlit)
st.set_page_config(page_title="نظام إدارة اللجان الذكي", layout="wide")

st.markdown("""
    <style>
    /* إخفاء شريط الأدوات العلوي وتذييل الصفحة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* تحسين الخطوط والتنسيق العربي الاحترافي */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; text-align: right; direction: rtl; }
    
    /* تصميم بطاقات المعلومات */
    .metric-container {
        background-color: #ffffff; padding: 15px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-right: 5px solid #1e3a8a;
        margin-bottom: 20px;
    }

    /* هندسة الطباعة الدقيقة لفورماتك 3*7 */
    @media print {
        .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .label-container { 
            display: grid; grid-template-columns: repeat(3, 70mm); 
            grid-template-rows: repeat(7, 42.3mm); gap: 0;
        }
        .label-box {
            width: 70mm; height: 42.3mm; border: 0.1mm solid #eee;
            display: flex; flex-direction: column; justify-content: center;
            align-items: center; text-align: center; padding: 5px; box-sizing: border-box;
        }
        .page-break { page-break-after: always; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (لوحة التحكم الشاملة)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ إعدادات النظام</h2>", unsafe_allow_html=True)
    school = st.text_input("اسم المدرسة", "مدرسة ...")
    dept = st.text_input("الإدارة التعليمية", "إدارة تعليم ...")
    
    st.divider()
    st.subheader("📏 التحكم في المظهر")
    font_name_size = st.slider("حجم خط اسم الطالب", 10, 20, 14)
    show_id = st.checkbox("إظهار السجل المدني", value=True)
    show_comm = st.checkbox("إظهار رقم اللجنة", value=True)
    
    st.divider()
    st.subheader("📊 أرقام الجلوس واللجان")
    c_size = st.number_input("سعة اللجنة (طلاب)", value=20)
    s_no = st.number_input("بداية أرقام الجلوس", value=100)

# 3. الواجهة الرئيسية
st.markdown(f"<h1 style='text-align: center; color: #1e3a8a;'>📑 نظام لجان الاختبارات - {school}</h1>", unsafe_allow_html=True)

file = st.file_uploader("📂 ارفع ملف Excel المستخرج من نظام نور", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    df['رقم الجلوس'] = range(s_no, s_no + len(df))
    
    # بطاقات الإحصائيات
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f'<div class="metric-container"><h4>إجمالي الطلاب</h4><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-container"><h4>عدد اللجان</h4><h2>{math.ceil(len(df)/c_size)}</h2></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-container"><h4>حالة النظام</h4><h2>جاهز للطباعة</h2></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 كشوف المناداة", "🏷️ ملصقات فورماتك (3×7)"])

    with tab1:
        st.markdown('<button class="no-print" style="width:100%; padding:10px; background:#1e3a8a; color:white; border:none; border-radius:5px; cursor:pointer;" onclick="window.print()">🖨️ طباعة الكشوفات (PDF)</button>', unsafe_allow_html=True)
        for i in range(0, len(df), c_size):
            chunk = df.iloc[i:i+c_size]
            st.markdown(f"""
            <div class="page-break" style="padding: 15mm; direction: rtl; background: white;">
                <table style="width: 100%; margin-bottom: 20px;">
                    <tr>
                        <td style="text-align: right;">وزارة التعليم<br>{dept}<br>{school}</td>
                        <td style="text-align: center;"><h2>كشف مناداة لجنة ({int(i/c_size)+1})</h2></td>
                    </tr>
                </table>
                <table border="1" style="width: 100%; border-collapse: collapse; text-align: center;">
                    <tr style="background: #f8f9fa;">
                        <th>م</th><th>اسم الطالب</th><th>رقم الجلوس</th><th>السجل المدني</th><th style="width:120px;">التوقيع</th>
                    </tr>
                    {"".join([f"<tr><td>{idx+1}</td><td>{r.iloc[0]}</td><td>{r['رقم الجلوس']}</td><td>{r.iloc[1]}</td><td></td></tr>" for idx, r in chunk.iterrows()])}
                </table>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<button class="no-print" style="width:100%; padding:10px; background:#28a745; color:white; border:none; border-radius:5px; cursor:pointer;" onclick="window.print()">🖨️ طباعة ملصقات فورماتك (PDF)</button>', unsafe_allow_html=True)
        # توليد الصفحات (كل صفحة 21 ملصق)
        for p in range(0, len(df), 21):
            page_chunk = df.iloc[p:p+21]
            st.markdown('<div class="label-container page-break">', unsafe_allow_html=True)
            for idx, r in page_chunk.iterrows():
                st.markdown(f"""
                <div class="label-box" style="direction: rtl;">
                    <div style="font-size: 8pt; color: #777;">{school}</div>
                    <div style="font-size: {font_name_size}pt; font-weight: bold; margin: 2mm 0;">{r.iloc[0]}</div>
                    {f'<div style="font-size: 9pt;">هوية: {r.iloc[1]}</div>' if show_id else ''}
                    <div style="font-size: 10pt; font-weight: bold; color: #1e3a8a;">رقم الجلوس: {r["رقم الجلوس"]}</div>
                    {f'<div style="font-size: 8pt;">اللجنة: {int(idx/c_size)+1}</div>' if show_comm else ''}
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👋 مرحباً بك! يرجى رفع ملف الطلاب من نظام نور للبدء.")
