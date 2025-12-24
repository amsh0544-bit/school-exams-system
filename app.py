import streamlit as st
import pandas as pd
import math

# إعدادات الصفحة وتنسيق الطباعة
st.set_page_config(page_title="نظام لجان الاختبارات", layout="wide")

# CSS لضبط مقاسات الطباعة (فورماتك 3*7) وكشوف المناداة
st.markdown("""
    <style>
    @media print {
        .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        body { margin: 0; padding: 0; }
        .label-container { 
            display: grid; 
            grid-template-columns: repeat(3, 70mm); 
            grid-template-rows: repeat(7, 42.3mm); 
            gap: 0; padding: 0; margin: 0;
            justify-content: center;
        }
        .attendance-page { 
            page-break-after: always; 
            padding: 15mm; 
            direction: rtl; 
            height: 297mm;
        }
    }
    .label-box {
        width: 70mm; height: 42.3mm; 
        border: 0.1mm solid #eee; 
        text-align: center; 
        padding: 5mm; 
        box-sizing: border-box; 
        display: flex; flex-direction: column; justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# القائمة الجانبية للإعدادات
st.sidebar.header("⚙️ إعدادات النظام")
dept_name = st.sidebar.text_input("إدارة التعليم", "إدارة تعليم ...")
school_name = st.sidebar.text_input("اسم المدرسة", "مدرسة ...")

st.sidebar.divider()
st.sidebar.header("🏷️ خيارات الملصقات")
show_sch = st.sidebar.checkbox("إظهار اسم المدرسة على الملصق", value=True)
show_nid = st.sidebar.checkbox("إظهار رقم الهوية على الملصق", value=True)
show_class = st.sidebar.checkbox("إظهار اللجنة والصف على الملصق", value=True)

st.sidebar.divider()
st.sidebar.header("📊 التحكم في التوزيع")
committee_size = st.sidebar.number_input("عدد الطلاب في كل لجنة", value=20, min_value=1)
start_seat_no = st.sidebar.number_input("بداية أرقام الجلوس", value=101)

# واجهة رفع الملف
st.title("📑 نظام إدارة لجان الاختبارات")
uploaded_file = st.file_uploader("ارفع ملف Excel المستخرج من نظام نور", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # الحفاظ على ترتيب نور وتوليد أرقام الجلوس
    df['رقم الجلوس'] = range(start_seat_no, start_seat_no + len(df))
    
    tab1, tab2 = st.tabs(["📋 كشوف المناداة", "🏷️ ملصقات فورماتك"])
    
    with tab1:
        # كشوف المناداة - كل لجنة في صفحة
        for i in range(0, len(df), committee_size):
            chunk = df.iloc[i:i+committee_size]
            committee_num = int(i/committee_size) + 1
            st.markdown(f"""
            <div class="attendance-page">
                <table style="width:100%; text-align:center; border:none; direction:rtl;">
                    <tr>
                        <td style="text-align:right; font-size:12pt;">المملكة العربية السعودية<br>وزارة التعليم<br>{dept_name}<br>{school_name}</td>
                        <td><h2 style="margin:0;">كشف مناداة لجنة رقم ({committee_num})</h2></td>
                        <td style="text-align:left;">[شعار الوزارة]</td>
                    </tr>
                </table>
                <hr>
                <table border="1" style="width:100%; border-collapse:collapse; text-align:center; direction:rtl;">
                    <tr style="background:#f0f0f0;">
                        <th>م</th><th>اسم الطالب</th><th>رقم الجلوس</th><th>السجل المدني</th><th>التوقيع</th>
                    </tr>
                    {"".join([f"<tr><td>{idx+1}</td><td>{r.iloc[0]}</td><td>{r['رقم الجلوس']}</td><td>{r.iloc[1]}</td><td style='height:35px; width:120px;'></td></tr>" for idx, r in chunk.iterrows()])}
                </table>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        # ملصقات الطاولات 3*7
        st.markdown('<div class="label-container">', unsafe_allow_html=True)
        for idx, r in df.iterrows():
            curr_committee = int(idx/committee_size) + 1
            st.markdown(f"""
            <div class="label-box" style="direction:rtl;">
                {f'<div style="font-size:9pt;">{school_name}</div>' if show_sch else ''}
                <div style="font-size:13pt; font-weight:bold; margin:2mm 0;">{r.iloc[0]}</div>
                {f'<div style="font-size:10pt;">هوية: {r.iloc[1]}</div>' if show_nid else ''}
                <div style="font-size:10pt; font-weight:bold;">رقم الجلوس: {r["رقم الجلوس"]}</div>
                {f'<div style="font-size:9pt;">اللجنة: {curr_committee}</div>' if show_class else ''}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.success("✅ البيانات جاهزة للطباعة")
    st.sidebar.info("استخدم Ctrl + P للطباعة من المتصفح")
else:
    st.warning("يرجى رفع ملف Excel للبدء في توليد اللجان والملصقات.")
