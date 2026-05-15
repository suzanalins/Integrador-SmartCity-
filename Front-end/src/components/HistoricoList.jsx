import React, { useState, useEffect } from 'react';
import api from '../services/api';

const HistoricoList = () => {
    const [historicos, setHistoricos] = useState([]);
    const [filtro, setFiltro] = useState('');

    useEffect(() => {
        loadHistoricos();
    }, []);

    const loadHistoricos = async () => {
        const res = await api.get('historicos/');
        setHistoricos(res.data);
    };

    const filtered = historicos.filter(h => 
        h.sensor?.toString().includes(filtro)
    );

    return (
        <div>
            <h2>Histórico de Medições</h2>
            <input
                type="text"
                placeholder="Filtrar por ID do sensor..."
                value={filtro}
                onChange={(e) => setFiltro(e.target.value)}
                className="filter-input"
            />
            
            <table className="data-table">
                <thead>
                    <tr><th>ID</th><th>Sensor</th><th>Valor</th><th>Data/Hora</th></tr>
                </thead>
                <tbody>
                    {filtered.map(h => (
                        <tr key={h.id}>
                            <td>{h.id}</td>
                            <td>{h.sensor}</td>
                            <td>{h.valor}</td>
                            <td>{new Date(h.time_stamp).toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default HistoricoList;