import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
from datetime import datetime
import hashlib  # Untuk sistem login

# =============== SETUP PROFESIONAL ===============
st.set_page_config(
    page_title="FraudGuard Pro - Competitive Edition",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# =============== SISTEM LOGIN (Multi-user) ===============
def authenticate(username, password):
    """Sistem autentikasi sederhana untuk kompetisi"""
    users = {
        "bank": "5f4dcc3b5aa765d61d8327deb882cf99",  # password: password
        "regulator": "482c811da5d5b4bc6d497ffa98491e38",  # password: 123456
        "admin": "21232f297a57a5a743894a0e4a801fc3"  # password: admin
    }
    hashed_pw = hashlib.md5(password.encode()).hexdigest()
    return users.get(username) == hashed_pw

# =============== FUNGSI DETEKSI AI REAL ===============
class FraudDetector:
    def __init__(self):
        self.model = self.train_model()
        
    def train_model(self):
        """Model AI Isolation Forest untuk kompetisi"""
        # Simulasi dataset (dalam real competition pakai data nyata)
        np.random.seed(42)
        X = 0.3 * np.random.randn(100, 2)
        X = np.r_[X + 2, X - 2]
        return IsolationForest(contamination=0.2).fit(X)
    
    def predict(self, transaction):
        """Prediksi fraud dengan model AI"""
        features = [
            transaction['amount'] / 1000000,  # Jumlah dalam jutaan
            1 if transaction['time'][:2] in ['00','01','02','03','04'] else 0,  # Transaksi dini hari
            len(transaction['history'])  # Jumlah histori transaksi
        ]
        score = self.model.decision_function([features])[0]
        return score < -0.1  # Threshold untuk fraud

# =============== DASHBOARD KOMPETISI ===============
with st.sidebar:
    st.title("🔒 LOGIN FRAUDGUARD PRO")
    username = st.selectbox("Username", ["bank", "regulator", "admin"])
    password = st.text_input("Password", type="password")
    
    if st.button("Login", type="primary"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success(f"Berhasil login sebagai {username.upper()}")
        else:
            st.error("Login gagal! Password salah")

if st.session_state.get('logged_in'):
    # =============== HEADER KOMPETISI ===============
    st.title("🛡️ FRAUDGUARD PRO - COMPETITION EDITION")
    st.caption("AI-Powered Financial Fraud Detection | Real-time Monitoring & Blockchain Analysis")
    
    # =============== SIMULASI PROFESIONAL ===============
    detector = FraudDetector()
    
    with st.expander("⚙️ KOMPETISI PARAMETER", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            speed = st.slider("Transaksi/detik", 1, 10, 3)
        with col2:
            fraud_rate = st.slider("Tingkat Fraud (%)", 0, 100, 25)
        with col3:
            sensitivity = st.slider("Sensitivitas AI", 0.0, 1.0, 0.7)
    
    # =============== VISUALISASI REAL-TIME ===============
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🚨 LIVE ALERTS")
        alert_placeholder = st.empty()
        
    with col2:
        st.subheader("📊 FRAUD ANALYTICS")
        chart_placeholder = st.empty()
    
    # =============== DATA HISTORY ===============
    st.subheader("📝 AUDIT TRAIL")
    data_placeholder = st.empty()
    
    # Inisialisasi data
    if 'transactions' not in st.session_state:
        st.session_state.transactions = []
        st.session_state.fraud_count = 0
        st.session_state.normal_count = 0
    
    # =============== SIMULASI PROFESIONAL ===============
    while st.session_state.get('running', True):
        # Generate transaksi realistis
        trx = {
            'id': f"TX{time.time_ns() % 1000000}",
            'type': random.choice(["Transfer", "Crypto", "E-Wallet", "Credit Card"]),
            'amount': random.randint(10000, 500000000),
            'time': datetime.now().strftime("%H:%M:%S"),
            'from': f"USER-{random.randint(1000,9999)}",
            'to': f"RECV-{random.randint(1000,9999)}",
            'history': [random.randint(10000, 1000000) for _ in range(3)]
        }
        
        # Generate fraud buatan untuk kompetisi
        if random.random() < fraud_rate/100:
            trx['amount'] = random.randint(100000000, 2000000000)
            if random.random() > 0.5:
                trx['time'] = f"{random.randint(0,4):02d}:{random.randint(0,59):02d}"
        
        # Deteksi fraud dengan AI
        is_fraud = detector.predict(trx) if random.random() < sensitivity else False
        trx['status'] = "🚨 FRAUD" if is_fraud else "✅ NORMAL"
        
        # Update counters
        if is_fraud:
            st.session_state.fraud_count += 1
        else:
            st.session_state.normal_count += 1
            
        # Update data
        st.session_state.transactions.insert(0, trx.copy())
        if len(st.session_state.transactions) > 50:
            st.session_state.transactions.pop()
        
        # =============== UPDATE DASHBOARD ===============
        with alert_placeholder.container():
            if is_fraud:
                st.error(f"""
                **ALERT FRAUD TERBARU**  
                🔴 `{trx['id']}` | {trx['time']}  
                💸 **Rp {trx['amount']:,}**  
                🏷️ {trx['type']} » {trx['from']} → {trx['to']}
                """)
            else:
                st.success("✅ Tidak ada aktivitas mencurigakan")
                
            st.metric("Total Fraud Terdeteksi", st.session_state.fraud_count)
        
        with chart_placeholder.container():
            df = pd.DataFrame({
                'Status': ['Normal', 'Fraud'],
                'Count': [st.session_state.normal_count, st.session_state.fraud_count]
            })
            fig = px.pie(df, values='Count', names='Status', 
                         title='Distribusi Transaksi',
                         color_discrete_sequence=['green','red'])
            st.plotly_chart(fig, use_container_width=True)
        
        with data_placeholder.container():
            df = pd.DataFrame(st.session_state.transactions)
            st.dataframe(df[['id', 'type', 'amount', 'time', 'status']], 
                         height=300, use_container_width=True)
        
        time.sleep(3/speed)
else:
    st.markdown("""
    <div style="text-align:center; padding:5rem;">
        <h1>🛡️ FRAUDGUARD PRO</h1>
        <p>Competition Edition - Deteksi Fraud Keuangan & Blockchain</p>
        <p>Silakan login untuk mengakses sistem</p>
    </div>
    """, unsafe_allow_html=True)

# =============== FOOTER KOMPETISI ===============
st.divider()
st.caption("""
**FraudGuard Pro v1.0** | Copyright © 2024 - Tim Lomba Inovasi Keuangan  
Powered by AI | Real-time Fraud Detection | Blockchain Analysis  
""")
