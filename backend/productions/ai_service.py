import google.generativeai as genai
import os
import json
import logging
from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


logger = logging.getLogger(__name__)

class ProductionViewSet(viewsets.ModelViewSet):
    # ... existing code ...

    @action(detail=True, methods=['post'])
    def breakdown(self, request, pk=None):
        """Generate a production schedule from script text."""
        script_text = request.data.get('script_text')
        if not script_text:
            return Response(
                {"error": "script_text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            schedule_data = generate_schedule_from_script(script_text)
            
            # Save the breakdown
            production = self.get_object()
            ScriptBreakdown.objects.create(
                production=production,
                raw_text=script_text,
                schedule_data=schedule_data
            )

            return Response(schedule_data)
            
        except ValueError as e:
            logger.error(f"Value error in script breakdown: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in script breakdown: {str(e)}")
            return Response(
                {"error": "Failed to generate schedule"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )