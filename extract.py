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
Extract the syllabus and return ONLY valid JSON.

Example:

[
  {{
    "unit": "Unit 1",
    "topics": [
      "Topic 1",
      "Topic 2"
    ]
  }}
]

Return only JSON.
Do not return explanations.
Do not return markdown.
Do not return code fences.

Syllabus text:

{text}
"""


    print("BEFORE GROQ")

    try:
        print("Prompt length:", len(prompt))

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=2000
        )

        print("AFTER GROQ")

        if not response.choices:
            raise ValueError("No response received from GROQ")

        result = response.choices[0].message.content

        print("Response length:", len(result))

        return result

    except Exception as e:
        print("GROQ ERROR:", str(e))
        raise

   
def clean_json_response(raw):

    raw = raw.replace("```json", "")
    raw = raw.replace("```", "")
    raw = raw.strip()

    start = raw.find("[")
    end = raw.rfind("]")

    if start == -1 or end == -1:
        raise ValueError("No JSON array found in response")

    return raw[start:end + 1]


def main():
    text = extract_text_from_pdf(
        "1781168803616-019eb5ef-0f20-7000-9c71-5f9d921cf2cd-sample_syllabus_for_studypilot.pdf"
    )

    raw_output = extract_syllabus(text)

    print("\n===== RAW OUTPUT =====")
    print(raw_output)

    cleaned = clean_json_response(raw_output)

    print("\n===== CLEANED OUTPUT =====")
    print(cleaned)

    try:
        data = json.loads(cleaned)
    except Exception as e:
        print("\nJSON ERROR:", e)
        print("\nACTUAL CONTENT:")
        print(cleaned)
        return

    with open("syllabus.json", "w") as f:
        json.dump(data, f, indent=2)

    print("JSON has been written properly")

if __name__ == "__main__":
    main()
    
      
