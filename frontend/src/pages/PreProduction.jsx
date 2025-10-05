import React from 'react';
import ScriptBreakdown from '../features/pre-production/ScriptBreakdown';
import BudgetManager from '../features/pre-production/BudgetManager';
import { useProduction } from '../context/ProductionContext';

const PreProduction = () => {
    const { selectedProduction } = useProduction();

    if (!selectedProduction) {
        return <div>Please select a production to begin.</div>;
    }

    return (
        <div className="container mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Pre-Production: {selectedProduction.title}</h1>
            <div className="grid grid-cols-1 gap-8">
                <ScriptBreakdown productionId={selectedProduction.id} />
                <BudgetManager productionId={selectedProduction.id} />
            </div>
        </div>
    );
};

export default PreProduction;