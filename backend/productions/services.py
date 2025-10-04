import re
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class ScriptAnalysisService:
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

def analyze_script(text: str) -> Dict[str, List[str]]:
    """
    Wrapper function for script analysis.
    This is where we could swap in different analysis implementations.
    """
    analyzer = ScriptAnalysisService()
    return analyzer.analyze_script(text)