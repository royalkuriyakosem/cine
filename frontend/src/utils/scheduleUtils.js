export const groupDataByWeek = (data) => {
  if (!data || data.length === 0) {
    return [];
  }

  const weeks = [];
  let currentWeek = [];

  data.forEach((day, index) => {
    currentWeek.push(day);
    if ((index + 1) % 7 === 0 || (index + 1) === data.length) {
      weeks.push(currentWeek);
      currentWeek = [];
    }
  });

  return weeks.map((weekDays, index) => {
    const totalScenes = weekDays.reduce((acc, day) => acc + day.scenes.length, 0);
    const primaryLocations = [...new Set(weekDays.map(day => day.location))];

    return {
      weekNumber: index + 1,
      startDate: weekDays[0].date,
      endDate: weekDays[weekDays.length - 1].date,
      numberOfDays: weekDays.length,
      totalScenes,
      primaryLocations,
      days: weekDays,
    };
  });
};