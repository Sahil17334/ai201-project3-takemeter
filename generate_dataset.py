import csv
import json
import os
from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

prompt = """
Generate exactly 100 highly realistic Reddit comments from r/Cricket. 
Divide them evenly among these three categories:
1. 'analysis' (uses stats, pitch data, economy rates, player forms)
2. 'hot_take' (bold, angry, or controversial opinions without real proof)
3. 'reaction' (all caps, emotional, short, reacting to a wicket or boundary)

Return ONLY a valid JSON object containing an array under the key "comments", where each item has the keys "text" and "label".
"""

print("Generating data in batches to guarantee 200+ rows...")
all_comments = []
target_rows = 220

while len(all_comments) < target_rows:
    print(f"Current count: {len(all_comments)}/{target_rows}. Fetching another batch...")
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        data_str = response.choices[0].message.content
        data = json.loads(data_str)
        
        # Extract the list of comments safely
        batch = data.get("comments", [])
        all_comments.extend(batch)
        
    except Exception as e:
        print("Batch failed or hit a snag, retrying...", e)

# Save all accumulated comments to CSV
with open("cricket_takes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    for item in all_comments:
        writer.writerow([item.get("text", ""), item.get("label", "")])
        
print(f"✅ Mission accomplished! Saved {len(all_comments)} rows to cricket_takes.csv!")