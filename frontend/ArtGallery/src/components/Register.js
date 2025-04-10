import { useState } from "react";
import { registerUser } from "../api/authService";
import { useHistory } from "react-router-dom";
import "./auth.css";

export const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const history = useHistory();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await registerUser(name, email, password);  // Sending name, email, and password
      setSuccess("Registration successful! Redirecting to login...");
      setTimeout(() => history.push("/login"), 1500);
    } catch (err) {
      setError("Registration failed. Please try again.");
    }
  };

  return (
    <div className="zoom-card-wide">
      <i className="fas fa-times exit-icon" onClick={() => history.push("/")} />
      <h2 className="auth-title">Sign Up</h2>
      <form onSubmit={handleRegister} className="auth-form">
        <input
          className="auth-input"
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          className="auth-input"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="auth-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="auth-button">Register</button>
        <button onClick={() => history.push("/login")} className="link-button">Already have an account? Login</button>
        {success && <p className="success">{success}</p>}
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
};
