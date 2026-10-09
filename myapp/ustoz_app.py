import streamlit as st
import os
import sqlite3
import pandas as pd
from datetime import datetime

# 1. Ma'lumotlar bazasini ulaymiz (SQLite)
DB_PATH = os.path.join(os.environ.get('DATA_DIR', '.'), 'sat_platform.db')
conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=15)
c = conn.cursor()

def init_db():
    # Testlar jadvali
    c.execute('''CREATE TABLE IF NOT EXISTS tests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    duration INTEGER,
                    created_at TEXT)''')
    # Savollar jadvali
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_id INTEGER,
                    q_text TEXT,
                    image_path TEXT,
                    opt_a TEXT, opt_b TEXT, opt_c TEXT, opt_d TEXT,
                    correct_opt TEXT)''')
    # Natijalar (Statistika) jadvali
    c.execute('''CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT,
                    test_id INTEGER,
                    score INTEGER,
                    total_q INTEGER,
                    time_spent_min INTEGER,
                    date_taken TEXT)''')
    conn.commit()

init_db()

# 2. Ustoz uchun oddiy Login tizimi
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("👨‍🏫 Ustoz Paneliga Kirish")
    username = st.text_input("Login")
    password = st.text_input("Parol", type="password")
    if st.button("Kirish"):
        ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
        ADMIN_PASS = os.environ.get("ADMIN_PASS", "")
        if ADMIN_PASS and username == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Login yoki parol xato!")
else:
    # 3. Asosiy Ustoz Paneli (Dashboard)
    st.sidebar.title("Menyu")
    menu = st.sidebar.radio("Bo'limni tanlang:", ["yangi Test yaratish", "Savollar qo'shish", "O'quvchilar Statistikasi"])
    
    if st.sidebar.button("Chiqish (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

    # --- 1-BO'LIM: YANGI TEST YARATISH ---
    if menu == "yangi Test yaratish":
        st.title("📝 Yangi Test Yaratish")
        
        with st.form("test_form"):
            t_name = st.text_input("Test nomi (Masalan: Math Section 1)")
            t_duration = st.number_input("Testga beriladigan vaqt (daqiqa)", min_value=5, max_value=180, value=35)
            submit_test = st.form_submit_button("Testni saqlash")
            
            if submit_test and t_name:
                date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
                c.execute("INSERT INTO tests (title, duration, created_at) VALUES (?, ?, ?)", (t_name, t_duration, date_now))
                conn.commit()
                st.success(f"'{t_name}' muvaffaqiyatli yaratildi!")
        
        st.subheader("Mavjud Testlar")
        df_tests = pd.read_sql_query("SELECT * FROM tests", conn)
        st.dataframe(df_tests, use_container_width=True)

    # --- 2-BO'LIM: SAVOLLAR QO'SHISH ---
    elif menu == "Savollar qo'shish":
        st.title("➕ Testga Savol Qo'shish")
        
        # Bazadan testlarni olib kelish
        c.execute("SELECT id, title FROM tests")
        tests = c.fetchall()
        
        if not tests:
            st.warning("Avval 'Yangi Test yaratish' bo'limidan test yarating!")
        else:
            test_dict = {f"{t[0]} - {t[1]}": t[0] for t in tests}
            selected_test = st.selectbox("Qaysi testga savol qo'shamiz?", list(test_dict.keys()))
            test_id = test_dict[selected_test]
            
            with st.form("question_form"):
                q_text = st.text_area("Savol matni")
                q_image = st.file_uploader("Savol uchun rasm (Ixtiyoriy)", type=['png', 'jpg', 'jpeg'])
                
                col1, col2 = st.columns(2)
                with col1:
                    opt_a = st.text_input("A varianti")
                    opt_b = st.text_input("B varianti")
                with col2:
                    opt_c = st.text_input("C varianti")
                    opt_d = st.text_input("D varianti")
                
                correct = st.selectbox("To'g'ri javobni belgilang:", ["A", "B", "C", "D"])
                submit_q = st.form_submit_button("Savolni Saqlash")
                
                if submit_q and q_text and opt_a and opt_b:
                    # Agar rasm yuklangan bo'lsa uni nomini saqlab qolamiz (Faylni saqlash logikasi qo'shish mumkin)
                    img_name = q_image.name if q_image else "Yo'q"
                    
                    c.execute('''INSERT INTO questions 
                                 (test_id, q_text, image_path, opt_a, opt_b, opt_c, opt_d, correct_opt) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                                 (test_id, q_text, img_name, opt_a, opt_b, opt_c, opt_d, correct))
                    conn.commit()
                    st.success("Savol muvaffaqiyatli saqlandi!")

    # --- 3-BO'LIM: STATISTIKA VA NATIJALAR ---
    elif menu == "O'quvchilar Statistikasi":
        st.title("📊 O'quvchilar Natijalari")
        
        # Keling MVP ni ko'rsatish uchun "soxta (fake)" ma'lumot kiritib ko'ramiz
        if st.button("Test uchun soxta natija qo'shish (Demonstratsiya)"):
            c.execute("INSERT INTO results (student_name, test_id, score, total_q, time_spent_min, date_taken) VALUES (?, ?, ?, ?, ?, ?)",
                      ("Ali Valiyev", 1, 7, 8, 25, datetime.now().strftime("%Y-%m-%d %H:%M")))
            conn.commit()
            st.success("Ma'lumot qo'shildi!")

        # Natijalarni ko'rsatish
        query = '''
        SELECT 
            r.student_name as "O'quvchi", 
            t.title as "Test nomi", 
            r.score || '/' || r.total_q as "Natija", 
            r.time_spent_min as "Sarflangan vaqt (min)", 
            r.date_taken as "Topshirgan sanasi"
        FROM results r
        JOIN tests t ON r.test_id = t.id
        ORDER BY r.id DESC
        '''
        try:
            df_results = pd.read_sql_query(query, conn)
            if df_results.empty:
                st.info("Hali hech kim test ishlamagan.")
            else:
                st.dataframe(df_results, use_container_width=True)
                
                # Kichik chart (grafik) qilib ko'rsatamiz
                st.subheader("O'quvchilar o'zlashtirishi (Grafik)")
                st.bar_chart(data=df_results, x="O'quvchi", y="Natija")
                
        except:
            st.info("Hozircha natijalar bazasi shakllanmadi.")

# Bazani yopish (Xavfsizlik uchun)
conn.close()

