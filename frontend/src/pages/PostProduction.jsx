import React from 'react';
import VFXBoard from '../features/post-production/VFXBoard';

const PostProduction = () => {
    const currentProductionId = 1;
    return (
        <div className="container mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Post-Production</h1>
            <div className="grid grid-cols-1 gap-8">
                <VFXBoard productionId={currentProductionId} />
            </div>
        </div>
    );
};

export default PostProduction;