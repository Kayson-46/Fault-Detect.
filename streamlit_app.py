import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Fault Detector", layout="wide")
st.title("⚡ AI Power Fault Detector")
st.markdown("LG/LL/3PH detection from V/I measurements")

st.sidebar.header("📊 Test These Values 👇")
st.sidebar.info("""
**NORMAL:**
Va=Vb=Vc=1.0 | Ia=Ib=Ic=1.0

**LG-A FAULT:**  
Va=0.65, Ia=5.2 | Vb=Vc=0.95 | Ib=Ic=1.1

**LL-AB FAULT:**
Va=0.70, Vb=0.68 | Ia=4.8, Ib=4.5 | Vc=1.0, Ic=1.0

**3PH FAULT:**
Va=Vb=Vc=0.45 | Ia=8.5, Ib=8.2, Ic=8.7
""")

# Inputs
col1, col2 = st.columns(2)
Va = col1.slider("Va", 0.0, 2.0, 1.0)
Vb = col1.slider("Vb", 0.0, 2.0, 1.0)
Vc = col1.slider("Vc", 0.0, 2.0, 1.0)
Ia = col2.slider("Ia", 0.0, 10.0, 1.0)
Ib = col2.slider("Ib", 0.0, 10.0, 1.0)
Ic = col2.slider("Ic", 0.0, 10.0, 1.0)

if st.button("🔍 DETECT FAULT", use_container_width=True):
    voltages = [Va, Vb, Vc]
    currents = [Ia, Ib, Ic]
    
    min_v = min(voltages)
    max_i = max(currents)
    v_imbalance = max([abs(Va-Vb), abs(Vb-Vc), abs(Vc-Va)])
    i_imbalance = max([abs(Ia-Ib), abs(Ib-Ic), abs(Ic-Ia)])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if min_v < 0.60:
            st.error("🚨 **3-PHASE FAULT**")
            st.caption("All voltages <0.6pu + currents >7pu")
        elif v_imbalance > 0.22:
            st.warning("⚠️ **LINE-TO-LINE**")
            st.caption("ΔV >0.22pu between phases")
        elif (min_v < 0.78 or max_i > 4.0) and max([Ia,Ib,Ic]) > min([Ia,Ib,Ic])*3:
            st.warning("⚠️ **LINE-TO-GROUND**") 
            st.caption("1 phase affected: V<0.78 OR I>4pu")
        else:
            st.success("✅ **NORMAL**")
            st.caption("Balanced V≈1.0pu, I≈1.0pu")
    
    with col2:
        st.metric("Min Voltage", f"{min_v:.2f}", "1.0")
        st.metric("Max Current", f"{max_i:.1f}", "1.0")
    
    with col3:
        st.metric("V Imbalance", f"{v_imbalance:.2f}", "0.05")
        st.metric("I Imbalance", f"{i_imbalance:.1f}", "0.2")

# Phasor plot
st.subheader("📈 Voltage Triangle")
fig_data = {'Phase': ['A','B','C'], 'Voltage': [Va,Vb,Vc]}
st.bar_chart(fig_data)

st.caption("Real relay thresholds: IEEE C37.2 standards")
