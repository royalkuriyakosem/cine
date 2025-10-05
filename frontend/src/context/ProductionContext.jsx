import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../api/axiosConfig';

const ProductionContext = createContext();

export const useProduction = () => useContext(ProductionContext);

export const ProductionProvider = ({ children }) => {
    const [productions, setProductions] = useState([]);
    const [selectedProduction, setSelectedProduction] = useState(null);

    const fetchProductions = () => {
        // CORRECTED: The endpoint for the Production model is /productions/productions/
        api.get('/productions/productions/')
            .then(res => {
                setProductions(res.data);
                if (res.data.length > 0 && !selectedProduction) {
                    setSelectedProduction(res.data[0]);
                }
            })
            .catch(err => console.error("Failed to fetch productions:", err));
    };

    useEffect(() => {
        fetchProductions();
    }, []);

    const value = {
        productions,
        selectedProduction,
        setSelectedProduction,
        refreshProductions: fetchProductions, // Expose the fetch function
    };

    return (
        <ProductionContext.Provider value={value}>
            {children}
        </ProductionContext.Provider>
    );
};