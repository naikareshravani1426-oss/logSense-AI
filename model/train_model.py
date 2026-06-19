import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

random.seed(42)
data = []

# MEDICAL LOGS
for _ in range(300):
    spo2 = random.randint(75, 99)
    sys = random.randint(70, 140)
    dia = random.randint(40, 90)
    hr = random.randint(60, 140)
    data.append({
        'text': f'SpO2 {spo2}% oxygen saturation BP {sys}/{dia} heart rate {hr} bpm patient monitoring',
        'label': 'medical'
    })

data.append({'text': 'patient oxygen level critical blood pressure dropping emergency code blue', 'label': 'medical'})
data.append({'text': 'blood glucose 32 mg/dL hypoglycemia seizure risk unconscious', 'label': 'medical'})
data.append({'text': 'temperature 104F sepsis suspected white blood cell count high', 'label': 'medical'})
data.append({'text': 'BP 180/110 severe hypertension stroke risk headache vision blur', 'label': 'medical'})
data.append({'text': 'heart rate 142 bpm irregular rhythm chest pain reported', 'label': 'medical'})
data.append({'text': 'patient unconscious oxygen level 82% emergency ventilation required', 'label': 'medical'})
data.append({'text': 'blood pressure 70/40 septic shock suspected critical condition', 'label': 'medical'})
data.append({'text': 'heart rate 180 bpm ventricular tachycardia detected', 'label': 'medical'})
data.append({'text': 'temperature 104F severe fever infection suspected', 'label': 'medical'})
data.append({'text': 'blood sugar 420 diabetic ketoacidosis emergency', 'label': 'medical'})
data.append({'text': 'stroke symptoms facial droop slurred speech detected', 'label': 'medical'})
data.append({'text': 'oxygen saturation 78% respiratory distress immediate intervention', 'label': 'medical'})
data.append({'text': 'patient cyanosis low oxygen severe breathing difficulty', 'label': 'medical'})
data.append({'text': 'heart rate irregular atrial fibrillation high risk', 'label': 'medical'})
data.append({'text': 'blood pressure 190/120 hypertensive crisis emergency', 'label': 'medical'})
data.append({'text': 'severe chest pain ECG abnormal myocardial infarction suspected', 'label': 'medical'})
data.append({'text': 'glucose 35 mg/dL patient unresponsive hypoglycemia', 'label': 'medical'})
data.append({'text': 'oxygen saturation dropping despite oxygen support', 'label': 'medical'})
data.append({'text': 'respiratory failure mechanical ventilation recommended', 'label': 'medical'})
data.append({'text': 'sepsis markers elevated infection spreading rapidly', 'label': 'medical'})
data.append({'text': 'cardiac arrest code blue activated immediately', 'label': 'medical'})
data.append({'text': 'persistent fever 105F infection not responding treatment', 'label': 'medical'})
data.append({'text': 'oxygen saturation 81% blood pressure unstable critical patient', 'label': 'medical'})
data.append({'text': 'neurological deficit possible stroke urgent imaging required', 'label': 'medical'})
data.append({'text': 'patient stable vital signs normal recovery progressing', 'label': 'medical'})

# MACHINE LOGS
for _ in range(300):
    temp = random.randint(60, 110)
    vib = round(random.uniform(1.0, 12.0), 1)
    rpm = random.randint(1000, 3000)
    data.append({
        'text': f'motor temperature {temp}C vibration {vib}mm/s RPM {rpm} bearing fault detected',
        'label': 'machine'
    })

data.append({'text': 'conveyor belt stopped motor fault pressure valve failure emergency stop', 'label': 'machine'})
data.append({'text': 'hydraulic pressure exceeding limit pump failure imminent shutdown', 'label': 'machine'})
data.append({'text': 'coolant temperature critical engine overheat shutdown initiated', 'label': 'machine'})
data.append({'text': 'gearbox oil pressure low lubrication failure risk detected', 'label': 'machine'})
data.append({'text': 'compressor pressure safety valve opened emergency stop activated', 'label': 'machine'})
data.append({'text': 'bearing lubrication failure vibration exceeding threshold', 'label': 'machine'})
data.append({'text': 'coolant flow lost engine overheating shutdown triggered', 'label': 'machine'})
data.append({'text': 'hydraulic leak pressure dropped below safe level', 'label': 'machine'})
data.append({'text': 'compressor overload current spike detected', 'label': 'machine'})
data.append({'text': 'gearbox vibration abnormal maintenance required', 'label': 'machine'})
data.append({'text': 'conveyor motor stalled emergency stop activated', 'label': 'machine'})
data.append({'text': 'pump cavitation detected flow instability increasing', 'label': 'machine'})
data.append({'text': 'bearing temperature rising rapidly failure imminent', 'label': 'machine'})
data.append({'text': 'oil pressure critically low lubrication system fault', 'label': 'machine'})
data.append({'text': 'rotor imbalance excessive vibration shutdown recommended', 'label': 'machine'})
data.append({'text': 'cooling fan failure motor temperature increasing', 'label': 'machine'})
data.append({'text': 'valve blockage reducing system throughput significantly', 'label': 'machine'})
data.append({'text': 'hydraulic cylinder response delayed pressure instability', 'label': 'machine'})
data.append({'text': 'gear wear detected abnormal acoustic signature', 'label': 'machine'})
data.append({'text': 'compressor discharge temperature above safe range', 'label': 'machine'})
data.append({'text': 'shaft misalignment causing excessive vibration', 'label': 'machine'})
data.append({'text': 'machine startup successful all parameters normal', 'label': 'machine'})
data.append({'text': 'production line halted actuator communication lost', 'label': 'machine'})
data.append({'text': 'emergency shutdown activated due to thermal overload', 'label': 'machine'})
data.append({'text': 'motor current spike indicates winding damage', 'label': 'machine'})

# IT LOGS
for _ in range(300):
    cpu = random.randint(50, 100)
    mem = random.randint(50, 100)
    errors = random.randint(0, 1000)
    data.append({
        'text': f'CPU {cpu}% memory {mem}% HTTP 500 errors {errors} server issue detected',
        'label': 'it'
    })

data.append({'text': 'server down connection timeout database unreachable 503 error', 'label': 'it'})
data.append({'text': 'disk usage 98% write operations failing system crash imminent', 'label': 'it'})
data.append({'text': 'memory leak detected heap size critical out of memory kill', 'label': 'it'})
data.append({'text': 'SSL certificate expired authentication failures login blocked', 'label': 'it'})
data.append({'text': 'database connection pool exhausted max connections reached', 'label': 'it'})
data.append({'text': 'database connection pool exhausted service unavailable', 'label': 'it'})
data.append({'text': 'application crashed due to null pointer exception', 'label': 'it'})
data.append({'text': 'network timeout while contacting upstream server', 'label': 'it'})
data.append({'text': 'authentication failed invalid token received', 'label': 'it'})
data.append({'text': 'disk usage 99 percent storage exhausted', 'label': 'it'})
data.append({'text': 'docker container restarted unexpectedly', 'label': 'it'})
data.append({'text': 'service unavailable dependency endpoint not responding', 'label': 'it'})
data.append({'text': 'memory leak detected heap allocation continuously growing', 'label': 'it'})
data.append({'text': 'cpu throttling triggered due to sustained load', 'label': 'it'})
data.append({'text': 'database deadlock causing transaction failures', 'label': 'it'})
data.append({'text': 'api gateway returning 502 bad gateway errors', 'label': 'it'})
data.append({'text': 'redis cache unavailable fallback mode activated', 'label': 'it'})
data.append({'text': 'ssl certificate expired secure connections failing', 'label': 'it'})
data.append({'text': 'message queue backlog increasing consumer lag detected', 'label': 'it'})
data.append({'text': 'kernel out of memory killer terminated process', 'label': 'it'})
data.append({'text': 'web server healthy response time within limits', 'label': 'it'})
data.append({'text': 'dns resolution failed for external dependency', 'label': 'it'})
data.append({'text': 'backup process failed insufficient storage space', 'label': 'it'})
data.append({'text': 'load balancer health checks failing repeatedly', 'label': 'it'})
data.append({'text': 'unexpected service restart detected in production', 'label': 'it'})

# Save CSV
df = pd.DataFrame(data)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'training_data.csv')
df.to_csv(csv_path, index=False)
print(f'Generated {len(df)} rows!')
print(df['label'].value_counts())

# Train Model
X = df['text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=3000,
        ngram_range=(1,3),
        stop_words='english',
        lowercase=True)),
    ('clf', RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight='balanced')),
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print('\nAccuracy:', accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

from sklearn.metrics import confusion_matrix
print('\nConfusion Matrix:')
print(confusion_matrix(y_test, y_pred))

# Save Model
pkl_path = os.path.join(BASE_DIR, 'classifier.pkl')
joblib.dump(pipeline, pkl_path)
print('classifier.pkl saved!')

# Quick Test
tests = [
    'SpO2 84% oxygen low BP 88/52 heart rate 118',
    'motor temperature 94C bearing fault vibration high',
    'CPU 97% memory full HTTP 500 errors server crash',
]
print('\nQuick Test:')
for log in tests:
    pred = pipeline.predict([log])[0]
    conf = int(pipeline.predict_proba([log]).max() * 100)
    print(f'  {pred.upper()} ({conf}%) <- {log[:50]}')