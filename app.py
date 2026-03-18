from flask import Flask, render_template, request, jsonify
import gemini_Model

app = Flask(__name__)



# 🧠 Disease database (India-focused)
disease_data = {
    "Flu": ["fever", "cough", "body pain", "fatigue"],
    "Dengue": ["fever", "rash", "joint pain", "headache"],
    "Malaria": ["fever", "chills", "sweating", "headache"],
    "Covid-19": ["fever", "cough", "loss of smell", "breathing difficulty"],
    "Food Poisoning": ["vomiting", "diarrhea", "stomach pain"],
    "Migraine": ["headache", "nausea", "sensitivity to light"]
}

# 🔍 Prediction logic
def predict_disease(user_symptoms):
    best_match = None
    max_score = 0
    matched_symptoms = []

    for disease, symptoms in disease_data.items():
        common = list(set(user_symptoms) & set(symptoms))
        score = len(common)

        if score > max_score:
            max_score = score
            best_match = disease
            matched_symptoms = common

    return best_match, max_score, matched_symptoms


# 🚨 Risk logic
def get_risk(score):
    if score >= 3:
        return "High"
    elif score == 2:
        return "Medium"
    else:
        return "Low"

# 💡 Suggestion logic
def get_suggestion(risk):
    if risk == "High":
        return "⚠️ Consult a doctor immediately."
    elif risk == "Medium":
        return "Monitor symptoms and consult if condition worsens."
    else:
        return "Basic care and rest recommended."

# 🌐 Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    symptoms = data.get("symptoms", [])
    symptoms_text = data.get("symptoms_text", "")

    # Rule-based (optional fallback)
    disease, score, matched = predict_disease(symptoms)
    risk = get_risk(score)
    suggestion = get_suggestion(risk)

    # 🔥 CALL GEMINI HERE
    try:
        ai_result = gemini_Model.chatBot(symptoms_text)
    except Exception as e:
        ai_result = f"AI Error: {str(e)}"

    return jsonify({
        "disease": disease,
        "risk": risk,
        "matched": matched,
        "suggestion": suggestion,
        "ai_result": ai_result   # 👈 IMPORTANT
    })    

if __name__ == "__main__":
    app.run()