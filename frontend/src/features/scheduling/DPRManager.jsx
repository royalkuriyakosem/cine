import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { getDPRs, addDPR } from '../../api/scheduling';
import DPRForm from './DPRForm';

const DPRManager = ({ productionId }) => {
    const [dprs, setDprs] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const fetchDPRs = () => {
        if (productionId) {
            setIsLoading(true);
            getDPRs(productionId)
                .then(res => setDprs(res.data))
                .finally(() => setIsLoading(false));
        }
    };

    useEffect(fetchDPRs, [productionId]);

    const handleSave = async (formData) => {
        await addDPR({ ...formData, production: productionId });
        setIsModalOpen(false);
        fetchDPRs();
    };

    if (isLoading) return <Spinner />;

    return (
        <Card>
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold mb-4">Daily Production Reports</h3>
                <Button onClick={() => setIsModalOpen(true)}>Add DPR</Button>
            </div>
            <ul className="mt-4 space-y-2">
                {dprs.map(dpr => (
                    <li key={dpr.id} className="p-2 border rounded">
                        DPR for {dpr.dpr_date}
                    </li>
                ))}
            </ul>
            {isModalOpen && <DPRForm onClose={() => setIsModalOpen(false)} onSave={handleSave} />}
        </Card>
    );
};

export default DPRManager;