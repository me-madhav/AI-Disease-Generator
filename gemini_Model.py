import os
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
def chatBot(symptoms_text):
    client = genai.Client(
        api_key = os.getenv("GEMINI_API_KEY")
    )
    
    
    
    det = f"""You are a medical assistant AI designed for preliminary health risk assessment. 

                A user will provide a list of symptoms. Based on those symptoms, your task is to:

                1. Predict the most likely disease.
                2. Determine the risk level (Low, Medium, or High).
                3. Clearly explain why this disease is predicted based on the symptoms.
                4. Provide practical advice on what the user should do next.

                Important guidelines:
                - Do NOT claim this is a final medical diagnosis.
                - Keep the explanation simple and easy to understand.
                - Consider common diseases relevant to India (e.g., Dengue, Malaria, Flu, COVID-19, etc.).
                - If symptoms are unclear or insufficient, say that the result is uncertain.

                User Symptoms:
                {symptoms_text}

                Output format (strictly follow this):

                Disease: <Predicted Disease Name>
                Risk Level: <Low / Medium / High>
                Explanation: <Simple reasoning based on symptoms>
                Advice: <What the user should do next>
                
                Rules:
                1. use new line and spacing between lines as needed
                2. Don't use any special symbol
                """
                
                
    response = client.models.generate_content(
        
        model="gemini-3-flash-preview", contents= det
    )
    return(response.text)
