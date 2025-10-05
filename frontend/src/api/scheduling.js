import api from './axiosConfig';

// Call Sheets
export const getCallSheets = (productionId) => api.get(`/call-sheets/?production=${productionId}`);
export const addCallSheet = (data) => api.post('/call-sheets/', data);
export const publishCallSheet = (id) => api.post(`/call-sheets/${id}/publish/`);
export const getCallSheetPDF = (id) => api.get(`/call-sheets/${id}/pdf/`, { responseType: 'blob' });

// Daily Production Reports (DPRs)
export const getDPRs = (productionId) => api.get(`/dprs/?production=${productionId}`);
export const addDPR = (data) => api.post('/dprs/', data);