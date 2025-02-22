import streamlit as st
import pandas as pd
import sqlite3

# إنشاء قاعدة بيانات SQLite وتخزين المستخدمين
conn = sqlite3.connect("libmovie.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS favorites (username TEXT, movie_id INTEGER)''')
conn.commit()

movies_db = [
    {"id": 1, "title": "Inception", "poster": "https://image.tmdb.org/t/p/w500/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg", "description": "A thief who enters the dreams of others.", "url": "https://www.example.com/inception"},
    {"id": 2, "title": "Interstellar", "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", "description": "A journey through space and time.", "url": "https://www.example.com/interstellar"}
]

def login():
    st.title("LibMovie - تسجيل الدخول")
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل الدخول"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("تم تسجيل الدخول بنجاح!")
        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

def signup():
    st.title("LibMovie - إنشاء حساب")
    new_username = st.text_input("اسم المستخدم الجديد")
    new_password = st.text_input("كلمة المرور", type="password")
    if st.button("إنشاء حساب"):
        c.execute("SELECT * FROM users WHERE username=?", (new_username,))
        if c.fetchone():
            st.error("اسم المستخدم موجود بالفعل")
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            st.success("تم إنشاء الحساب! قم بتسجيل الدخول الآن.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    page = st.sidebar.selectbox("اختر", ["تسجيل الدخول", "إنشاء حساب"])
    if page == "تسجيل الدخول":
        login()
    else:
        signup()
else:
    st.sidebar.title(f"مرحبًا، {st.session_state.username}")
    st.sidebar.button("تسجيل الخروج", on_click=lambda: st.session_state.update({"logged_in": False, "username": ""}))
    
    search_query = st.text_input("🔍 البحث عن فيلم")
    
    st.subheader("🎬 الأفلام المقترحة")
    for movie in movies_db:
        if search_query.lower() in movie["title"].lower():
            with st.expander(movie["title"]):
                st.image(movie["poster"], width=200)
                st.write(movie["description"])
                
                # زر إضافة إلى المفضلة
                if st.button("❤️ أضف إلى المفضلة", key=f"fav_{movie['id']}"):
                    c.execute("INSERT INTO favorites (username, movie_id) VALUES (?, ?)", (st.session_state.username, movie['id']))
                    conn.commit()
                    st.success("تمت الإضافة إلى المفضلة!")
                
                # التقييم
                rating = st.slider("⭐ التقييم", 0, 5, 3, key=f"rating_{movie['id']}")
                
                # زر المشاهدة
                if st.button("▶️ مشاهدة الفيلم", key=f"watch_{movie['id']}"):
                    st.video(movie["url"])
                
                # قسم التعليقات
                st.text_area("💬 أضف تعليقك", key=f"comment_{movie['id']}")
                if st.button("إرسال التعليق", key=f"submit_{movie['id']}"):
                    st.success("تم إرسال تعليقك!")
