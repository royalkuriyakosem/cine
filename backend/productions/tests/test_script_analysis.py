from django.test import TestCase
from productions.services import analyze_script

class ScriptAnalysisTests(TestCase):
    def test_basic_script_analysis(self):
        test_script = """
        INT. OFFICE - DAY
        
        JOHN sits at his desk. He picks up a coffee mug.
        
        JOHN:
        Another day at the office.
        
        SARAH enters. She fights with a copy machine.
        
        EXT. PARKING LOT - NIGHT
        
        A car magically transforms into a robot (VFX).
        """

        breakdown = analyze_script(test_script)

        self.assertIn('JOHN', breakdown['characters'])
        self.assertIn('SARAH', breakdown['characters'])
        self.assertIn('OFFICE', breakdown['locations'])
        self.assertIn('PARKING LOT', breakdown['locations'])
        self.assertIn('Mug', breakdown['props'])
        self.assertIn('Fights - EXT. PARKING LOT - NIGHT', breakdown['stunts'])
        self.assertIn('Transforms - EXT. PARKING LOT - NIGHT', breakdown['special_effects'])

    def test_empty_script(self):
        breakdown = analyze_script("")
        self.assertEqual(breakdown['characters'], [])
        self.assertEqual(breakdown['locations'], [])
        self.assertEqual(breakdown['props'], [])
        self.assertEqual(breakdown['stunts'], [])
        self.assertEqual(breakdown['special_effects'], [])

    def test_complex_scene_heading(self):
        test_script = """
        INT./EXT. MOVING CAR - SUNSET
        
        DRIVER grabs the steering wheel.
        """
        
        breakdown = analyze_script(test_script)
        self.assertIn('MOVING CAR', breakdown['locations'])
        self.assertIn('DRIVER', breakdown['characters'])
        self.assertIn('Wheel', breakdown['props'])