import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import ProtectedRoute from '../../components/ProtectedRoute';
import { Card } from '../../components/ui/Card';
import { FileUpload } from '../../components/ui/FileUpload';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { breakdownScript } from '../../api/productions';

const ScriptBreakdown = ({ productionId }) => {
    const [file, setFile] = useState(null);
    const [breakdown, setBreakdown] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleFileChange = (selectedFile) => {
        setFile(selectedFile);
        setBreakdown(null);
        setError('');
    };

    const handleAnalyzeClick = async () => {
        if (!file || !productionId) {
            setError('Please select a script file and ensure a production is selected.');
            return;
        }

        setIsLoading(true);
        setError('');

        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                const scriptText = event.target.result;
                const result = await breakdownScript(productionId, scriptText);
                setBreakdown(result);
            } catch (err) {
                setError('Failed to analyze script. The backend service may be unavailable.');
            } finally {
                setIsLoading(false);
            }
        };
        reader.onerror = () => {
            setError('Failed to read the file.');
            setIsLoading(false);
        };
        reader.readAsText(file);
    };

    const BreakdownCategory = ({ title, items }) => (
        <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-2">{title}</h4>
            {items && items.length > 0 ? (
                <ul className="list-disc list-inside bg-gray-50 p-3 rounded-md space-y-1">
                    {items.map((item, index) => (
                        <li key={index} className="text-gray-600">{item}</li>
                    ))}
                </ul>
            ) : (
                <p className="text-gray-500 italic">None identified.</p>
            )}
        </div>
    );

    return (
        <Card>
            <h3 className="text-xl font-bold mb-4 text-gray-800">Script Breakdown</h3>
            
            <ProtectedRoute allowedRoles={['PRODUCER', 'ADMIN']}>
                <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
                    <FileUpload onFileSelect={handleFileChange} accept=".txt,.md" />
                    <Button onClick={handleAnalyzeClick} disabled={isLoading || !file}>
                        {isLoading ? <Spinner /> : 'Analyze Script'}
                    </Button>
                    {error && <p className="text-red-500 mt-2">{error}</p>}
                </div>
            </ProtectedRoute>

            {breakdown && (
                <div className="mt-6 space-y-6">
                    <h3 className="text-lg font-semibold border-b pb-2">Analysis Results</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <BreakdownCategory title="Characters" items={breakdown.characters} />
                        <BreakdownCategory title="Props" items={breakdown.props} />
                        <BreakdownCategory title="Locations" items={breakdown.locations} />
                        <BreakdownCategory title="Stunts" items={breakdown.stunts} />
                        <BreakdownCategory title="Special Effects" items={breakdown.special_effects} />
                    </div>
                </div>
            )}
        </Card>
    );
};

export default ScriptBreakdown;