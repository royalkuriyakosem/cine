import React from 'react';

const DetailedCallSheet = ({ dayData, onBack }) => {
  if (!dayData) return <div className="detail-view">Loading...</div>;

  const formattedDate = new Date(dayData.date).toLocaleDateString('en-US', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });

  const getStatusClass = (status) => {
    switch (status) {
      case 'W': return 'status-wo';
      case 'SW': return 'status-sw';
      case 'H': return 'status-h';
      default: return '';
    }
  };

  return (
    <div className="detail-view">
      <button onClick={onBack} className="back-btn">&larr; Back to Schedule Overview</button>
      <div className="detail-header">
        <h2>Call Sheet: Day {dayData.day}</h2>
        <p>{formattedDate}</p>
      </div>
      <div className="detail-grid">
        <div className="detail-box"><h4>Location</h4><p>{dayData.location}</p></div>
        <div className="detail-box"><h4>General Call</h4><p>{dayData.generalCall}</p></div>
        <div className="detail-box"><h4>First Shot</h4><p>{dayData.firstShot}</p></div>
        <div className="detail-box"><h4>Est. Wrap</h4><p>{dayData.estWrap}</p></div>
        <div className="detail-box"><h4>Weather</h4><p>{dayData.weather}</p></div>
        <div className="detail-box"><h4>Sunrise / Sunset</h4><p>{dayData.sunrise} / {dayData.sunset}</p></div>
      </div>
      <div className="detail-section">
        <h3>Scheduled Scenes</h3>
        <div className="scene-list">
          {dayData.scenes.map(scene => (
            <div key={scene.sceneNumber} className="scene-item">
              <p><strong>Sc. {scene.sceneNumber} ({scene.startTime} - {scene.endTime}):</strong> {scene.description}</p>
              <p className="text-sm text-gray-600"><strong>Cast:</strong> {scene.cast.join(', ')}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="detail-section">
        <h3>Cast Calls</h3>
        <table className="cast-call-table">
          <thead>
            <tr><th>Character</th><th>Actor</th><th>Status</th><th>H/M/W</th><th>On Set</th></tr>
          </thead>
          <tbody>
            {dayData.castCalls.map(call => (
              <tr key={call.character}>
                <td>{call.character}</td><td>{call.actor}</td>
                <td><span className={`status-badge ${getStatusClass(call.status)}`}>{call.status}</span></td>
                <td>{call.hmw}</td><td>{call.onSet}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {dayData.notes && (
        <div className="detail-section">
          <h3>Notes</h3>
          <div className="detail-box"><p>{dayData.notes}</p></div>
        </div>
      )}
    </div>
  );
};

export default DetailedCallSheet;