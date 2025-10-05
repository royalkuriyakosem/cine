import google.generativeai as genai
import os
import json
import logging

logger = logging.getLogger(__name__)

class AIScheduleGenerator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_schedule(self, script_text: str):
        prompt = """
        Act as an expert film director and seasoned production manager. Your task is to analyze the provided film script and create a highly realistic, efficient, and optimized shooting schedule as a JSON array.

        **Primary Goal:** Create a logistically sound schedule that minimizes company moves by grouping scenes based on location.

        **JSON Structure Requirements:**
        Your entire output MUST be a single JSON array. Each object in the array represents one shooting day and must have the following structure and data types:
        - id: integer (sequential, starting from 1)
        - day: integer (sequential, starting from 1)
        - date: string in 'YYYY-MM-DD' format (start from today's date)
        - location: string
        - generalCall: string in 'HH:MM' format
        - firstShot: string in 'HH:MM' format
        - estWrap: string in 'HH:MM' format
        - weather: string (a brief prediction)
        - sunrise: string in 'HH:MM' format
        - sunset: string in 'HH:MM' format
        - notes: string
        - scenes: array of scene objects, each with { sceneNumber: string, description: string, cast: array of strings, startTime: string 'HH:MM', endTime: string 'HH:MM' }
        - castCalls: array of cast call objects, each with { character: string, actor: 'TBD', status: string ('W', 'SW', or 'H'), hmw: string 'HH:MM', onSet: string 'HH:MM' }

        **Special Instruction:** In the 'notes' field of the VERY FIRST day object, you must provide a project summary. This summary should include your expert prediction for the **total number of shooting days** required for the entire script and a brief mention of the biggest production risks.
        """
        
        try:
            response = self.model.generate_content([prompt, script_text])
            # Clean up the response to extract the JSON
            text_response = response.text
            json_str = text_response.replace("```json", "").replace("```", "").strip()
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Error generating schedule with AI: {e}")
            raise

def generate_schedule_from_script(script_text: str):
    generator = AIScheduleGenerator()
    return generator.generate_schedule(script_text)