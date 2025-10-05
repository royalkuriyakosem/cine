import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useProduction } from '../../context/ProductionContext';
import { Select } from '../ui/Select';
import { Button } from '../ui/Button';
import ProductionForm from '../../features/productions/ProductionForm';
import { addProduction } from '../../api/productions';

const Header = () => {
    const { user, logout } = useAuth();
    const { productions, selectedProduction, setSelectedProduction, refreshProductions } = useProduction();
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleProductionChange = (e) => {
        const prodId = parseInt(e.target.value, 10);
        const newSelection = productions.find(p => p.id === prodId);
        setSelectedProduction(newSelection);
    };

    const handleSaveProduction = async (formData) => {
        await addProduction(formData);
        refreshProductions(); // Refresh the list in the context
        setIsModalOpen(false);
    };

    return (
        <header className="flex items-center justify-between px-6 py-4 bg-white border-b-2 border-gray-200">
            <div className="flex items-center">
                <h2 className="text-xl font-semibold text-gray-800 mr-4">Dashboard</h2>
                {productions.length > 0 && selectedProduction && (
                    <Select
                        name="production_selector"
                        value={selectedProduction.id}
                        onChange={handleProductionChange}
                    >
                        {productions.map(prod => (
                            <option key={prod.id} value={prod.id}>{prod.title}</option>
                        ))}
                    </Select>
                )}
                <Button onClick={() => setIsModalOpen(true)} size="sm" className="ml-4">New Production</Button>
            </div>
            <div className="flex items-center">
                <div className="relative">
                    <span className="mr-4 font-medium text-gray-700">{user?.username} ({user?.role})</span>
                    <button
                        onClick={logout}
                        className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring"
                    >
                        Logout
                    </button>
                </div>
            </div>
            {isModalOpen && <ProductionForm onClose={() => setIsModalOpen(false)} onSave={handleSaveProduction} />}
        </header>
    );
};

export default Header;