import React from 'react';
import LiveShootBoard from '../features/production/LiveShootBoard';
// Import other production components here as they are built

const Production = () => {
    // A production ID would typically come from a selector or URL parameter
    const currentProductionId = 1;

    return (
        <div className="container mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Production</h1>
            <div className="grid grid-cols-1 gap-8">
                <LiveShootBoard productionId={currentProductionId} />
                {/* Other components like CallSheets and CrewCheckins would go here */}
            </div>
        </div>
    );
};

export default Production;