import React from 'react';

const DayCard = ({ dayData, onSelect }) => {
  return (
    <div className="day-card" onClick={() => onSelect(dayData.id)}>
      <div className="card-header">
        <h3>Day {dayData.day}</h3>
        <span>{new Date(dayData.date).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })}</span>
      </div>
      <div className="card-info">
        <p><strong>Location:</strong> {dayData.location}</p>
        <p><strong>Scenes:</strong> <span className="info-badge">{dayData.scenes.length}</span></p>
        <p><strong>Est. Wrap:</strong> {dayData.estWrap}</p>
      </div>
    </div>
  );
};

export default DayCard;