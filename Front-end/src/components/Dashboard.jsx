import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Dashboard = () => {
    const [sensores, setSensores] = useState([]);
    const [ultimasMedicoes, setUltimasMedicoes] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [sRes, hRes] = await Promise.all([
                api.get('sensores/'),
                api.get('historicos/')
            ]);
            setSensores(sRes.data);
            // Pegar apenas as últimas 10 medições
            const ultimas = hRes.data.slice(-10).reverse();
            setUltimasMedicoes(ultimas);
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
        } finally {
            setLoading(false);
        }
    };

    const getIcon = (tipo) => {
        const icons = { 
            'temperatura': '🌡️', 
            'umidade': '💧', 
            'luminosidade': '☀️', 
            'contador': '🔢' 
        };
        return icons[tipo] || '📊';
    };

    const getSensorNome = (sensorId) => {
        const sensor = sensores.find(s => s.id === sensorId);
        return sensor ? sensor.sensor : 'Sensor ' + sensorId;
    };

    const getUnidade = (sensorId) => {
        const sensor = sensores.find(s => s.id === sensorId);
        return sensor ? sensor.unidade_medida : '';
    };

    if (loading) return <div className="loading">Carregando...</div>;

    return (
        <div className="dashboard">
            <h2>Dashboard de Sensores</h2>
            
            <div className="cards-grid">
                {sensores.map(sensor => (
                    <div 
                        key={sensor.id} 
                        className="sensor-card"
                        onClick={() => navigate(`/sensores/editar/${sensor.id}`)}
                        style={{ cursor: 'pointer' }}
                    >
                        <div className="icon">{getIcon(sensor.sensor)}</div>
                        <h3>{sensor.sensor}</h3>
                        <p>{sensor.unidade_medida}</p>
                        <span className={`status ${sensor.status === 'A' ? 'active' : 'inactive'}`}>
                            {sensor.status === 'A' ? 'Ativo' : 'Inativo'}
                        </span>
                    </div>
                ))}
            </div>
            
            <h3>Últimas Medições</h3>
            <table className="data-table">
                <thead>
                    <tr>
                        <th>Sensor</th>
                        <th>Valor</th>
                        <th>Data/Hora</th>
                    </tr>
                </thead>
                <tbody>
                    {ultimasMedicoes.map(h => (
                        <tr key={h.id}>
                            <td>{getSensorNome(h.sensor)}</td>
                            <td>{h.valor} {getUnidade(h.sensor)}</td>
                            <td>{new Date(h.time_stamp).toLocaleString('pt-BR')}</td>
                        </tr>
                    ))}
                    {ultimasMedicoes.length === 0 && (
                        <tr>
                            <td colSpan="3" style={{ textAlign: 'center' }}>Nenhuma medição encontrada</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default Dashboard;