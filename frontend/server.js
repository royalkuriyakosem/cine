import express from 'express';
import cors from 'cors';
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json({ limit: '5mb' }));

if (!process.env.GEMINI_API_KEY) {
    console.error("\nError: GEMINI_API_KEY not found in environment variables");
    process.exit(1);
}

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" }); // Using more stable model

const cleanJsonString = (text) => {
    // Find the start and end of the JSON array
    const startIndex = text.indexOf('[');
    const endIndex = text.lastIndexOf(']');

    if (startIndex === -1 || endIndex === -1 || endIndex < startIndex) {
        throw new Error('Could not find a valid JSON array in the API response.');
    }

    // Extract the JSON part
    let jsonStr = text.substring(startIndex, endIndex + 1);

    return jsonStr;
};

const validateScheduleData = (data) => {
    if (!Array.isArray(data)) {
        throw new Error('Schedule must be an array');
    }

    data.forEach((day, index) => {
        const requiredFields = [
            'id', 'day', 'date', 'location', 'generalCall', 'firstShot', 
            'estWrap', 'weather', 'sunrise', 'sunset', 'notes', 
            'scenes', 'castCalls'
        ];

        requiredFields.forEach(field => {
            if (!(field in day)) {
                throw new Error(`Day ${index + 1} missing required field: ${field}`);
            }
        });
    });

    return data;
};

app.post('/api/generate-schedule', async (req, res) => {
    const { scriptText } = req.body;

    if (!scriptText) {
        return res.status(400).json({ error: 'Script text is required.' });
    }

    try {
        const prompt = `
            Act as an expert film director and production manager. Create a shooting schedule.
            Your response MUST be a valid JSON array, starting with '[' and ending with ']'. 
            Do not include any explanatory text, markdown, or anything else outside of the JSON array.
            Each object in the array represents a shooting day and must have this exact structure:
            {
                "id": number,
                "day": number,
                "date": "YYYY-MM-DD",
                "location": string,
                "generalCall": "HH:MM",
                "firstShot": "HH:MM",
                "estWrap": "HH:MM",
                "weather": string,
                "sunrise": "HH:MM",
                "sunset": "HH:MM",
                "notes": string,
                "scenes": [
                    {
                        "sceneNumber": string,
                        "description": string,
                        "cast": string[],
                        "startTime": "HH:MM",
                        "endTime": "HH:MM"
                    }
                ],
                "castCalls": [
                    {
                        "character": string,
                        "actor": string,
                        "status": "W"|"SW"|"H",
                        "hmw": "HH:MM",
                        "onSet": "HH:MM"
                    }
                ]
            }
        `;

        const result = await model.generateContent([prompt, scriptText]);
        const response = await result.response;
        const text = response.text();
        
        // Clean and parse the JSON
        const cleanedJson = cleanJsonString(text);
        const schedule = JSON.parse(cleanedJson);
        
        // Validate the schedule data
        const validatedSchedule = validateScheduleData(schedule);
        
        res.json(validatedSchedule);
    } catch (error) {
        console.error("Error generating schedule:", error);
        res.status(500).json({ 
            error: 'Failed to generate schedule',
            details: error.message
        });
    }
});

app.listen(port, () => {
    console.log(`AI Schedule Server running at http://localhost:3001`);
});