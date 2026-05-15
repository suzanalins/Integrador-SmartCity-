import React from 'react';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();
    const userStr = localStorage.getItem('user');
    const user = userStr ? JSON.parse(userStr) : null;

    const handleLogout = () => {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        localStorage.removeItem('user');
        navigate('/login');
    };

    return (
        <nav className="navbar">
            <h1 onClick={() => navigate('/dashboard')}>SmartCity</h1>
            <div className="nav-links">
                <button onClick={() => navigate('/sensores')}>Sensores</button>
                <button onClick={() => navigate('/ambientes')}>Ambientes</button>
                <button onClick={() => navigate('/microcontroladores')}>Microcontroladores</button>
                <button onClick={() => navigate('/historicos')}>Histórico</button>
                {user?.is_superuser && (
                    <>
                        <button onClick={() => navigate('/locais')}>Locais</button>
                        <button onClick={() => navigate('/responsaveis')}>Responsáveis</button>
                    </>
                )}
                <span>Olá, {user?.nome || user?.username}</span>
                <button onClick={handleLogout} className="logout">Sair</button>
            </div>
        </nav>
    );
};

export default Navbar;