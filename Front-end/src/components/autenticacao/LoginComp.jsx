import { useState } from "react";
import api from "../../services/api";

export default function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function handleLogin(e) {

        e.preventDefault();

        try {

            const response = await api.post("/token/", {
                username,
                password
            });

            localStorage.setItem("access", response.data.access);
            localStorage.setItem("refresh", response.data.refresh);

            alert("Login realizado!");

            console.log(response.data);

        } catch (error) {

            console.log(error.response?.data);

            alert("Usuário ou senha inválidos");
        }
    }

    return (
        <div>

            <h1>Login</h1>

            <form onSubmit={handleLogin}>

                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />

                <input
                    type="password"
                    placeholder="Senha"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                <button type="submit">
                    Entrar
                </button>

            </form>

        </div>
    );
}