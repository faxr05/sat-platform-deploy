import subprocess
import sys
import time

def main():
    print("🚀 SAT Platformasi ishga tushirilmoqda...")
    print("Iltimos, kuting...\n")

    # 1. Flask serverni ishga tushirish (O'quvchi qismi API)
    flask_process = subprocess.Popen([sys.executable, 'server.py'])
    
    # 2. Streamlit serverni ishga tushirish (Ustoz paneli)
    streamlit_process = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'ustoz_app.py'])

    print("\n✅ Tizim muvaffaqiyatli ishga tushdi!")
    print("👨‍🏫 Ustoz paneli: Brauzerda avtomatik ochiladi (yoki http://localhost:8501)")
    print("🧑‍🎓 O'quvchi paneli: http://localhost:5000 manziliga kiring\n")
    print("Dasturni to'xtatish uchun terminalda 'Ctrl + C' ni bosing.")

    try:
        # Asosiy jarayon yopilib qolmasligi uchun cheksiz tsikl
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Ctrl+C bosilganda ikkala serverni ham to'xtatish
        print("\n🛑 Dastur to'xtatilmoqda...")
        flask_process.terminate()
        streamlit_process.terminate()
        flask_process.wait()
        streamlit_process.wait()
        print("✅ Barcha jarayonlar to'xtatildi. Xayr!")

if __name__ == '__main__':
    main()

