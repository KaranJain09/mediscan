import re
import os
import requests
import json
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Recommendation prompt template (unchanged)
improved_prompt_template = PromptTemplate(
    input_variables=["report"],
    template="""You are a compassionate, highly knowledgeable virtual health assistant with expertise in hematology and diagnostics. Your task is to carefully review and analyze the blood report details provided below. Provide a detailed and structured response that includes:

1. **Potential Health Concerns:**
   - Identify any abnormal values or trends.
   - Explain possible medical conditions or areas that may require further investigation.

2. **Medication Guidance (General Information Only):**
   - Suggest potential medications or treatments that might be considered.
   - Clearly state that these suggestions are general guidance and not a substitute for professional medical advice.

3. **Diet and Lifestyle Recommendations:**
   - Provide actionable advice on dietary modifications.
   - Suggest lifestyle changes to improve overall health and well-being.

Please present your analysis in a clear, organized format using bullet points or numbered lists where appropriate.

**Blood Report Details:**
{report}
"""
)

# Updated health metrics prompt template with escaped curly braces for literal JSON structure.
health_metrics_prompt_template = PromptTemplate(
    input_variables=["report"],
    template="""You are a compassionate and highly knowledgeable virtual health assistant. Your task is to analyze the following blood test report details and extract key health metrics in a structured JSON format. The JSON should have the following format:

{{
  "metrics": [
    {{
      "name": "Metric Name",
      "value": numeric value,
      "unit": "unit if applicable",
      "normal_range": [min_value, max_value]
    }},
    ...
  ]
}}

Please only include metrics that are mentioned in the report and ensure that the values are extracted accurately. If a metric is not present or cannot be determined, omit it.

**Blood Report Details:**
{report}

Respond only with the JSON object.
"""
)

def validate_blood_report(text: str) -> bool:
    """Check if the text appears to be a blood report by looking for key terms."""
    keywords = [
        "hemoglobin", "RBC", "WBC", "platelets", "MCV", "MCH",
        "creatinine", "bilirubin", "dengue", "IgG", "IgM", "ELISA",
        "antibody", "infection", "glucose", "cholesterol"
    ]
    return any(re.search(rf"\b{keyword}\b", text, re.IGNORECASE) for keyword in keywords)

def generate_recommendations(text: str) -> str:
    """Generate structured health recommendations if the text appears to be a blood report."""
    if not validate_blood_report(text):
        return "⚠️ This tool is designed for analyzing blood reports only. Please upload a valid blood report."
    
    formatted_prompt = improved_prompt_template.format(report=text)
    messages = [
        {"role": "system", "content": formatted_prompt}
    ]
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_completion_tokens": 512
    }
    url = "https://api.groq.com/openai/v1/chat/completions"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        return f"Error: API call failed with status code {response.status_code}. Response: {response.text}"
    
    result = response.json()
    return result.get("choices", [{}])[0].get("message", {}).get("content", "No completion found.")

# In agent.py, update generate_health_metrics function
def generate_health_metrics(text: str) -> str:
    """Generate structured health metrics analysis in JSON format based on the blood report."""
    if not validate_blood_report(text):
        return '{"metrics": []}'
    
    formatted_prompt = health_metrics_prompt_template.format(report=text)
    messages = [
        {"role": "system", "content": formatted_prompt}
    ]
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_completion_tokens": 1024  # Increased from 512
    }
    url = "https://api.groq.com/openai/v1/chat/completions"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        return '{"metrics": []}'
    
    result = response.json()
    print(result)  # Keep for debugging
    return result.get("choices", [{}])[0].get("message", {}).get("content", '{"metrics": []}')
