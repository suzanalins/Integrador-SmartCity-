import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../services/api';

const LocalForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [form, setForm] = useState({ local: '' });

    useEffect(() => {
        if (id) loadLocal();
    }, [id]);

    const loadLocal = async () => {
        const res = await api.get(`locais/${id}/`);
        setForm(res.data);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (id) {
            await api.put(`locais/${id}/`, form);
        } else {
            await api.post('locais/', form);
        }
        navigate('/locais');
    };

    return (
        <div className="form-container">
            <h2>{id ? 'Editar' : 'Novo'} Local</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Nome do local"
                    value={form.local}
                    onChange={(e) => setForm({...form, local: e.target.value})}
                    required
                />
                <div className="form-actions">
                    <button type="button" onClick={() => navigate('/locais')}>Cancelar</button>
                    <button type="submit">Salvar</button>
                </div>
            </form>
        </div>
    );
};

export default LocalForm;