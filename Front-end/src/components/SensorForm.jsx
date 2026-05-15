import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../services/api';

const SensorForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [micros, setMicros] = useState([]);
    const [loading, setLoading] = useState(false);
    const [form, setForm] = useState({
        sensor: 'temperatura',
        unidade_medida: '°C',
        microcontrolador: '',
        status: 'A'
    });

    useEffect(() => {
        loadMicros();
        if (id) loadSensor();
    }, [id]);

    const loadMicros = async () => {
        try {
            const res = await api.get('microcontroladores/');
            setMicros(res.data);
        } catch (error) {
            console.error('Erro ao carregar microcontroladores:', error);
        }
    };

    const loadSensor = async () => {
        try {
            const res = await api.get(`sensores/${id}/`);
            setForm({
                sensor: res.data.sensor,
                unidade_medida: res.data.unidade_medida,
                microcontrolador: res.data.microcontrolador,
                status: res.data.status
            });
        } catch (error) {
            console.error('Erro ao carregar sensor:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const dataToSend = {
                sensor: form.sensor,
                unidade_medida: form.unidade_medida,
                microcontrolador: parseInt(form.microcontrolador),
                status: form.status
            };
            
            if (id) {
                await api.put(`sensores/${id}/`, dataToSend);
            } else {
                await api.post('sensores/', dataToSend);
            }
            navigate('/sensores');
        } catch (error) {
            console.error('Erro ao salvar:', error);
            alert('Erro ao salvar sensor: ' + (error.response?.data?.detail || error.message));
        } finally {
            setLoading(false);
        }
    };

    const sensorTypes = [
        { value: 'temperatura', label: 'Temperatura', unidade: '°C' },
        { value: 'umidade', label: 'Umidade', unidade: '%' },
        { value: 'luminosidade', label: 'Luminosidade', unidade: 'lux' },
        { value: 'contador', label: 'Contador', unidade: 'uni' }
    ];

    const handleSensorChange = (e) => {
        const tipo = sensorTypes.find(t => t.value === e.target.value);
        setForm({ 
            ...form, 
            sensor: e.target.value, 
            unidade_medida: tipo.unidade 
        });
    };

    return (
        <div className="form-container">
            <h2>{id ? 'Editar' : 'Novo'} Sensor</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Tipo de Sensor</label>
                    <select value={form.sensor} onChange={handleSensorChange} required>
                        {sensorTypes.map(t => (
                            <option key={t.value} value={t.value}>{t.label}</option>
                        ))}
                    </select>
                </div>
                
                <div className="form-group">
                    <label>Unidade de Medida</label>
                    <input type="text" value={form.unidade_medida} disabled />
                </div>
                
                <div className="form-group">
                    <label>Microcontrolador</label>
                    <select 
                        value={form.microcontrolador} 
                        onChange={(e) => setForm({...form, microcontrolador: e.target.value})} 
                        required
                    >
                        <option value="">Selecione um microcontrolador</option>
                        {micros.map(m => (
                            <option key={m.id} value={m.id}>
                                {m.modelo} - {m.mac_adress}
                            </option>
                        ))}
                    </select>
                </div>
                
                <div className="form-group">
                    <label>Status</label>
                    <select value={form.status} onChange={(e) => setForm({...form, status: e.target.value})}>
                        <option value="A">Ativo</option>
                        <option value="I">Inativo</option>
                    </select>
                </div>
                
                <div className="form-actions">
                    <button type="button" onClick={() => navigate('/sensores')}>Cancelar</button>
                    <button type="submit" disabled={loading}>
                        {loading ? 'Salvando...' : 'Salvar'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default SensorForm;