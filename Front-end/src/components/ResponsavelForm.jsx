import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../services/api';

const ResponsavelForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [form, setForm] = useState({ responsavel: '' });

    useEffect(() => {
        if (id) loadResponsavel();
    }, [id]);

    const loadResponsavel = async () => {
        const res = await api.get(`responsaveis/${id}/`);
        setForm(res.data);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (id) {
            await api.put(`responsaveis/${id}/`, form);
        } else {
            await api.post('responsaveis/', form);
        }
        navigate('/responsaveis');
    };

    return (
        <div className="form-container">
            <h2>{id ? 'Editar' : 'Novo'} Responsável</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Nome do responsável"
                    value={form.responsavel}
                    onChange={(e) => setForm({...form, responsavel: e.target.value})}
                    required
                />
                <div className="form-actions">
                    <button type="button" onClick={() => navigate('/responsaveis')}>Cancelar</button>
                    <button type="submit">Salvar</button>
                </div>
            </form>
        </div>
    );
};

export default ResponsavelForm;