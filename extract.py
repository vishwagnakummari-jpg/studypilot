import pdfplumber
import os
import json
from groq import Groq
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
load_dotenv()
#print("API Key =", os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_syllabus(text):

    prompt = f"""
    Your prompt here...

    Syllabus text:

    {text}
    """

    print("BEFORE GROQ")

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=4000
        )

        print("AFTER GROQ")

    except Exception as e:
        print("GROQ ERROR:", str(e))
        raise

    return response.choices[0].message.content   

def clean_json_response(raw):
    start = raw.find("[")
    end = raw.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("No JSON found")
    
    return raw[start : end +1]


def main():
    text = extract_text_from_pdf("1781168803616-019eb5ef-0f20-7000-9c71-5f9d921cf2cd-sample_syllabus_for_studypilot.pdf")
    raw_output = extract_syllabus(text)
    cleaned = clean_json_response(raw_output)
    print(cleaned)
    data = json.loads(cleaned)
    with open("syllabus.json","w") as f:
        json.dump(data, f, indent=2)
    print("Json has been written properly")

if __name__ == "__main__":
    main()
    
      
