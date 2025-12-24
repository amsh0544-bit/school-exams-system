import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="نظام اللجان الذكي", layout="centered")

# 2. كود إخفاء الزوائد وتحسين الخط العربي
st.markdown("""
    <style>
    /* إخفاء شريط GitHub و Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* تحسين الخط العربي */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Tajawal', sans-serif; 
        text-align: right; 
        direction: rtl; 
    }
    
    /* تنسيق خاص للطباعة فقط (لا يؤثر على شكل التطبيق في الجوال) */
    @media print {
        .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .label-container { 
            display: grid; 
            grid-template-columns: repeat(3, 70mm); 
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

# 3. القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    school = st.text_input("اسم المدرسة", "مدرسة التميز")
    dept = st.text_input("إدارة التعليم", "إدارة تعليم ...")
    st.divider()
    c_size = st.number_input("سعة اللجنة (طلاب)", value=20)
    s_no = st.number_input("بداية أرقام الجلوس", value=100)
    font_size = st.slider("حجم خط الملصق", 10, 20, 14)

# 4. واجهة التطبيق الرئيسية (بسيطة ومنظمة)
st.title("📑 نظام إدارة اللجان")
st.caption(f"تطبيق خاص بـ: {school}")

file = st.file_uploader("📂 ارفع ملف اكسل (نظام نور)", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    df['رقم الجلوس'] = range(s_no, s_no + len(df))
    
    # عرض الإحصائيات بشكل بسيط متوافق مع الجوال
    st.success(f"✅ تم رفع {len(df)} طالباً بنجاح")
    
    col_info1, col_info2 = st.columns(2)
    col_info1.metric("إجمالي الطلاب", len(df))
    col_info2.metric("عدد اللجان", math.ceil(len(df)/c_size))

    tab1, tab2 = st.tabs(["📋 كشوف المناداة", "🏷️ ملصقات فورماتك"])

    with tab1:
        st.info("💡 اضغط مطولاً على الجدول أو استخدم زر الطباعة في المتصفح")
        for i in range(0, len(df), c_size):
            chunk = df.iloc[i:i+c_size]
            st.subheader(f"لجنة رقم {int(i/c_size)+1}")
            # عرض جدول بسيط جداً يسهل رؤيته في الجوال
            display_df = chunk.iloc[:, [0, 1]].copy()
            display_df.columns = ['الاسم', 'السجل']
            display_df['رقم الجلوس'] = chunk['رقم الجلوس']
            st.table(display_df)

    with tab2:
        st.warning("⚠️ ملصقات (3×7): يفضل استعراضها وطباعتها من الكمبيوتر لضمان دقة المقاسات.")
        if st.button("👁️ عرض الملصقات للمعاينة"):
            for p in range(0, len(df), 21):
                page = df.iloc[p:p+21]
                st.markdown('<div class="label-container">', unsafe_allow_html=True)
                for idx, r in page.iterrows():
                    st.markdown(f"""
                    <div class="label-box">
                        <div style="font-size: 8pt; color: gray;">{school}</div>
                        <div style="font-size: {font_size}pt; font-weight: bold;">{r.iloc[0]}</div>
                        <div style="font-size: 10pt;">رقم الجلوس: {r["رقم الجلوس"]}</div>
                        <div style="font-size: 9pt;">اللجنة: {int(idx/c_size)+1}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👋 الرجاء رفع ملف الطلاب للبدء.")
