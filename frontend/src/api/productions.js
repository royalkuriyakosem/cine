import api from './axiosConfig';

export const breakdownScript = async (productionId, scriptText) => {
    try {
        // Call the AI service endpoint
        const response = await fetch('http://localhost:3001/api/generate-schedule', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scriptText })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const schedule = await response.json();
        
        // Save the generated schedule to backend
        await api.post(`/productions/productions/${productionId}/breakdown/`, {
            schedule_data: schedule,
            script_text: scriptText
        });

        return schedule;
    } catch (error) {
        console.error("Error breaking down script:", error);
        throw error;
    }
};

// CORRECTED: The endpoint for the Production model is /productions/productions/
export const addProduction = (data) => api.post('/productions/productions/', data);

// CORRECTED: The endpoint for the Scene model is /productions/scenes/
export const addScene = (data) => api.post('/productions/scenes/', data);

// CORRECTED: The endpoint for the Shot model is /productions/shots/
export const addShot = (data) => api.post('/productions/shots/', data);

export const getScenesForProduction = async (productionId) => {
    try {
        // CORRECTED: Added the required '/productions' prefix
        const response = await api.get(`/productions/scenes/?production=${productionId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching scenes for production ${productionId}:`, error.response?.data || error.message);
        throw error;
    }
};

export const getBudgetLines = async (productionId) => {
    try {
        // CORRECTED: Added the required '/productions' prefix
        const response = await api.get(`/productions/budget-lines/?production=${productionId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching budget lines:", error.response?.data || error.message);
        throw error;
    }
};

export const addBudgetLine = async (data) => {
    try {
        // CORRECTED: Added the required '/productions' prefix
        const response = await api.post('/productions/budget-lines/', data);
        return response.data;
    } catch (error) {
        console.error("Error adding budget line:", error.response?.data || error.message);
        throw error;
    }
};

export const updateBudgetLine = async (id, data) => {
    try {
        // CORRECTED: Added the required '/productions' prefix
        const response = await api.patch(`/productions/budget-lines/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error("Error updating budget line:", error.response?.data || error.message);
        throw error;
    }
};

export const deleteBudgetLine = async (id) => {
    try {
        // CORRECTED: Added the required '/productions' prefix
        await api.delete(`/productions/budget-lines/${id}/`);
    } catch (error) {
        console.error("Error deleting budget line:", error.response?.data || error.message);
        throw error;
    }
};

export const generatePrediction = async (productionId) => {
    try {
        // CORRECTED: The action is on the ProductionViewSet, which is at /productions/productions/
        const response = await api.post(`/productions/productions/${productionId}/predict-budget/`);
        return response.data;
    } catch (error) {
        console.error("Error generating budget prediction:", error.response?.data || error.message);
        throw error;
    }
};