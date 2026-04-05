import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { STATUS, useAuth } from "@/context/AuthContext";
import { loginUser } from "@/api/usersApi";
import { useNavigate } from "react-router-dom";
import Button from "@/components/ui/Button";
import { LogIn } from "lucide-react";
export default function Login() {
    const { isAuthenticated, isRegistering, login } = useAuth();
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [remember, setRemember] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const handleLogin = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const res = await loginUser(username, password);
            login(res.access_token, username, remember, res.status, res.refresh_token);
            if (res.status === STATUS.PENDING) {
                navigate("/onboarding");
            }
            else {
                navigate("/dashboard");
            }
        }
        catch (err) {
            setError("Invalid username or password");
        }
        finally {
            setIsLoading(false);
        }
    };
    return (_jsx("div", { className: "flex h-screen items-center justify-center bg-gradient-to-br from-primary/10 via-neutral to-secondary/10", children: _jsxs("form", { onSubmit: handleLogin, className: "bg-white p-8 rounded-2xl card-shadow-lg w-full max-w-md", children: [_jsx("div", { className: "flex items-center justify-center mb-8", children: _jsx("div", { className: "p-3 bg-slate-100 rounded-lg", children: _jsx(LogIn, { size: 32, className: "text-slate-700" }) }) }), _jsx("h1", { className: "text-3xl font-bold text-center text-slate-900 mb-2", children: "GrandFlow" }), _jsx("p", { className: "text-center text-gray-500 mb-8", children: "Welcome back" }), error && (_jsx("div", { className: "mb-4 p-3 bg-red-50 border border-red-200 rounded-lg", children: _jsx("p", { className: "text-red-600 text-sm", children: error }) })), _jsxs("div", { className: "mb-5", children: [_jsx("label", { className: "block text-sm font-medium text-slate-900 mb-2", children: "Username" }), _jsx("input", { type: "text", placeholder: "Enter your username", value: username, onChange: (e) => setUsername(e.target.value), className: "w-full px-4 py-2 border border-gray-300 rounded-lg input-focus bg-white", required: true })] }), _jsxs("div", { className: "mb-6", children: [_jsx("label", { className: "block text-sm font-medium text-slate-900 mb-2", children: "Password" }), _jsx("input", { type: "password", placeholder: "Enter your password", value: password, onChange: (e) => setPassword(e.target.value), className: "w-full px-4 py-2 border border-gray-300 rounded-lg input-focus bg-white", required: true })] }), _jsxs("div", { className: "flex items-center mb-6", children: [_jsx("input", { type: "checkbox", id: "remember", checked: remember, onChange: (e) => setRemember(e.target.checked), className: "w-4 h-4 rounded border-gray-300 text-slate-800 focus:ring-2 focus:ring-slate-300 cursor-pointer" }), _jsx("label", { htmlFor: "remember", className: "ml-2 text-sm text-gray-600 cursor-pointer", children: "Remember me" })] }), _jsx(Button, { type: "submit", variant: "primary", className: "w-full disabled:opacity-50 disabled:cursor-not-allowed font-medium", disabled: isLoading, children: isLoading ? "Logging in..." : "Login" }), _jsxs("p", { className: "text-center text-gray-600 mt-6", children: ["Don't have an account?", " ", _jsx("a", { href: "/register", className: "text-slate-700 font-semibold hover:text-slate-900 hover:underline", children: "Sign up" })] })] }) }));
}
