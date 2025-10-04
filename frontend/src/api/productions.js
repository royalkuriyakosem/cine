import api from './axiosConfig';

export const breakdownScript = async (productionId, scriptText) => {
    try {
        const response = await api.post(`/productions/${productionId}/breakdown/`, {
            script_text: scriptText
        });
        return response.data;
    } catch (error) {
        console.error("Error breaking down script:", error.response?.data || error.message);
        throw error;
    }
};

export const getScenesForProduction = async (productionId) => {
    try {
        const response = await api.get(`/productions/scenes/?production=${productionId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching scenes for production ${productionId}:`, error.response?.data || error.message);
        throw error;
    }
};