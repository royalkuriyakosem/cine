import React from 'react';

const timeToGridRow = (timeStr) => {
  if (!timeStr) return 0;
  const [hours, minutes] = timeStr.split(':').map(Number);
  const totalHours = hours + minutes / 60;
  return (totalHours - 6) * 2 + 2;
};

const CalendarView = ({ weekData, onPrevWeek, onNextWeek, isFirstWeek, isLastWeek }) => {
  if (!weekData) {
    return <div className="detail-view">No data for this week.</div>;
  }

  const timeSlots = Array.from({ length: 17 }, (_, i) => {
    const hour = i + 6;
    return `${hour.toString().padStart(2, '0')}:00`;
  });
  
  const formatDate = (dateString) => new Date(dateString).toLocaleDateString('en-US', { day: 'numeric', month: 'short'});

  return (
    <div className="calendar-view-container">
      <div className="calendar-header">
        <h2>Weekly Calendar: Week {weekData.weekNumber}</h2>
        <div className="calendar-nav">
          <button onClick={onPrevWeek} disabled={isFirstWeek} className="back-btn">&larr; Prev</button>
          <button onClick={onNextWeek} disabled={isLastWeek} className="back-btn">Next &rarr;</button>
        </div>
      </div>
      <div className="calendar-grid">
        {/* Calendar implementation */}
      </div>
    </div>
  );
};

export default CalendarView;