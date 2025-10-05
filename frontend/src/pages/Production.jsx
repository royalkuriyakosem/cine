import React from 'react';
import LiveShootBoard from '../features/production/LiveShootBoard';
import CallSheetManager from '../features/scheduling/CallSheetManager';
import DPRManager from '../features/scheduling/DPRManager';
import { useProduction } from '../context/ProductionContext';

const Production = () => {
    const { selectedProduction } = useProduction();

    if (!selectedProduction) {
        return <div>Please select a production to begin.</div>;
    }

    return (
        <div className="container mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Production: {selectedProduction.title}</h1>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="lg:col-span-2">
                    <LiveShootBoard productionId={selectedProduction.id} />
                </div>
                <CallSheetManager productionId={selectedProduction.id} />
                <DPRManager productionId={selectedProduction.id} />
            </div>
        </div>
    );
};

export default Production;