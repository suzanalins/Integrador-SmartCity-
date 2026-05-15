import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

const Register = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        nome: '',
        telefone: '',
        tipo_usuario: 'user'
    });
    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        // Limpar erro do campo ao digitar
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    const validateForm = () => {
        const newErrors = {};
        
        if (!formData.username.trim()) {
            newErrors.username = 'Usuário é obrigatório';
        } else if (formData.username.length < 3) {
            newErrors.username = 'Usuário deve ter pelo menos 3 caracteres';
        }
        
        if (!formData.email.trim()) {
            newErrors.email = 'Email é obrigatório';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Email inválido';
        }
        
        if (!formData.password) {
            newErrors.password = 'Senha é obrigatória';
        } else if (formData.password.length < 6) {
            newErrors.password = 'Senha deve ter pelo menos 6 caracteres';
        }
        
        if (!formData.nome.trim()) {
            newErrors.nome = 'Nome é obrigatório';
        }
        
        if (!formData.telefone.trim()) {
            newErrors.telefone = 'Telefone é obrigatório';
        }
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        setLoading(true);
        
        try {
            const response = await api.post('register/', formData);
            
            if (response.status === 201 || response.status === 200) {
                // Após cadastro, faz login automaticamente
                const loginResponse = await api.post('token/', {
                    username: formData.username,
                    password: formData.password
                });
                
                localStorage.setItem('access', loginResponse.data.access);
                localStorage.setItem('refresh', loginResponse.data.refresh);
                
                // Buscar dados do usuário
                const userResponse = await api.get('me/');
                localStorage.setItem('user', JSON.stringify(userResponse.data));
                
                // Redirecionar para dashboard
                navigate('/dashboard');
            }
        } catch (error) {
            console.error('Erro no cadastro:', error);
            
            if (error.response?.data) {
                const apiErrors = error.response.data;
                
                if (typeof apiErrors === 'object') {
                    const newErrors = {};
                    
                    if (apiErrors.username) {
                        newErrors.username = apiErrors.username[0] || 'Usuário já existe';
                    }
                    if (apiErrors.email) {
                        newErrors.email = apiErrors.email[0] || 'Email já existe';
                    }
                    if (apiErrors.detail) {
                        // Erro geral
                        setErrors({ general: apiErrors.detail });
                    } else {
                        setErrors(newErrors);
                    }
                } else if (typeof apiErrors === 'string') {
                    setErrors({ general: apiErrors });
                }
            } else {
                setErrors({ general: 'Erro ao conectar com o servidor' });
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <div className="register-card">
                <h2>Criar Nova Conta</h2>
                <p className="subtitle">Preencha os dados abaixo para se cadastrar</p>
                
                {errors.general && (
                    <div className="error-message">{errors.general}</div>
                )}
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Usuário *</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            placeholder="Digite seu nome de usuário"
                            className={errors.username ? 'error' : ''}
                        />
                        {errors.username && <span className="error-text">{errors.username}</span>}
                    </div>
                    
                    <div className="form-group">
                        <label>Email *</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="Digite seu email"
                            className={errors.email ? 'error' : ''}
                        />
                        {errors.email && <span className="error-text">{errors.email}</span>}
                    </div>
                    
                    <div className="form-group">
                        <label>Nome Completo *</label>
                        <input
                            type="text"
                            name="nome"
                            value={formData.nome}
                            onChange={handleChange}
                            placeholder="Digite seu nome completo"
                            className={errors.nome ? 'error' : ''}
                        />
                        {errors.nome && <span className="error-text">{errors.nome}</span>}
                    </div>
                    
                    <div className="form-group">
                        <label>Telefone *</label>
                        <input
                            type="tel"
                            name="telefone"
                            value={formData.telefone}
                            onChange={handleChange}
                            placeholder="(00) 00000-0000"
                            className={errors.telefone ? 'error' : ''}
                        />
                        {errors.telefone && <span className="error-text">{errors.telefone}</span>}
                    </div>
                    
                    <div className="form-group">
                        <label>Tipo de Usuário</label>
                        <select
                            name="tipo_usuario"
                            value={formData.tipo_usuario}
                            onChange={handleChange}
                        >
                            <option value="user">Usuário Comum</option>
                            <option value="admin">Administrador</option>
                        </select>
                        <small className="help-text">
                            Administradores têm acesso a todas as funções do sistema
                        </small>
                    </div>
                    
                    <div className="form-group">
                        <label>Senha *</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Mínimo 6 caracteres"
                            className={errors.password ? 'error' : ''}
                        />
                        {errors.password && <span className="error-text">{errors.password}</span>}
                    </div>
                    
                    <button 
                        type="submit" 
                        className="btn-primary"
                        disabled={loading}
                    >
                        {loading ? 'Cadastrando...' : 'Cadastrar'}
                    </button>
                    
                    <div className="login-link">
                        Já tem uma conta? <Link to="/login">Faça login</Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Register;