import React, { useState, useEffect } from 'react';
import api from '../services/api';

const MicrocontroladorList = () => {
    const [micros, setMicros] = useState([]);

    useEffect(() => {
        loadMicros();
    }, []);

    const loadMicros = async () => {
        const res = await api.get('microcontroladores/');
        setMicros(res.data);
    };

    return (
        <div>
            <h2>Microcontroladores</h2>
            <table className="data-table">
                <thead>
                    <tr><th>ID</th><th>Modelo</th><th>MAC Address</th><th>Latitude</th><th>Longitude</th><th>Status</th></tr>
                </thead>
                <tbody>
                    {micros.map(m => (
                        <tr key={m.id}>
                            <td>{m.id}</td>
                            <td>{m.modelo}</td>
                            <td>{m.mac_adress}</td>
                            <td>{m.latitude}</td>
                            <td>{m.longitude}</td>
                            <td>
                                <span className={`status-badge ${m.status === 'A' ? 'active' : 'inactive'}`}>
                                    {m.status === 'A' ? 'Ativo' : 'Inativo'}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default MicrocontroladorList;