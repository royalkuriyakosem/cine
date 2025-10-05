import React from 'react';

const WeekCard = ({ weekData, onSelect }) => {
  const formatDate = (dateString) => new Date(dateString).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });

  return (
    <div className="week-card" onClick={() => onSelect(weekData.weekNumber)}>
      <div className="card-header">
        <h3>Week {weekData.weekNumber}</h3>
        <span>{weekData.numberOfDays} Days</span>
      </div>
      <div className="card-info">
        <p><strong>Dates:</strong> {formatDate(weekData.startDate)} - {formatDate(weekData.endDate)}</p>
        <p><strong>Total Scenes:</strong> <span className="info-badge">{weekData.totalScenes}</span></p>
        <p><strong>Locations:</strong> {weekData.primaryLocations.slice(0, 2).join(', ')}...</p>
      </div>
    </div>
  );
};

export default WeekCard;