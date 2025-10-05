import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { getCallSheets, publishCallSheet, getCallSheetPDF, addCallSheet } from '../../api/scheduling';
import CallSheetForm from './CallSheetForm';

const CallSheetManager = ({ productionId }) => {
    const [callSheets, setCallSheets] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const fetchCallSheets = () => {
        if (productionId) {
            setIsLoading(true);
            getCallSheets(productionId)
                .then(res => setCallSheets(res.data))
                .finally(() => setIsLoading(false));
        }
    };

    useEffect(fetchCallSheets, [productionId]);

    const handlePublish = async (id) => {
        await publishCallSheet(id);
        fetchCallSheets();
    };

    const handleViewPDF = async (id) => {
        const res = await getCallSheetPDF(id);
        const file = new Blob([res.data], { type: 'application/pdf' });
        const fileURL = URL.createObjectURL(file);
        window.open(fileURL);
    };

    const handleSave = async (formData) => {
        await addCallSheet({ ...formData, production: productionId });
        setIsModalOpen(false);
        fetchCallSheets();
    };

    if (isLoading) return <Spinner />;

    return (
        <Card>
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold">Call Sheets</h3>
                <Button onClick={() => setIsModalOpen(true)}>Add Call Sheet</Button>
            </div>
            <ul className="mt-4 space-y-2">
                {callSheets.map(cs => (
                    <li key={cs.id} className="flex justify-between items-center p-2 border rounded">
                        <span>Call Sheet for {cs.date}</span>
                        <div className="space-x-2">
                            <Button size="sm" onClick={() => handleViewPDF(cs.id)}>View PDF</Button>
                            {!cs.published && (
                                <Button size="sm" onClick={() => handlePublish(cs.id)}>Publish</Button>
                            )}
                        </div>
                    </li>
                ))}
            </ul>
            {isModalOpen && <CallSheetForm onClose={() => setIsModalOpen(false)} onSave={handleSave} />}
        </Card>
    );
};

export default CallSheetManager;