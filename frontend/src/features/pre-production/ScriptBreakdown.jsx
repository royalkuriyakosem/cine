import React, { useState } from 'react';
import ProtectedRoute from '../../components/ProtectedRoute';
import { Card } from '../../components/ui/Card';
import { FileUpload } from '../../components/ui/FileUpload';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import DailyView from '../scheduling/components/DailyView';
import WeeklyView from '../scheduling/components/WeeklyView';
import CalendarView from '../scheduling/components/CalendarView';
import { groupDataByWeek } from '../../utils/scheduleUtils';

const ScriptBreakdown = ({ productionId }) => {
    const [file, setFile] = useState(null);
    const [schedule, setSchedule] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [view, setView] = useState('daily');
    const [currentWeekIndex, setCurrentWeekIndex] = useState(0);

    const weeklyData = React.useMemo(() => 
        schedule ? groupDataByWeek(schedule) : [], [schedule]
    );

    const handleFileChange = (selectedFile) => {
        setFile(selectedFile);
        setSchedule(null);
        setError('');
    };

    const handleAnalyzeClick = async () => {
        if (!file || !productionId) {
            setError('Please select a script file and ensure a production is selected.');
            return;
        }

        setIsLoading(true);
        setError('');
        
        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                const scriptText = event.target.result;
                const result = await breakdownScript(productionId, scriptText);
                setSchedule(result);
            } catch (err) {
                setError('Failed to analyze script. Please try again.');
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };
        reader.readAsText(file);
    };

    const handleNextWeek = () => {
        setCurrentWeekIndex(prev => Math.min(prev + 1, weeklyData.length - 1));
    };

    const handlePrevWeek = () => {
        setCurrentWeekIndex(prev => Math.max(prev - 1, 0));
    };

    return (
        <Card>
            <h3 className="text-xl font-bold mb-4">AI-Powered Schedule Generator</h3>
            
            <ProtectedRoute allowedRoles={['PRODUCER', 'ADMIN']}>
                <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
                    <p className="text-sm text-gray-600">
                        Upload a script file to generate a production schedule using AI.
                    </p>
                    <FileUpload onFileSelect={handleFileChange} accept=".txt,.md" />
                    <Button onClick={handleAnalyzeClick} disabled={isLoading || !file}>
                        {isLoading ? <Spinner /> : 'Generate Schedule'}
                    </Button>
                    {error && <p className="text-red-500 mt-2">{error}</p>}
                </div>
            </ProtectedRoute>

            {schedule && (
                <div className="mt-6">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-semibold">Generated Schedule</h3>
                        <div className="space-x-2">
                            <Button 
                                onClick={() => setView('daily')}
                                className={view === 'daily' ? 'bg-blue-600' : ''}
                            >
                                Daily
                            </Button>
                            <Button 
                                onClick={() => setView('weekly')}
                                className={view === 'weekly' ? 'bg-blue-600' : ''}
                            >
                                Weekly
                            </Button>
                            <Button 
                                onClick={() => setView('calendar')}
                                className={view === 'calendar' ? 'bg-blue-600' : ''}
                            >
                                Calendar
                            </Button>
                        </div>
                    </div>

                    {view === 'daily' && (
                        <DailyView scheduleData={schedule} onSelectDay={() => {}} />
                    )}
                    {view === 'weekly' && (
                        <WeeklyView weeklyData={weeklyData} onSelectWeek={() => {}} />
                    )}
                    {view === 'calendar' && (
                        <CalendarView 
                            weekData={weeklyData[currentWeekIndex]}
                            onPrevWeek={handlePrevWeek}
                            onNextWeek={handleNextWeek}
                            isFirstWeek={currentWeekIndex === 0}
                            isLastWeek={currentWeekIndex === weeklyData.length - 1}
                        />
                    )}
                </div>
            )}
        </Card>
    );
};

export default ScriptBreakdown;

export const breakdownScript = async (productionId, scriptText) => {
    try {
        // Call the Node.js AI service endpoint
        const response = await fetch('http://localhost:3001/api/generate-schedule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scriptText })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const schedule = await response.json();
        return schedule;
    } catch (error) {
        console.error("Error breaking down script:", error);
        throw error;
    }
};