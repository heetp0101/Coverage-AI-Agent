import os
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import json
import time
from google.api_core import exceptions

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Defining the schema exactly as requested by the assignment
class Suggestion(BaseModel):
    target_bin: str
    priority: str
    difficulty: str
    suggestion: str
    test_outline: List[str]
    dependencies: List[str]
    reasoning: str

class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion]

def get_all_suggestions(full_parsed_data):
    # We pass the WHOLE JSON as context
    prompt = f"""
    You are a Silicon Verification Expert.
    Below is a Functional Coverage Report for a {full_parsed_data['design']}.
    
    CONTEXT:
    {json.dumps(full_parsed_data, indent=3)}
    
    TASK:
    1. Analyze the uncovered_bins and cross_coverage gaps.
    2. Generate specific test scenarios to close these gaps.
    3. For each suggestion, provide priority, difficulty, and a technical test outline.
    """

# Try up to 3 times if we hit a quota limit
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': SuggestionsResponse,
                }
            )
            return response.parsed
        
        except exceptions.ResourceExhausted as e:
            print(f"Quota exceeded! Waiting 60 seconds before retrying... (Attempt {attempt + 1}/3)")
            time.sleep(60) # Wait a full minute for the quota to reset
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
    return None


if __name__ == "__main__":
    # 1. Get the data from our new parser
    from main import parse_coverage
    data = parse_coverage("report.txt")
    

    #get only first covergroup
    # data["covergroups"] = [data["covergroups"][0]]

    covergroups = data["covergroups"]

    data["covergroups"] = data["covergroups"][0:1]

    data["covergroups"][0]["coverpoints"] = data["covergroups"][0]["coverpoints"][0:1]
   
    data["covergroups"][0]["coverpoints"][0]["bins"] = data["covergroups"][0]["coverpoints"][0]["bins"][0:2]

    coverpoints = covergroups[0]["coverpoints"][0]

    bins = coverpoints["bins"][0:2]


    data["uncovered_bins"] = data["uncovered_bins"][0:4]

    data["cross_coverage"] = data["cross_coverage"][0:1]

    print(json.dumps(data, indent=3))


       # 2. Get AI suggestions
    print("Generating Suggestions from Gemini...")


    final_output = get_all_suggestions(data)
    
    # 3. Print the result
    print(final_output.model_dump_json(indent=2))