import React from 'react';
import VFXBoard from '../features/post-production/VFXBoard';
import AssetManager from '../features/vfx/AssetManager';
import { useProduction } from '../context/ProductionContext';

const PostProduction = () => {
    const { selectedProduction } = useProduction();

    if (!selectedProduction) {
        return <div>Please select a production to begin.</div>;
    }

    return (
        <div className="container mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Post-Production: {selectedProduction.title}</h1>
            <div className="grid grid-cols-1 gap-8">
                <VFXBoard productionId={selectedProduction.id} />
                <AssetManager productionId={selectedProduction.id} />
            </div>
        </div>
    );
};

export default PostProduction;