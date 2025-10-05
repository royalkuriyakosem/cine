import React from 'react';
import DayCard from './DayCard';
import './Schedule.css';

const DailyView = ({ scheduleData, onSelectDay }) => {
  return (
    <div className="scroll-container">
      {scheduleData.map(day => (
        <DayCard key={day.id} dayData={day} onSelect={onSelectDay} />
      ))}
    </div>
  );
};

export default DailyView;