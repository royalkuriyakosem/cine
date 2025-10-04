import api from './axiosConfig';

export const getVFXShots = async (productionId) => {
    try {
        const response = await api.get(`/vfx/shots/?production=${productionId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching VFX shots for production ${productionId}:`, error.response?.data || error.message);
        throw error;
    }
};

export const getShotVersions = async (vfxShotId) => {
    try {
        const response = await api.get(`/vfx/versions/?vfx_shot=${vfxShotId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching versions for VFX shot ${vfxShotId}:`, error.response?.data || error.message);
        throw error;
    }
};

export const uploadVFXVersion = async (vfxShotId, file, notes) => {
    const formData = new FormData();
    formData.append('vfx_shot', vfxShotId);
    formData.append('file', file);
    formData.append('notes', notes);
    // The version number would typically be calculated on the backend.
    // Sending a placeholder or letting the backend handle it is best.
    
    try {
        const response = await api.post('/vfx/versions/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error(`Error uploading version for VFX shot ${vfxShotId}:`, error.response?.data || error.message);
        throw error;
    }
};