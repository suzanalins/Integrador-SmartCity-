import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const LocalList = () => {
    const [locais, setLocais] = useState([]);
    const [filtro, setFiltro] = useState('');
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    useEffect(() => {
        loadLocais();
    }, []);

    const loadLocais = async () => {
        const res = await api.get('locais/');
        setLocais(res.data);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Tem certeza que deseja excluir este local?')) {
            await api.delete(`locais/${id}/`);
            loadLocais();
        }
    };

    const filtered = locais.filter(l => 
        l.local.toLowerCase().includes(filtro.toLowerCase())
    );

    return (
        <div>
            <div className="page-header">
                <h2>Locais</h2>
                {user?.is_superuser && (
                    <button className="btn-primary" onClick={() => navigate('/locais/novo')}>
                        + Novo Local
                    </button>
                )}
            </div>
            
            <input
                type="text"
                placeholder="Filtrar locais..."
                value={filtro}
                onChange={(e) => setFiltro(e.target.value)}
                className="filter-input"
            />
            
            <table className="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Local</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {filtered.map(local => (
                        <tr key={local.id}>
                            <td>{local.id}</td>
                            <td>{local.local}</td>
                            <td>
                                <button onClick={() => navigate(`/locais/editar/${local.id}`)}>✏️</button>
                                {user?.is_superuser && (
                                    <button onClick={() => handleDelete(local.id)}>🗑️</button>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default LocalList;