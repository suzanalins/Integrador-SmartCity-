import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const SensorList = () => {
    const [sensores, setSensores] = useState([]);
    const [filtro, setFiltro] = useState('');
    const [filtroStatus, setFiltroStatus] = useState('');
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    useEffect(() => {
        loadSensores();
    }, []);

    const loadSensores = async () => {
        try {
            const response = await api.get('sensores/');
            setSensores(response.data);
        } catch (error) {
            console.error('Erro ao carregar sensores:', error);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Tem certeza que deseja excluir este sensor?')) {
            try {
                await api.delete(`sensores/${id}/`);
                loadSensores();
            } catch (error) {
                console.error('Erro ao deletar:', error);
                alert('Erro ao deletar sensor');
            }
        }
    };

    const filtered = sensores.filter(s => {
        const matchTipo = s.sensor.toLowerCase().includes(filtro.toLowerCase());
        const matchStatus = !filtroStatus || s.status === filtroStatus;
        return matchTipo && matchStatus;
    });

    const getIcon = (tipo) => {
        const icons = { 
            'temperatura': '🌡️', 
            'umidade': '💧', 
            'luminosidade': '☀️', 
            'contador': '🔢' 
        };
        return icons[tipo] || '📊';
    };

    return (
        <div>
            <div className="page-header">
                <h2>Sensores</h2>
                {user?.is_superuser && (
                    <button className="btn-primary" onClick={() => navigate('/sensores/novo')}>
                        + Novo Sensor
                    </button>
                )}
            </div>
            
            <div className="filters-section">
                <input
                    type="text"
                    placeholder="Filtrar por tipo de sensor..."
                    value={filtro}
                    onChange={(e) => setFiltro(e.target.value)}
                    className="filter-input"
                />
                <select 
                    value={filtroStatus} 
                    onChange={(e) => setFiltroStatus(e.target.value)}
                    className="filter-select"
                >
                    <option value="">Todos os status</option>
                    <option value="A">Ativo</option>
                    <option value="I">Inativo</option>
                </select>
            </div>
            
            <table className="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Tipo</th>
                        <th>Unidade</th>
                        <th>Status</th>
                        <th>Microcontrolador</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {filtered.map(sensor => (
                        <tr key={sensor.id}>
                            <td>{sensor.id}</td>
                            <td>{getIcon(sensor.sensor)} {sensor.sensor}</td>
                            <td>{sensor.unidade_medida}</td>
                            <td>
                                <span className={`status-badge ${sensor.status === 'A' ? 'active' : 'inactive'}`}>
                                    {sensor.status === 'A' ? 'Ativo' : 'Inativo'}
                                </span>
                            </td>
                            <td>{sensor.microcontrolador}</td>
                            <td className="actions">
                                <button onClick={() => navigate(`/sensores/editar/${sensor.id}`)} title="Editar">✏️</button>
                                {user?.is_superuser && (
                                    <button onClick={() => handleDelete(sensor.id)} title="Excluir">🗑️</button>
                                )}
                            </td>
                        </tr>
                    ))}
                    {filtered.length === 0 && (
                        <tr>
                            <td colSpan="6" style={{ textAlign: 'center' }}>Nenhum sensor encontrado</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default SensorList;