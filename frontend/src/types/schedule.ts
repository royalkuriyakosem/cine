export interface Scene {
    sceneNumber: string;
    description: string;
    cast: string[];
    startTime?: string;
    endTime?: string;
}

export interface CastCall {
    character: string;
    actor: string;
    status: 'W' | 'SW' | 'H';
    hmw: string;
    onSet: string;
}

export interface DaySchedule {
    id: number;
    day: number;
    date: string;
    location: string;
    generalCall: string;
    firstShot: string;
    estWrap: string;
    weather: string;
    sunrise: string;
    sunset: string;
    notes: string;
    scenes: Scene[];
    castCalls: CastCall[];
}

export interface WeekSchedule {
    weekNumber: number;
    startDate: string;
    endDate: string;
    numberOfDays: number;
    totalScenes: number;
    primaryLocations: string[];
    days: DaySchedule[];
}