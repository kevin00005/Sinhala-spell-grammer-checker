import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def check_text(text):
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Check the following Sinhala text for verb conjugation errors based on these rules:
    
    1. For plural subjects/passengers (බහුවචනය,මගීන්): 
       - Convert verbs to end with ෝය (e.g., කළාය -> කලෝය, ගියේය -> ගියෝය)
    
    2. For first person (මම):
       - Convert verbs to end with මි (e.g., කලාය -> කලෙමි, ගියේය -> ගියෙමි)
    
    3. For first person plural (අපි):
       - Convert verbs to end with මු (e.g., කලාය -> කලෙමු, ගියේය -> ගියෙමු)
    
    4. For feminine subjects (අක්කා,අම්මා):
       - Convert verbs to end with ාය/ේය (e.g., කලෙමි -> කලේය, ගියෙමි -> ගියාය)
    
    5. For masculine subjects (අයියා,මල්ලී):
       - Convert verbs to end with ේය (e.g., ගියෙමි -> ගියේය, කලාය -> කලේය)
    
    6. For third person masculine (ඔහු):
       - Convert verbs to end with ෝය (e.g., ගියෙමි -> ගියෝය, කලේය -> කලෝය)

    Text to check: {text}
    
    Identify the subject of each sentence and check if the verb forms match these rules.
    Provide corrections in Sinhala with brief explanations for each error found.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("සිංහල ව්‍යාකරණ පරීක්ෂකය")
    
    user_text = st.text_area("වාක්‍ය ලියන්න:", height=150)
    
    if st.button("පරීක්ෂා කරන්න"):
        if user_text:
            with st.spinner("පරීක්ෂා කරමින්..."):
                result = check_text(user_text)
                st.markdown("### වෙනස්කම්:")
                st.write(result)
        else:
            st.warning("කරුණාකර පරීක්ෂා කිරීමට වාක්‍ය ලියන්න.")

if __name__ == "__main__":
    main()