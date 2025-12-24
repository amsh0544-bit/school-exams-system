import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة وهوية النظام
st.set_page_config(page_title="نظام الاختبارات الذكي", layout="wide", initial_sidebar_state="collapsed")

# 2. كود التصميم المتقدم (CSS) لمحاكاة الصور التي أرفقتها
st.markdown("""
    <style>
    /* إخفاء العناصر غير المرغوبة */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display:none;}
    
    /* الخلفية والخطوط */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Tajawal', sans-serif; 
        direction: rtl; 
        background-color: #f4f7f9; 
    }

    /* الهيدر العلوي المتدرج مثل الصورة */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; padding: 30px; border-radius: 0 0 30px 30px;
        text-align: center; margin: -60px -20px 30px -20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* تصميم البطاقات الملونة (Grid System) */
    .card-container {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 15px; margin: 20px 0;
    }
    .feature-card {
        background: white; border-radius: 20px; padding: 20px;
        text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-bottom: 5px solid #3b82f6; transition: 0.3s;
    }
    .feature-card:active { transform: scale(0.95); }
    .icon-circle {
        width: 50px; height: 50px; background: #eff6ff;
        border-radius: 50%; display: flex; align-items: center;
        justify-content: center; margin: 0 auto 10px auto; font-size: 24px;
    }

    /* تحسين شكل رفع الملفات */
    .stFileUploader { background: white; border-radius: 20px; padding: 20px; border: 2px dashed #3b82f6; }

    /* تنسيق الطباعة (مخفي في العرض) */
    @media print {
        .no-print { display: none !important; }
        @page { size: A4; margin: 0; }
        .label-grid { display: grid; grid-template-columns: repeat(3, 70mm); grid-template-rows: repeat(7, 42.3mm); }
        .label-item { 
            width: 70mm; height: 42.3mm; border: 0.1mm solid #eee;
            display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الهيدر العلوي
st.markdown(f"""
    <div class="main-header">
        <h2 style="margin:0;">متوسطة وثانوية ...</h2>
        <p style="opacity:0.8;">نظام إدارة لجان الاختبارات والتحضير</p>
    </div>
    """, unsafe_allow_html=True)

# 4. لوحة التحكم الجانبية (للإعدادات فقط)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/ar/8/bb/%D8%B4%D8%B9%D8%A7%D8%B1_%D9%88%D8%B2%D8%A7%D8%B1%D8%A9_%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85_%D8%A7%D9%84%D8%B3%D8%B9%D9%88%D8%AF%D9%8A%D8%A9.png", width=100)
    st.subheader("⚙️ ضبط النظام")
    school_name = st.text_input("اسم المدرسة", "مدرسة فيصل بن فهد")
    c_size = st.number_input("طلاب اللجنة", value=20)
    s_no = st.number_input("بداية أرقام الجلوس", value=100)

# 5. الواجهة الرئيسية (البطاقات التفاعلية)
uploaded_file = st.file_uploader("📂 الخطوة الأولى: ارفع ملف الطلاب (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df['رقم الجلوس'] = range(s_no, s_no + len(df))
    
    st.markdown("### 📊 مركز العمليات")
    st.markdown(f"""
    <div class="card-container no-print">
        <div class="feature-card">
            <div class="icon-circle">👥</div>
            <div style="font-weight:bold;">الطلاب</div>
            <div style="color:#3b82f6; font-size:20px;">{len(df)}</div>
        </div>
        <div class="feature-card">
            <div class="icon-circle">🏫</div>
            <div style="font-weight:bold;">اللجان</div>
            <div style="color:#10b981; font-size:20px;">{math.ceil(len(df)/c_size)}</div>
        </div>
        <div class="feature-card">
            <div class="icon-circle">📅</div>
            <div style="font-weight:bold;">الحالة</div>
            <div style="color:#f59e0b; font-size:14px;">جاهز للتوزيع</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🖨️ مركز الطباعة")
    
    # بطاقات الطباعة (أزرار تفاعلية)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 كشوف المناداة"):
            st.session_state.mode = "list"
    with col2:
        if st.button("🏷️ ملصقات الطاولات"):
            st.session_state.mode = "labels"

    # عرض النتائج بناءً على الاختيار
    if 'mode' in st.session_state:
        if st.session_state.mode == "list":
            for i in range(0, len(df), c_size):
                chunk = df.iloc[i:i+c_size]
                st.markdown(f"""
                <div style="background:white; padding:20px; border-radius:15px; margin-bottom:10px; border:1px solid #ddd;">
                    <h4 style="text-align:center;">كشف لجنة {int(i/c_size)+1}</h4>
                    <table style="width:100%; text-align:center; border-collapse:collapse;">
                        <tr style="background:#f3f4f6;"><th>الاسم</th><th>الجلوس</th></tr>
                        {"".join([f"<tr><td>{r.iloc[0]}</td><td>{r['رقم الجلوس']}</td></tr>" for idx, r in chunk.iterrows()])}
                    </table>
                </div>
                """, unsafe_allow_html=True)
            st.button("🖨️ تأكيد طباعة الكشوف", on_click=None)

        elif st.session_state.mode == "labels":
            st.warning("⚠️ الطباعة مصممة لورق A4 (3x7)")
            if st.button("إرسال للطابعة"):
                for p in range(0, len(df), 21):
                    page = df.iloc[p:p+21]
                    st.markdown('<div class="label-grid">', unsafe_allow_html=True)
                    for idx, r in page.iterrows():
                        st.markdown(f"""
                        <div class="label-item">
                            <div style="font-size: 8pt; color: #888;">{school_name}</div>
                            <div style="font-size: 11pt; font-weight: bold;">{r.iloc[0]}</div>
                            <div style="font-size: 10pt; color: #1e3a8a;">جلوس: {r["رقم الجلوس"]}</div>
                            <div style="font-size: 9pt;">لجنة: {int(idx/c_size)+1}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center; padding:50px; color:#999;">
        <p>ارفع ملف Excel من نظام نور للبدء في توزيع اللجان تلقائياً</p>
    </div>
    """, unsafe_allow_html=True)
