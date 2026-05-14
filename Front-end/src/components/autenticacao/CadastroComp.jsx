import { useState } from "react";
import api from "../../services/api";

export default function Register() {

    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        nome: "",
        telefone: "",
        tipo_usuario: "user"
    });

    function handleChange(e) {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    }

    async function handleRegister(e) {

        e.preventDefault();

        try {

            const response = await api.post("/register/", formData);

            console.log(response.data);

            alert("Usuário cadastrado!");

        } catch (error) {

            console.log(error.response?.data);

            alert("Erro ao cadastrar");
        }
    }

    return (
        <div>

            <h1>Cadastro</h1>

            <form onSubmit={handleRegister}>

                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    onChange={handleChange}
                />

                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    onChange={handleChange}
                />

                <input
                    type="password"
                    name="password"
                    placeholder="Senha"
                    onChange={handleChange}
                />

                <input
                    type="text"
                    name="nome"
                    placeholder="Nome"
                    onChange={handleChange}
                />

                <input
                    type="text"
                    name="telefone"
                    placeholder="Telefone"
                    onChange={handleChange}
                />

                <select
                    name="tipo_usuario"
                    onChange={handleChange}
                >
                    <option value="user">Usuário</option>
                    <option value="admin">Admin</option>
                </select>

                <button type="submit">
                    Cadastrar
                </button>

            </form>

        </div>
    );
}