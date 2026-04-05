import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Routes, Route, Navigate, BrowserRouter } from "react-router-dom";
import { useAuth, AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import Register from "./pages/Register";
import Onboarding from "./pages/OnBoarding";
import BudgetsPage from "./pages/Budgets/budgets";
import { SingleBudgetViewContainer, } from "./pages/Budgets/SingleBudgetView";
function PrivateRoute({ children }) {
    const { isAuthenticated, loading } = useAuth();
    if (loading)
        return _jsx("div", { children: "Loading..." });
    if (!isAuthenticated)
        return _jsx(Navigate, { to: "/login", replace: true });
    return children;
}
export default function App() {
    return (_jsx(AuthProvider, { children: _jsx(BrowserRouter, { children: _jsxs(Routes, { children: [_jsx(Route, { path: "/login", element: _jsx(Login, {}) }), _jsx(Route, { path: "/register", element: _jsx(Register, {}) }), _jsx(Route, { path: "/onboarding", element: _jsx(PrivateRoute, { children: _jsx(Onboarding, {}) }) }), _jsx(Route, { path: "/dashboard", element: _jsx(PrivateRoute, { children: _jsx(Dashboard, {}) }) }), _jsx(Route, { path: "/budgets", element: _jsx(PrivateRoute, { children: _jsx(BudgetsPage, {}) }) }), _jsx(Route, { path: "/budgets/:id", element: _jsx(PrivateRoute, { children: _jsx(SingleBudgetViewContainer, {}) }) }), _jsx(Route, { path: "*", element: _jsx(Navigate, { to: "/dashboard", replace: true }) })] }) }) }));
}
