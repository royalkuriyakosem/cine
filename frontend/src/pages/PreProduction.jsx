import React from 'react';
import ScriptBreakdown from '../features/pre-production/ScriptBreakdown';
import BudgetManager from '../features/pre-production/BudgetManager';

const PreProduction = () => {
    // A production ID would typically come from a selector or URL parameter
    const currentProductionId = 1; 

    return (
        <div className="container mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Pre-Production</h1>
            <div className="grid grid-cols-1 gap-8">
                <ScriptBreakdown productionId={currentProductionId} />
                <BudgetManager productionId={currentProductionId} />
            </div>
        </div>
    );
};

export default PreProduction;