import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../services/api';

const AmbienteForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [locais, setLocais] = useState([]);
    const [responsaveis, setResponsaveis] = useState([]);
    const [form, setForm] = useState({ 
        local: '', 
        descricao: '', 
        responsavel: '' 
    });

    useEffect(() => {
        loadData();
        if (id) loadAmbiente();
    }, [id]);

    const loadData = async () => {
        try {
            const [lRes, rRes] = await Promise.all([
                api.get('locais/'),
                api.get('responsaveis/')
            ]);
            setLocais(lRes.data);
            setResponsaveis(rRes.data);
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
        }
    };

    const loadAmbiente = async () => {
        try {
            const res = await api.get(`ambientes/${id}/`);
            setForm({
                local: res.data.local,
                descricao: res.data.descricao,
                responsavel: res.data.responsavel
            });
        } catch (error) {
            console.error('Erro ao carregar ambiente:', error);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (id) {
                await api.put(`ambientes/${id}/`, form);
            } else {
                await api.post('ambientes/', form);
            }
            navigate('/ambientes');
        } catch (error) {
            console.error('Erro ao salvar:', error);
            alert('Erro ao salvar ambiente. Verifique os dados.');
        }
    };

    return (
        <div className="form-container">
            <h2>{id ? 'Editar' : 'Novo'} Ambiente</h2>
            <form onSubmit={handleSubmit}>
                <select 
                    value={form.local} 
                    onChange={(e) => setForm({...form, local: parseInt(e.target.value)})} 
                    required
                >
                    <option value="">Selecione o local</option>
                    {locais.map(l => (
                        <option key={l.id} value={l.id}>{l.local}</option>
                    ))}
                </select>
                
                <textarea 
                    placeholder="Descrição do ambiente" 
                    value={form.descricao} 
                    onChange={(e) => setForm({...form, descricao: e.target.value})} 
                    required 
                />
                
                <select 
                    value={form.responsavel} 
                    onChange={(e) => setForm({...form, responsavel: parseInt(e.target.value)})} 
                    required
                >
                    <option value="">Selecione o responsável</option>
                    {responsaveis.map(r => (
                        <option key={r.id} value={r.id}>{r.responsavel}</option>
                    ))}
                </select>
                
                <div className="form-actions">
                    <button type="button" onClick={() => navigate('/ambientes')}>Cancelar</button>
                    <button type="submit">Salvar</button>
                </div>
            </form>
        </div>
    );
};

export default AmbienteForm;