import re

# ==========================================
# AI System Prompt Template
# ==========================================
SYSTEM_PROMPT_TEMPLATE = """
You are AgriDSS_AI, a virtual agronomist. Answer the farmer's question based strictly on the Farmer Profile and Retrieved Context.

Farmer Profile:
{farmer_profile}

Retrieved Context:
{retrieved_context}

Rules:
1. Do not hallucinate specific treatments, chemical names, or diagnoses if they are missing from the Retrieved Context.
2. If the Retrieved Context lacks the specific answer, your Recommendation must state: "I cannot provide a definite diagnosis or recommendation based on the current data."
3. SAFE FALLBACK: To facilitate the farmer, if context is missing, your Actionable Steps MUST provide safe, general advisory guidance. Do not leave the farmer with zero actionable steps. Examples include advising them to consult a local agricultural extension officer, taking clear photos of the symptoms, or monitoring the crop closely. Do not apply treatments from the retrieved context if they do not directly solve the farmer's specific problem.
4. Avoid absolute diagnoses; use phrases like "Possible reasons include..."
5. Format your response exactly with these headings: Recommendation, Why, Actionable Steps, Sources.
"""

# ==========================================
# LLM Response Parser for Streamlit UI
# ==========================================
def parse_ai_response(ai_text):
    """
    Splits the raw markdown string from the LLM into a structured Python dictionary.
    This allows the Streamlit frontend to neatly display each section.
    """
    # Regex pattern to match the 4 headings, ignoring case, bolding (**), or hashes (###)
    pattern = r"(?i)\**#{0,3}\s*(Recommendation|Why|Actionable Steps|Sources):?\**"
    
    parts = re.split(pattern, ai_text)
    
    # Default fallback dictionary in case a section is missing from the LLM output
    parsed_dict = {
        "Recommendation": "Not provided.",
        "Why": "Not provided.",
        "Actionable Steps": "Not provided.",
        "Sources": "Not provided."
    }
    
    # re.split puts the matched heading at odd indices and the content at even indices
    for i in range(1, len(parts), 2):
        heading = parts[i].title().strip() 
        content = parts[i+1].strip()
        
        if heading in parsed_dict:
            parsed_dict[heading] = content
            
    return parsed_dict