# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os
import time

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="ChurnGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS (Premium Animation) ======================
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e2937 100%);
        color: white;
    }


    .stSelectbox label,
    .stSlider label,
    .stNumberInput label,
    .stTextInput label,
    .stMultiSelect label {

    color: #38bdf8 !important;
    font-size: 18px !important;
    font-weight: 700 !important;

    text-shadow:
        0 0 5px #38bdf8,
        0 0 10px #38bdf8,
        0 0 20px rgba(56,189,248,0.8);

    letter-spacing: 0.5px;
    }
            


    h1, h2, h3 {
        color: #e0f2fe;
        font-weight: 700;
    }
    .stButton>button {
        width: 100%;
        height: 3.2em;
        border-radius: 16px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.5);
    }
    .metric-card {
        background: rgba(255,255,255,0.08);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        text-align: center;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .churn-high {
        color: #f87171;
        font-size: 2rem;
        font-weight: bold;
    }
    .churn-low {
        color: #4ade80;
        font-size: 2rem;
        font-weight: bold;
        
    }

}          
</style>
""", unsafe_allow_html=True)


# ====================== TITLE ======================
st.markdown("""
    <h1 style='text-align:center; margin-bottom:0;'>
        🛡️ ChurnGuard AI
    </h1>
    <p style='text-align:center; font-size:22px; color:#94a3b8;'>
        Intelligent Telecom Customer Retention System
    </p>
""", unsafe_allow_html=True)

# ====================== LOAD DATA ======================
file_path = "churn_dataset.csv"

if not os.path.exists(file_path):
    st.error("❌ Dataset not found! Please place `churn_dataset.csv` in the same folder.")
    st.stop()

df = pd.read_csv(file_path)

# ====================== DATA PREPROCESSING ======================
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

if 'customerID' in df.columns:
    df.drop('customerID', axis=1, inplace=True)

# Encoding
label_encoders = {}
for col in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# ====================== MODEL TRAINING ======================
X = df.drop('Churn', axis=1)
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test_scaled))

# ====================== SIDEBAR ======================
st.sidebar.image("https://img.icons8.com/3d-fluency/96/shield.png", width=80)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Prediction", "Analytics", "About"])

# ====================== DASHBOARD ======================
if page == "Dashboard":
    st.subheader("📊 Business Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Total Customers</h4>
            <h1>{len(df):,}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        churn_rate = round(df['Churn'].mean() * 100, 2)
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Churn Rate</h4>
            <h1>{churn_rate}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Model Accuracy</h4>
            <h1>{round(accuracy*100, 2)}%</h1>
        </div>
        """, unsafe_allow_html=True)

    # Animated Charts
    c1, c2 = st.columns([2, 1])
    with c1:
        fig1 = px.pie(df, names=df['Churn'].map({0:"Stayed", 1:"Churned"}), 
                     title="Churn Distribution", hole=0.6,
                     color_discrete_sequence=['#4ade80', '#f87171'])
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.histogram(df, x='MonthlyCharges', color=df['Churn'].map({0:"Stayed", 1:"Churned"}),
                           title="Monthly Charges Distribution", 
                           color_discrete_sequence=['#4ade80', '#f87171'])
        st.plotly_chart(fig2, use_container_width=True)

# ====================== PREDICTION ======================
elif page == "Prediction":
    st.subheader("🔮 Real-time Churn Prediction")

    with st.form("predict_form"):
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["Female", "Male"])
            senior = st.selectbox("Senior Citizen", [0, 1])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])
            tenure = st.slider("Tenure (Months)", 0, 72, 12)
            monthly = st.slider("Monthly Charges", 18.0, 150.0, 70.0)

        with col2:
            phone = st.selectbox("Phone Service", ["Yes", "No"])
            internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
            payment = st.selectbox("Payment Method", [
                "Electronic check", "Mailed check",
                "Bank transfer (automatic)", "Credit card (automatic)"
            ])

        submitted = st.form_submit_button("🚀 Predict Churn Risk")

    if submitted:
        with st.spinner("Analyzing customer..."):
            time.sleep(1.2)  # Simulate AI thinking

        input_dict = {
            'gender': gender, 'SeniorCitizen': senior, 'Partner': partner,
            'Dependents': dependents, 'tenure': tenure, 'PhoneService': phone,
            'MultipleLines': 'No', 'InternetService': internet,
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'No',
            'TechSupport': 'No', 'StreamingTV': 'No', 'StreamingMovies': 'No',
            'Contract': contract, 'PaperlessBilling': paperless,
            'PaymentMethod': payment, 'MonthlyCharges': monthly,
            'TotalCharges': monthly * tenure
        }

        input_df = pd.DataFrame([input_dict])

        # Encode
        for col in input_df.columns:
            if col in label_encoders:
                input_df[col] = label_encoders[col].transform(input_df[col])

        input_df = input_df[X.columns]
        input_scaled = scaler.transform(input_df)

        prob = model.predict_proba(input_scaled)[0][1]
        prediction = model.predict(input_scaled)[0]

        st.markdown("### Prediction Result")
        if prediction == 1:
            st.markdown(f"<p class='churn-high'>⚠️ HIGH CHURN RISK ({prob:.1%})</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p class='churn-low'>✅ LOW CHURN RISK ({(1-prob):.1%})</p>", unsafe_allow_html=True)

        # Animated Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=prob * 100,
            title={'text': "Churn Probability"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#f87171" if prob > 0.5 else "#4ade80"},
                   'steps': [{'range': [0, 40], 'color': "#4ade80"},
                             {'range': [40, 70], 'color': "#fbbf24"},
                             {'range': [70, 100], 'color': "#f87171"}]}
        ))
        st.plotly_chart(fig, use_container_width=True)

# ====================== ANALYTICS & ABOUT ======================
elif page == "Analytics":
    st.subheader("📊 Advanced Analytics")
    fig = px.box(df, x='Churn', y='MonthlyCharges', color='Churn',
                title="Monthly Charges vs Churn")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.imshow(df.corr(), text_auto=True, title="Feature Correlation")
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.subheader("About ChurnGuard AI")
    st.markdown("""
        <div style="
        background: rgba(255,255,255,0.05);
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.1);
        color: #38bdf8;
        font-size: 15px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(56,189,248,0.8);
    ">
        ❤️ Built with Streamlit, Plotly & Scikit-learn
    </div>
    """, unsafe_allow_html=True)

    # st.info("Built with ❤️ using Streamlit, Plotly & Scikit-learn")
    # st.write("Goal: Help telecom companies reduce customer churn using AI.")

st.markdown("---")
st.markdown("""
<p style='
text-align:center;
color:white;
font-size:18px;
font-weight:bold;
text-shadow:0 0 10px rgba(255,255,255,0.8);
animation:pulse 2s infinite;
'>
Made with ❤️ using Streamlit
</p>
""", unsafe_allow_html=True)



















# # app.py
# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score
# import os
# import time

# # ====================== PAGE CONFIG ======================
# st.set_page_config(
#     page_title="ChurnGuard AI",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ====================== CUSTOM CSS + ANIMATED LOGO ======================
# st.markdown("""
# <style>
#     .main {
#         background: linear-gradient(135deg, #0f172a 0%, #1e2937 100%);
#         color: white;
#     }
#     .rotating-logo {
#         animation: rotate 8s linear infinite;
#         width: 85px;
#         filter: drop-shadow(0 0 10px rgba(147, 197, 253, 0.6));
#     }
#     @keyframes rotate {
#         from { transform: rotate(0deg); }
#         to { transform: rotate(360deg); }
#     }
#     .stButton>button {
#         width: 100%;
#         height: 3.2em;
#         border-radius: 16px;
#         background: linear-gradient(90deg, #3b82f6, #8b5cf6);
#         color: white;
#         font-weight: bold;
#         font-size: 18px;
#         border: none;
#         transition: all 0.3s ease;
#     }
#     .stButton>button:hover {
#         transform: scale(1.05);
#         box-shadow: 0 10px 30px rgba(59, 130, 246, 0.5);
#     }
#     .metric-card {
#         background: rgba(255,255,255,0.08);
#         padding: 24px;
#         border-radius: 16px;
#         border: 1px solid rgba(148, 163, 184, 0.2);
#         text-align: center;
#         transition: transform 0.3s;
#     }
#     .metric-card:hover {
#         transform: translateY(-5px);
#     }
#     .churn-high { color: #f87171; font-size: 2rem; font-weight: bold; }
#     .churn-low { color: #4ade80; font-size: 2rem; font-weight: bold; }
# </style>
# """, unsafe_allow_html=True)

# # ====================== ANIMATED LOGO ======================
# st.sidebar.markdown("""
#     <div style="text-align: center; margin-bottom: 20px;">
#         <img src="https://img.icons8.com/3d-fluency/100/shield.png" class="rotating-logo">
#     </div>
# """, unsafe_allow_html=True)

# st.sidebar.title("ChurnGuard AI")
# st.sidebar.markdown("**AI-Powered Customer Retention**")
# st.sidebar.divider()

# # ====================== TITLE ======================
# st.markdown("""
#     <h1 style='text-align:center; margin-bottom:0;'>
#         🛡️ ChurnGuard AI
#     </h1>
#     <p style='text-align:center; font-size:22px; color:#94a3b8;'>
#         Intelligent Telecom Customer Retention System
#     </p>
# """, unsafe_allow_html=True)

# # ====================== REST OF YOUR CODE (Same as before) ======================
# file_path = "churn_dataset.csv"

# if not os.path.exists(file_path):
#     st.error("❌ Dataset not found! Please place `churn_dataset.csv` in the same folder.")
#     st.stop()

# df = pd.read_csv(file_path)

# # Data Preprocessing
# df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
# df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

# if 'customerID' in df.columns:
#     df.drop('customerID', axis=1, inplace=True)

# # Encoding
# label_encoders = {}
# for col in df.select_dtypes(include=['object']).columns:
#     le = LabelEncoder()
#     df[col] = le.fit_transform(df[col])
#     label_encoders[col] = le

# # Model Training
# X = df.drop('Churn', axis=1)
# y = df['Churn']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# model = LogisticRegression(max_iter=1000)
# model.fit(X_train_scaled, y_train)

# accuracy = accuracy_score(y_test, model.predict(X_test_scaled))

# # Sidebar Navigation
# page = st.sidebar.radio("Go to", ["Dashboard", "Prediction", "Analytics", "About"])

# # ====================== PAGES ======================
# if page == "Dashboard":
#     st.subheader("📊 Business Overview")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown(f"<div class='metric-card'><h4>Total Customers</h4><h1>{len(df):,}</h1></div>", unsafe_allow_html=True)
#     with col2:
#         churn_rate = round(df['Churn'].mean() * 100, 2)
#         st.markdown(f"<div class='metric-card'><h4>Churn Rate</h4><h1>{churn_rate}%</h1></div>", unsafe_allow_html=True)
#     with col3:
#         st.markdown(f"<div class='metric-card'><h4>Model Accuracy</h4><h1>{round(accuracy*100, 2)}%</h1></div>", unsafe_allow_html=True)

#     c1, c2 = st.columns([2, 1])
#     with c1:
#         fig1 = px.pie(df, names=df['Churn'].map({0:"Stayed", 1:"Churned"}), 
#                      title="Churn Distribution", hole=0.6,
#                      color_discrete_sequence=['#4ade80', '#f87171'])
#         st.plotly_chart(fig1, use_container_width=True)

#     with c2:
#         fig2 = px.histogram(df, x='MonthlyCharges', color=df['Churn'].map({0:"Stayed", 1:"Churned"}),
#                            title="Monthly Charges Distribution", 
#                            color_discrete_sequence=['#4ade80', '#f87171'])
#         st.plotly_chart(fig2, use_container_width=True)

# elif page == "Prediction":
#     # (Your prediction code remains same - I kept it short for brevity)
#     st.subheader("🔮 Real-time Churn Prediction")
#     # ... [Keep your existing prediction form code here] ...

#     # Example result (you can keep your full prediction logic)
#     if st.button("🚀 Predict Churn Risk"):
#         st.success("✅ Prediction Logic Works! (Add your full prediction code here)")

# elif page == "Analytics":
#     st.subheader("📊 Advanced Analytics")
#     fig = px.box(df, x='Churn', y='MonthlyCharges', color='Churn')
#     st.plotly_chart(fig, use_container_width=True)

# else:
#     st.subheader("About ChurnGuard AI")
#     st.info("Premium Animated Dashboard with Rotating Logo")

# st.markdown("---")
# st.markdown("<p style='text-align:center; color:#64748b;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)