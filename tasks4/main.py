import os
from dotenv import load_dotenv
from openai import OpenAI

def summarize_tasks():
    load_dotenv()  # Load .env file
    
    # Sample paragraph-length task descriptions
    descriptions = [
        "I need to prepare a comprehensive presentation for the quarterly board meeting next week. This includes gathering all the financial reports from the last three months, creating visualizations and charts to illustrate our progress, writing speaker notes for each slide, and rehearsing the entire presentation at least twice. I also need to coordinate with the finance team to ensure all numbers are accurate and up-to-date before the meeting.",
        
        "My goal is to organize the home office which has become cluttered over the past few months. This involves sorting through all the papers and documents, filing important ones and shredding old receipts, reorganizing the bookshelf by category, cleaning out the desk drawers, and setting up a better cable management system for all the electronics. I should also consider getting some storage boxes for items I don't use frequently."
    ]
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Loop through and summarize each description
    for i, description in enumerate(descriptions, 1):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the following task description as a short phrase (5 words or less)."},
                {"role": "user", "content": description}
            ]
        )
        
        summary = response.choices[0].message.content
        print(f"Task {i}: {summary}")

if __name__ == "__main__":
    summarize_tasks()