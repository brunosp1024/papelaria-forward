import { useState } from "react";

import { useAuth } from "../../contexts/AuthContext";
import "./Login.css";

export function Login() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await login({ username: username.trim(), password });
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Nao foi possivel fazer login.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="login-root">
      <section className="login-card" aria-label="Formulario de login">
        <h1 className="login-title">Papelaria Forward</h1>
        <p className="login-subtitle">Entre com usuario e senha para acessar o dashboard.</p>

        <form className="login-form" onSubmit={handleSubmit}>
          <label className="login-label" htmlFor="username">
            Usuario
          </label>
          <input
            id="username"
            className="login-input"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
            required
          />

          <label className="login-label" htmlFor="password">
            Senha
          </label>
          <input
            id="password"
            className="login-input"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
            required
          />

          {errorMessage ? <p className="login-error">{errorMessage}</p> : null}

          <button className="login-submit" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Entrando..." : "Entrar"}
          </button>
        </form>
      </section>
    </main>
  );
}