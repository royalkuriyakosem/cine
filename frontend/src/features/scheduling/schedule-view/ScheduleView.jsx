import React, { useState } from 'react';
import DayCard from './DayCard';
import DetailedCallSheet from './DetailedCallSheet';
import './ScheduleView.css';

const ScheduleView = ({ scheduleData }) => {
    const [selectedDayId, setSelectedDayId] = useState(null);

    const handleSelectDay = (dayId) => setSelectedDayId(dayId);
    const handleBack = () => setSelectedDayId(null);

    const selectedDayData = scheduleData.find(d => d.id === selectedDayId);

    if (selectedDayData) {
        return <DetailedCallSheet dayData={selectedDayData} onBack={handleBack} />;
    }

    return (
        <div className="schedule-container">
            <div className="schedule-header">
                <h3>Daily View</h3>
                {/* View toggles can be added here if needed */}
            </div>
            <div className="scroll-container">
                {scheduleData.map(day => (
                    <DayCard key={day.id} dayData={day} onSelect={handleSelectDay} />
                ))}
            </div>
        </div>
    );
};

export default ScheduleView;