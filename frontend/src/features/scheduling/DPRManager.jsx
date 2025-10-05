import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { getDPRs } from '../../api/scheduling';

const DPRManager = ({ productionId }) => {
    const [dprs, setDprs] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (productionId) {
            getDPRs(productionId)
                .then(res => setDprs(res.data))
                .finally(() => setIsLoading(false));
        }
    }, [productionId]);

    if (isLoading) return <Spinner />;

    return (
        <Card>
            <h3 className="text-xl font-bold mb-4">Daily Production Reports</h3>
            <Button>Add DPR</Button>
            <ul className="mt-4 space-y-2">
                {dprs.map(dpr => (
                    <li key={dpr.id} className="p-2 border rounded">
                        DPR for {dpr.dpr_date}
                    </li>
                ))}
            </ul>
        </Card>
    );
};

export default DPRManager;