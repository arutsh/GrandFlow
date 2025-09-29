import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { loginUser } from "@/api/usersApi";
import { useNavigate } from "react-router-dom";
import Button from "@/components/ui/Button";

export default function Login() {
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [remember, setRemember] = useState(false);

  // 🔹 Redirect to dashboard if already logged in
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await loginUser(username, password);
      login(res.access_token, username, remember);
      navigate("/dashboard", { replace: true });
    } catch (err: any) {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-slate-300">
      <form
        onSubmit={handleLogin}
        className="bg-white p-6 rounded-xl shadow-lg w-96"
      >
        <h1 className="text-xl font-bold mb-4">Login</h1>
        {error && <p className="text-red-500">{error}</p>}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <label>
          <input
            type="checkbox"
            checked={remember}
            onChange={(e) => setRemember(e.target.checked)}
          />
          Remember me
        </label>
        <Button type="submit" variant="primary">
          Login
        </Button>
        <p className="text-center text-navy mt-4">
          Don't have an account?{" "}
          <a href="/register" className="text-blue hover:underline">
            Register
          </a>
        </p>
      </form>
    </div>
  );
}
