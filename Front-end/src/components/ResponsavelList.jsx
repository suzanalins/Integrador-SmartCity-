import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const ResponsavelList = () => {
    const [responsaveis, setResponsaveis] = useState([]);
    const [filtro, setFiltro] = useState('');
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    useEffect(() => {
        loadResponsaveis();
    }, []);

    const loadResponsaveis = async () => {
        const res = await api.get('responsaveis/');
        setResponsaveis(res.data);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Tem certeza que deseja excluir este responsável?')) {
            await api.delete(`responsaveis/${id}/`);
            loadResponsaveis();
        }
    };

    const filtered = responsaveis.filter(r => 
        r.responsavel.toLowerCase().includes(filtro.toLowerCase())
    );

    return (
        <div>
            <div className="page-header">
                <h2>Responsáveis</h2>
                {user?.is_superuser && (
                    <button className="btn-primary" onClick={() => navigate('/responsaveis/novo')}>
                        + Novo Responsável
                    </button>
                )}
            </div>
            
            <input
                type="text"
                placeholder="Filtrar responsáveis..."
                value={filtro}
                onChange={(e) => setFiltro(e.target.value)}
                className="filter-input"
            />
            
            <table className="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Responsável</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {filtered.map(responsavel => (
                        <tr key={responsavel.id}>
                            <td>{responsavel.id}</td>
                            <td>{responsavel.responsavel}</td>
                            <td>
                                <button onClick={() => navigate(`/responsaveis/editar/${responsavel.id}`)}>✏️</button>
                                {user?.is_superuser && (
                                    <button onClick={() => handleDelete(responsavel.id)}>🗑️</button>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ResponsavelList;