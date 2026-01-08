import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Check if model exists
try:
    model = joblib.load('fault_detector.pkl')
    st.success("✅ Model loaded successfully!")
except:
    st.error("❌ fault_detector.pkl NOT FOUND! Copy from Jupyter folder.")
    st.stop()

st.title("⚡ AI Power Fault Detector")
st.markdown("Enter voltages/currents below:")

# Simple inputs
col1, col2 = st.columns(2)
Va = col1.slider("Va (Voltage A)", 0.0, 2.0, 1.0)
Vb = col1.slider("Vb (Voltage B)", 0.0, 2.0, 1.0) 
Vc = col1.slider("Vc (Voltage C)", 0.0, 2.0, 1.0)
Ia = col2.slider("Ia (Current A)", 0.0, 10.0, 1.0)
Ib = col2.slider("Ib (Current B)", 0.0, 10.0, 1.0)
Ic = col2.slider("Ic (Current C)", 0.0, 10.0, 1.0)

if st.button("🔍 DETECT FAULT", use_container_width=True):
    features = ['Va', 'Vb', 'Vc', 'Ia', 'Ib', 'Ic']
    measurement = pd.DataFrame([[Va,Vb,Vc,Ia,Ib,Ic]], columns=features)
    
    pred = model.predict(measurement)[0]
    probs = model.predict_proba(measurement)[0]
    
    faults = {0:"✅ Normal", 1:"⚠️ LG Fault", 2:"⚠️ LL Fault", 3:"🚨 3PH Fault"}
    
    st.markdown(f"### **RESULT: {faults[pred]}**")
    st.markdown(f"**Confidence: {max(probs)*100:.1f}%**")
    
    st.balloons()  # Celebration!
