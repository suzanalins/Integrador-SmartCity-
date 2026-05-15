import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './layout/Layout';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import SensorList from './components/SensorList';
import SensorForm from './components/SensorForm';
import AmbienteList from './components/AmbienteList';
import AmbienteForm from './components/AmbienteForm';
import MicrocontroladorList from './components/MicrocontroladorList';
import HistoricoList from './components/HistoricoList';
import LocalList from './components/LocalList';
import LocalForm from './components/LocalForm';
import ResponsavelList from './components/ResponsavelList';
import ResponsavelForm from './components/ResponsavelForm';
import './App.css';

function App() {
    const isAuthenticated = () => !!localStorage.getItem('access');

    const PrivateRoute = ({ children }) => {
        return isAuthenticated() ? children : <Navigate to="/login" />;
    };

    const AdminRoute = ({ children }) => {
        const userStr = localStorage.getItem('user');
        const user = userStr ? JSON.parse(userStr) : null;
        return isAuthenticated() && user?.is_superuser ? children : <Navigate to="/dashboard" />;
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/" element={<Navigate to="/dashboard" />} />
                
                <Route path="/dashboard" element={
                    <PrivateRoute>
                        <Layout>
                            <Dashboard />
                        </Layout>
                    </PrivateRoute>
                } />
                
                <Route path="/sensores" element={
                    <PrivateRoute>
                        <Layout>
                            <SensorList />
                        </Layout>
                    </PrivateRoute>
                } />
                
                <Route path="/sensores/novo" element={
                    <AdminRoute>
                        <Layout>
                            <SensorForm />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/sensores/editar/:id" element={
                    <AdminRoute>
                        <Layout>
                            <SensorForm />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/ambientes" element={
                    <PrivateRoute>
                        <Layout>
                            <AmbienteList />
                        </Layout>
                    </PrivateRoute>
                } />
                
                <Route path="/ambientes/novo" element={
                    <AdminRoute>
                        <Layout>
                            <AmbienteForm />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/ambientes/editar/:id" element={
                    <AdminRoute>
                        <Layout>
                            <AmbienteForm />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/microcontroladores" element={
                    <PrivateRoute>
                        <Layout>
                            <MicrocontroladorList />
                        </Layout>
                    </PrivateRoute>
                } />
                
                <Route path="/historicos" element={
                    <PrivateRoute>
                        <Layout>
                            <HistoricoList />
                        </Layout>
                    </PrivateRoute>
                } />
                
                <Route path="/locais" element={
                    <AdminRoute>
                        <Layout>
                            <LocalList />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/locais/novo" element={
                    <AdminRoute>
                        <Layout>
                            <LocalForm />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/locais/editar/:id" element={
                    <AdminRoute>
                        <Layout>
                            <LocalForm />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/responsaveis" element={
                    <AdminRoute>
                        <Layout>
                            <ResponsavelList />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/responsaveis/novo" element={
                    <AdminRoute>
                        <Layout>
                            <ResponsavelForm />
                        </Layout>
                    </AdminRoute>
                } />
                
                <Route path="/responsaveis/editar/:id" element={
                    <AdminRoute>
                        <Layout>
                            <ResponsavelForm />
                        </Layout>
                    </AdminRoute>
                } />
            </Routes>
        </Router>
    );
}

export default App;