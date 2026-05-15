import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const AmbienteList = () => {
    const [ambientes, setAmbientes] = useState([]);
    const [filtro, setFiltro] = useState('');
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    useEffect(() => {
        loadAmbientes();
    }, []);

    const loadAmbientes = async () => {
        const res = await api.get('ambientes/');
        setAmbientes(res.data);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Tem certeza?')) {
            await api.delete(`ambientes/${id}/`);
            loadAmbientes();
        }
    };

    const filtered = ambientes.filter(a => 
        a.descricao?.toLowerCase().includes(filtro.toLowerCase()) ||
        a.local?.toString().includes(filtro)
    );

    // Buscar nomes dos locais e responsáveis
    const getLocalNome = (localId) => {
        // Isso seria ideal com um cache, mas por simplicidade
        return localId || 'N/A';
    };

    return (
        <div>
            <div className="page-header">
                <h2>Ambientes</h2>
                {user?.is_superuser && (
                    <button className="btn-primary" onClick={() => navigate('/ambientes/novo')}>
                        + Novo Ambiente
                    </button>
                )}
            </div>
            
            <input
                type="text"
                placeholder="Filtrar ambientes..."
                value={filtro}
                onChange={(e) => setFiltro(e.target.value)}
                className="filter-input"
            />
            
            <table className="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Local</th>
                        <th>Descrição</th>
                        <th>Responsável</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {filtered.map(amb => (
                        <tr key={amb.id}>
                            <td>{amb.id}</td>
                            <td>{amb.local}</td>
                            <td>{amb.descricao}</td>
                            <td>{amb.responsavel}</td>
                            <td>
                                <button onClick={() => navigate(`/ambientes/editar/${amb.id}`)}>✏️</button>
                                {user?.is_superuser && (
                                    <button onClick={() => handleDelete(amb.id)}>🗑️</button>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AmbienteList;