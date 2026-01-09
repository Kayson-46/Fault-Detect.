import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Fault Detector", layout="wide")
st.title("⚡ AI Power System Fault Detection")

# Sidebar inputs (NO instructions)
st.sidebar.header("📊 Live Measurements")
col1, col2 = st.sidebar.columns(2)
Va = col1.slider("Voltage A (pu)", 0.0, 2.0, 1.0, 0.01)
Vb = col1.slider("Voltage B (pu)", 0.0, 2.0, 1.0, 0.01)
Vc = col1.slider("Voltage C (pu)", 0.0, 2.0, 1.0, 0.01)
Ia = col2.slider("Current A (pu)", 0.0, 10.0, 1.0, 0.1)
Ib = col2.slider("Current B (pu)", 0.0, 10.0, 1.0, 0.1)
Ic = col2.slider("Current C (pu)", 0.0, 10.0, 1.0, 0.1)

# Fault detection button
if st.button("🔍 DETECT FAULT", use_container_width=True):
    voltages = [Va, Vb, Vc]
    currents = [Ia, Ib, Ic]
    
    min_v = min(voltages)
    max_i = max(currents)
    v_imbalance = max([abs(Va-Vb), abs(Vb-Vc), abs(Vc-Va)])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if min_v < 0.60:
            st.error("🚨 **THREE-PHASE FAULT**")
        elif v_imbalance > 0.22:
            st.warning("⚠️ **LINE-TO-LINE FAULT**")
        elif min_v < 0.78 or max_i > 4.0:
            st.warning("⚠️ **LINE-TO-GROUND FAULT**")
        else:
            st.success("✅ **NORMAL OPERATION**")
    
    with col2:
        st.metric("Min Voltage", f"{min_v:.2f}", "1.00")
        st.metric("Max Current", f"{max_i:.1f}", "1.0")
    
    with col3:
        st.metric("Voltage Δ", f"{v_imbalance:.2f}", "0.05")

# Simple voltage plot
st.subheader("📈 Voltages")
st.bar_chart({'A': Va, 'B': Vb, 'C': Vc})

st.caption("Professional fault detection dashboard")
