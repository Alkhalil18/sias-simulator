import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# 1. Load data and train the AI
sms_data = pd.read_csv('combined_sms.csv')[['label', 'text']].dropna()
semantic_model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
    ('classifier', MultinomialNB())
])
semantic_model.fit(sms_data['text'], sms_data['label'])

# 2. Phase I: Heuristics
def heuristic_scanner(message):
    risk_score = 0
    if re.search(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', message):
        risk_score += 0.8
    for tld in [r'\.xyz', r'\.top', r'\.click', r'\.link', r'\.bit']:
        if re.search(tld, message, re.IGNORECASE):
            risk_score += 0.4
            break 
    return min(risk_score, 1.0)

# 3. Phase II: Neural Engine
def normalize_and_score_vibe(text):
    leetspeak_map = {'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '8': 'b', 'å£': '£'}
    clean_text = text.lower()
    for leet, normal in leetspeak_map.items():
        clean_text = clean_text.replace(leet, normal)
    return clean_text

def get_neural_score(cleaned_text):
    return semantic_model.predict_proba([cleaned_text])[0][1]

# 4. Phase III: Cloud Sandbox
def cloud_sandbox_analyze(url):
    if ".xyz" in url or ".top" in url: return 1.0 
    return 0.1 

def classify_message(score):
    if 0 <= score <= 3.9: return "Safe / Ham", "Normal delivery."
    elif 4.0 <= score <= 6.9: return "Suspicious", "Deliver with warning banner; links disabled."
    else: return "Critical / Smish", "Quarantined; user notified of blocked threat."

# ---> THIS IS THE MISSING FUNCTION YOUR APP IS LOOKING FOR <---
def sias_pipeline(text):
    r_h = heuristic_scanner(text)
    
    cleaned_text = normalize_and_score_vibe(text)
    r_n = get_neural_score(cleaned_text)
    
    financial_keywords = ['payment', 'bank', 'account', 'transfer', 'charge', 'deducted']
    has_financial = any(word in cleaned_text for word in financial_keywords)
    raw_num_string = text.replace(" ", "").replace("-", "")
    has_phone = bool(re.search(r'\d{10,}', raw_num_string))
    
    if has_financial and has_phone: r_n = max(r_n, 0.85) 
        
    urls = re.findall(r'https?://[^\s]+', text)
    r_u = 0.0
    
    if urls:
        r_u = cloud_sandbox_analyze(urls[0])
        unified_score = round((2.0 * r_h) + (3.0 * r_n) + (5.0 * r_u), 1)
    else:
        unified_score = round((4.0 * r_h) + (6.0 * r_n), 1)
        
    classification, action = classify_message(unified_score)
    
    return {
        "text": text,
        "heuristic_risk": round(r_h, 2),
        "neural_risk": round(r_n, 2),
        "url_risk": round(r_u, 2) if urls else "N/A",
        "final_score": unified_score,
        "classification": classification,
        "action": action
    }