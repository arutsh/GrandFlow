import { jsx as _jsx } from "react/jsx-runtime";
import { createContext, useContext, useState, useEffect, } from "react";
export const STATUS = {
    PENDING: "pending",
    ACTIVE: "active",
};
const AuthContext = createContext(undefined);
export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem("token"));
    const [username, setUsername] = useState(localStorage.getItem("username"));
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isRegistering, setIsRegistering] = useState(false);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        // Check both storages
        const tokenFromStorage = localStorage.getItem("token") || sessionStorage.getItem("token");
        console.log("AuthProvider useEffect token", tokenFromStorage, "isAuthenticated, ", isAuthenticated);
        setToken(tokenFromStorage);
        const usernameFromStorage = localStorage.getItem("username") || sessionStorage.getItem("username");
        setUsername(usernameFromStorage);
        const status = sessionStorage.getItem("status");
        setIsRegistering(status === STATUS.PENDING);
        setIsAuthenticated(!!tokenFromStorage);
        console.log("token is true, is authenticated set as true");
        setLoading(false); // ✅ auth check finished
    }, []);
    const login = (token, username, remember, status, refreshToken) => {
        setToken(token);
        setUsername(username);
        if (remember) {
            localStorage.setItem("token", token);
            localStorage.setItem("username", username);
            localStorage.setItem("refreshToken", refreshToken);
        }
        else {
            sessionStorage.setItem("token", token);
            sessionStorage.setItem("username", username);
            sessionStorage.setItem("status", status);
            sessionStorage.setItem("refreshToken", refreshToken);
        }
        setIsAuthenticated(true);
        setIsRegistering(status === STATUS.PENDING);
    };
    const logout = () => {
        setToken(null);
        setUsername(null);
        localStorage.clear();
        sessionStorage.clear();
        setIsAuthenticated(false);
        setIsRegistering(false);
    };
    // 🔹 Don’t render children until we finish checking storage
    if (loading) {
        return _jsx("div", { children: "Loading..." });
    }
    return (_jsx(AuthContext.Provider, { value: {
            username,
            token,
            isAuthenticated: !!token,
            login,
            logout,
            isRegistering,
            loading,
            setIsRegistering,
        }, children: children }));
};
export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx)
        throw new Error("useAuth must be inside AuthProvider");
    return ctx;
};
