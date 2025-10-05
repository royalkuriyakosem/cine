import React from 'react';
import WeekCard from './WeekCard';
import './Schedule.css';

const WeeklyView = ({ weeklyData, onSelectWeek }) => {
  return (
    <div className="scroll-container">
      {weeklyData.map(week => (
        <WeekCard key={week.weekNumber} weekData={week} onSelect={onSelectWeek} />
      ))}
    </div>
  );
};

export default WeeklyView;