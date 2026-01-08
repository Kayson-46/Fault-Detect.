from flask import Flask, request, render_template_string
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('fault_detector.pkl')

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    confidence = None
    if request.method == 'POST':
        # Get form inputs
        data = [float(request.form[f]) for f in ['Va','Vb','Vc','Ia','Ib','Ic']]
        df_input = pd.DataFrame([data], columns=['Va','Vb','Vc','Ia','Ib','Ic'])
        
        pred = model.predict(df_input)[0]
        probs = model.predict_proba(df_input)[0]
        confidence = max(probs) * 100
        
        fault_names = {0:'✅ Normal Operation', 
                      1:'⚠️ Line-to-Ground Fault', 
                      2:'⚠️ Line-to-Line Fault', 
                      3:'🚨 Three-Phase Fault'}
        prediction = fault_names[pred]
    
    html = '''
    <!DOCTYPE html>
    <html><head><title>AI Power Fault Detector</title>
    <style>body{font-family:Arial;background:#1a1a2e;color:#fff;padding:50px;max-width:600px;margin:auto;}
    input{width:100px;padding:10px;margin:5px;font-size:16px;}
    button{background:#0f3460;color:white;padding:12px 30px;border:none;font-size:16px;cursor:pointer;}
    .result{background:#16213e;padding:20px;margin-top:20px;border-radius:10px;font-size:20px;}</style></head>
    <body>
    <h1>⚡ AI Power System Fault Detector</h1>
    <p>Enter per-unit voltages and currents:</p>
    <form method="post">
        <div>Va: <input name="Va" value="1.0" step="0.01" required> 
        Vb: <input name="Vb" value="1.0" step="0.01" required> 
        Vc: <input name="Vc" value="1.0" step="0.01" required></div>
        <div>Ia: <input name="Ia" value="1.0" step="0.01" required> 
        Ib: <input name="Ib" value="1.0" step="0.01" required> 
        Ic: <input name="Ic" value="1.0" step="0.01" required></div>
        <br><button>🔍 Detect Fault</button>
    </form>
    {% if prediction %}
        <div class="result">{{ prediction }} <br> 
        Confidence: {{ "%.1f"|format(confidence) }}%</div>
    {% endif %}
    </body></html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
