import joblib
import os
import json

# Load Shravani's ML Model
pipeline = joblib.load(os.path.join(os.path.dirname(__file__), 'classifier.pkl'))

def load_rules(domain: str) -> list:
    path = os.path.join(os.path.dirname(__file__), 'rules', f"{domain}.json")
    with open(path) as f:
        return json.load(f)

def match_rules(log_text: str, domain: str) -> dict:
    rules = load_rules(domain)
    log_text_lower = log_text.lower()
    best_match = None
    best_score = 0
    
    for rule in rules:
        hits = sum(1 for t in rule['triggers'] if t.lower() in log_text_lower)
        if hits > best_score:
            best_score = hits
            best_match = rule
            
    return best_match or rules[0]

def predict(log_text: str) -> dict:
    # 1. Ask ML model for the domain
    raw_domain = pipeline.predict([log_text])[0]
    
    # 2. Get the confidence score
    confidence = int(pipeline.predict_proba([log_text]).max() * 100)
    
    # 3. Match with your JSON rules
    match = match_rules(log_text, raw_domain)
    
    return {
        "domain": raw_domain,
        "severity": match['severity'],
        "confidence": confidence,
        "diagnosis": match['diagnosis'],
        "cause": match['cause'],
        "fix_steps": match['fix_steps'],
        "pattern_matched": match['name']
    }