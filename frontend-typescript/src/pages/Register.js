import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Button from "@/components/ui/Button";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { registerUser } from "@/api/usersApi";
import { useAuth } from "@/context/AuthContext";
import { UserPlus } from "lucide-react";
export default function Register() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState(null);
    const { login } = useAuth();
    const mutation = useMutation({
        mutationFn: ({ email, password }) => registerUser(email, password),
        onSuccess: (data) => {
            login(data.access_token, email, false, data.status, data.refresh_token || "");
            navigate("/onboarding");
        },
        onError: (error) => {
            setError("Registration failed. Please try again.");
            console.error("Registration failed", error);
        },
    });
    const handleSubmit = (e) => {
        e.preventDefault();
        setError(null);
        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }
        if (password.length < 6) {
            setError("Password must be at least 6 characters");
            return;
        }
        mutation.mutate({ email, password });
    };
    return (_jsx("div", { className: "flex items-center justify-center h-screen bg-gradient-to-br from-primary/10 via-neutral to-secondary/10", children: _jsxs("form", { onSubmit: handleSubmit, className: "bg-white p-8 rounded-2xl card-shadow-lg w-full max-w-md", children: [_jsx("div", { className: "flex items-center justify-center mb-8", children: _jsx("div", { className: "p-3 bg-green-50 rounded-lg", children: _jsx(UserPlus, { size: 32, className: "text-green-600" }) }) }), _jsx("h1", { className: "text-3xl font-bold text-center text-slate-900 mb-2", children: "Create Account" }), _jsx("p", { className: "text-center text-gray-500 mb-8", children: "Join GrandFlow today" }), error && (_jsx("div", { className: "mb-4 p-3 bg-red-50 border border-red-200 rounded-lg", children: _jsx("p", { className: "text-red-600 text-sm", children: error }) })), _jsxs("div", { className: "mb-5", children: [_jsx("label", { className: "block text-sm font-medium text-slate-900 mb-2", children: "Email Address" }), _jsx("input", { type: "email", placeholder: "Enter your email", value: email, onChange: (e) => setEmail(e.target.value), className: "w-full px-4 py-2 border border-gray-300 rounded-lg input-focus bg-white", required: true })] }), _jsxs("div", { className: "mb-5", children: [_jsx("label", { className: "block text-sm font-medium text-slate-900 mb-2", children: "Password" }), _jsx("input", { type: "password", placeholder: "Create a password", value: password, onChange: (e) => setPassword(e.target.value), className: "w-full px-4 py-2 border border-gray-300 rounded-lg input-focus bg-white", required: true }), _jsx("p", { className: "text-xs text-gray-500 mt-1", children: "At least 6 characters" })] }), _jsxs("div", { className: "mb-6", children: [_jsx("label", { className: "block text-sm font-medium text-slate-900 mb-2", children: "Confirm Password" }), _jsx("input", { type: "password", placeholder: "Confirm your password", value: confirmPassword, onChange: (e) => setConfirmPassword(e.target.value), className: "w-full px-4 py-2 border border-gray-300 rounded-lg input-focus bg-white", required: true })] }), _jsx(Button, { type: "submit", variant: "primary", className: "w-full disabled:opacity-50 disabled:cursor-not-allowed font-medium", disabled: mutation.isPending, children: mutation.isPending ? "Creating account..." : "Create Account" }), _jsxs("p", { className: "text-center text-gray-600 mt-6", children: ["Already have an account?", " ", _jsx("a", { href: "/login", className: "text-slate-700 font-semibold hover:text-slate-900 hover:underline", children: "Login" })] })] }) }));
}
