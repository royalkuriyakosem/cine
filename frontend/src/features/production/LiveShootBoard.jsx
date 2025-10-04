import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Spinner } from '../../components/ui/Spinner';
import { getScenesForProduction } from '../../api/productions';

const LiveShootBoard = ({ productionId }) => {
    const [scenes, setScenes] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    // NOTE: The backend Scene model does not have a 'status' field.
    // This state is managed on the frontend for demonstration purposes.
    const [sceneStatuses, setSceneStatuses] = useState({});
    const STATUSES = ['To Do', 'In Progress', 'Done'];

    useEffect(() => {
        const fetchScenes = async () => {
            if (!productionId) return;
            try {
                setIsLoading(true);
                const data = await getScenesForProduction(productionId);
                setScenes(data);
                // Initialize statuses
                const initialStatuses = data.reduce((acc, scene) => {
                    acc[scene.id] = 'To Do'; // Default status
                    return acc;
                }, {});
                setSceneStatuses(initialStatuses);
            } catch (err) {
                setError('Failed to load scenes.');
            } finally {
                setIsLoading(false);
            }
        };
        fetchScenes();
    }, [productionId]);

    const handleStatusChange = (sceneId, newStatus) => {
        setSceneStatuses(prev => ({ ...prev, [sceneId]: newStatus }));
        // In a real app, you would call an API to persist this change.
    };

    const SceneCard = ({ scene }) => (
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
            <h4 className="font-bold text-gray-800">Scene {scene.number}: {scene.title}</h4>
            <p className="text-sm text-gray-600">{scene.location}</p>
            <p className="text-xs text-gray-500 mt-1">{scene.pages} pages</p>
            <select
                value={sceneStatuses[scene.id] || 'To Do'}
                onChange={(e) => handleStatusChange(scene.id, e.target.value)}
                className="mt-4 block w-full p-2 border border-gray-300 rounded-md bg-white text-sm"
            >
                {STATUSES.map(status => (
                    <option key={status} value={status}>{status}</option>
                ))}
            </select>
        </div>
    );

    if (isLoading) return <Spinner />;
    if (error) return <p className="text-red-500">{error}</p>;

    return (
        <Card>
            <h3 className="text-xl font-bold mb-4 text-gray-800">Live Shoot Board</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {STATUSES.map(status => (
                    <div key={status} className="bg-gray-100 p-4 rounded-lg">
                        <h4 className="font-bold text-center mb-4 text-gray-700">{status}</h4>
                        <div className="space-y-4">
                            {scenes.filter(scene => sceneStatuses[scene.id] === status).map(scene => (
                                <SceneCard key={scene.id} scene={scene} />
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </Card>
    );
};

export default LiveShootBoard;