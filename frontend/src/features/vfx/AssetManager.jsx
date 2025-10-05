import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { getAssets, addAsset } from '../../api/vfx';
import AssetForm from './AssetForm';

const AssetManager = ({ productionId }) => {
    const [assets, setAssets] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const fetchAssets = () => {
        if (productionId) {
            setIsLoading(true);
            getAssets(productionId)
                .then(res => setAssets(res.data))
                .finally(() => setIsLoading(false));
        }
    };

    useEffect(fetchAssets, [productionId]);

    const handleSave = async (formData) => {
        await addAsset({ ...formData, production: productionId });
        setIsModalOpen(false);
        fetchAssets();
    };

    if (isLoading) return <Spinner />;

    return (
        <Card>
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold">VFX Assets</h3>
                <Button onClick={() => setIsModalOpen(true)}>Upload Asset</Button>
            </div>
            <ul className="mt-4 space-y-2">
                {assets.map(asset => (
                    <li key={asset.id} className="p-2 border rounded">
                        {asset.name} ({asset.asset_type})
                    </li>
                ))}
            </ul>
            {isModalOpen && <AssetForm onClose={() => setIsModalOpen(false)} onSave={handleSave} />}
        </Card>
    );
};

export default AssetManager;