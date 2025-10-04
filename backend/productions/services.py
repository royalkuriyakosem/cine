import re
import json
import openai
from typing import Dict, List, Any
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class AIScriptAnalysisService:
    """
    Service for analyzing script text using OpenAI's GPT API.
    """
    
    def __init__(self):
        # Only pass api_key, do NOT pass timeout, max_retries, or proxies
        self.client = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def analyze_script(self, text: str) -> Dict[str, List[str]]:
        """
        Analyze script text using GPT to extract production elements.
        """
        try:
            # Prepare the prompt
            prompt = f"""Analyze this screenplay excerpt and extract the following elements:
            1. Characters (speaking roles and mentioned characters)
            2. Locations (both interior and exterior)
            3. Props (objects that characters interact with)
            4. Stunts (any physical action sequences)
            5. Special Effects (visual effects, practical effects, or magical elements)

            Format the response as a JSON object with these keys: characters, locations, props, stunts, special_effects
            Each value should be a list of strings.

            Screenplay text:
            {text}
            """

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional script supervisor analyzing a screenplay."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )

            # Parse the response
            result = response.choices[0].message.content
            return json.loads(result)

        except Exception as e:
            logger.error(f"Error in AI script analysis: {str(e)}")
            # Fall back to basic analysis if AI fails
            return BasicScriptAnalysisService().analyze_script(text)

class BasicScriptAnalysisService:
    """
    Service for analyzing script text and extracting production elements.
    Currently uses basic regex patterns - TODO: Replace with NLP/LLM integration.
    """
    
    def __init__(self):
        # Basic patterns - these would be much more sophisticated with NLP/LLM
        self.character_pattern = r'^([A-Z]{2,}):?' # Matches lines in all caps followed by optional colon
        self.location_pattern = r'(?:INT\.|EXT\.) ([^.!?\n]+)'
        self.props_keywords = ['holds', 'picks up', 'grabs', 'carries', 'puts down', 'with a']
        self.stunts_keywords = ['fights', 'jumps', 'falls', 'crashes', 'explosion']
        self.fx_keywords = ['CGI', 'VFX', 'effect', 'magical', 'transforms', 'appears', 'disappears']

    def analyze_script(self, text: str) -> Dict[str, List[str]]:
        """
        Analyze script text and return breakdown of elements.
        
        TODO: Replace this basic implementation with calls to:
        1. OpenAI GPT API for sophisticated text analysis
        2. Custom NLP model trained on screenplay format
        3. Industry standard script parsing service
        """
        lines = text.split('\n')
        
        # Initialize collections with deduplication
        characters = set()
        locations = set()
        props = set()
        stunts = set()
        special_effects = set()

        current_scene = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Find characters (basic: looks for ALL CAPS dialogue headers)
            character_match = re.match(self.character_pattern, line)
            if character_match:
                char = character_match.group(1)
                if len(char) > 2 and char not in ['INT', 'EXT']:  # Basic filtering
                    characters.add(char.title())

            # Find locations (basic: looks for INT./EXT. headers)
            location_match = re.search(self.location_pattern, line)
            if location_match:
                locations.add(location_match.group(1).strip())
                current_scene = line

            # Look for props, stunts, and effects in action lines
            lower_line = line.lower()
            
            # Props (basic: looks for specific verbs and prepositions)
            for keyword in self.props_keywords:
                if keyword in lower_line:
                    # Extract the object of the action (very basic)
                    words = lower_line.split(keyword)[1].split()
                    if words:
                        props.add(words[0].title())

            # Stunts (basic: keyword matching)
            for keyword in self.stunts_keywords:
                if keyword in lower_line:
                    stunts.add(f"{keyword.title()} - {current_scene}")

            # Special Effects (basic: keyword matching)
            for keyword in self.fx_keywords:
                if keyword in lower_line:
                    special_effects.add(f"{keyword.title()} - {current_scene}")

        return {
            'characters': sorted(list(characters)),
            'locations': sorted(list(locations)),
            'props': sorted(list(props)),
            'stunts': sorted(list(stunts)),
            'special_effects': sorted(list(special_effects))
        }

def analyze_script(text: str, use_ai: bool = True) -> Dict[str, List[str]]:
    """
    Wrapper function for script analysis.
    Falls back to basic analysis if AI is disabled or fails.
    """
    if use_ai and hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
        analyzer = AIScriptAnalysisService()
    else:
        analyzer = BasicScriptAnalysisService()
    return analyzer.analyze_script(text)