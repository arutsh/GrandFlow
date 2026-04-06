import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "./DashboardLayout";
import { useEffect } from "react";
import { FileText, TrendingUp, BarChart3, DollarSign } from "lucide-react";
import Button from "@/components/ui/Button";
export default function Dashboard() {
    const { username, logout, isRegistering } = useAuth();
    const navigate = useNavigate();
    useEffect(() => {
        console.log("Dashboard - isRegistering:", isRegistering);
        if (isRegistering) {
            navigate("/onboarding");
        }
    }, [isRegistering]);
    const handleLogout = () => {
        logout();
        navigate("/login", { replace: true });
    };
    // Mock stats data - replace with real data from API
    const stats = [
        {
            title: "Total Budgets",
            value: "12",
            icon: FileText,
            color: "text-slate-700",
            bgColor: "bg-slate-100",
        },
        {
            title: "On Track",
            value: "9",
            icon: TrendingUp,
            color: "text-green-600",
            bgColor: "bg-green-50",
        },
        {
            title: "Over Budget",
            value: "2",
            icon: BarChart3,
            color: "text-red-600",
            bgColor: "bg-red-50",
        },
        {
            title: "Total Allocated",
            value: "$125K",
            icon: DollarSign,
            color: "text-slate-700",
            bgColor: "bg-slate-100",
        },
    ];
    return (_jsx(DashboardLayout, { children: _jsxs("div", { className: "flex flex-col min-h-screen bg-gray-50", children: [_jsxs("div", { className: "mb-12", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsxs("h1", { className: "text-4xl font-bold text-slate-900", children: ["Welcome back,", " ", _jsx("span", { className: "text-slate-800 font-bold", children: username }), " \uD83D\uDC4B"] }), _jsx(Button, { onClick: handleLogout, variant: "secondary", className: "py-2 px-4", children: "Logout" })] }), _jsx("p", { className: "text-gray-600", children: "Here's what's happening with your budgets today." })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12", children: stats.map((stat, idx) => {
                        const Icon = stat.icon;
                        return (_jsx("div", { className: `${stat.bgColor} rounded-lg card-shadow-hover p-6 transition-all`, children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("p", { className: "text-gray-600 text-sm font-medium mb-1", children: stat.title }), _jsx("p", { className: "text-3xl font-bold text-slate-900", children: stat.value })] }), _jsx("div", { className: `p-2 rounded-lg ${stat.bgColor}`, children: _jsx(Icon, { size: 24, className: stat.color }) })] }) }, idx));
                    }) }), _jsxs("div", { className: "mb-12", children: [_jsx("h2", { className: "text-2xl font-bold text-slate-900 mb-6", children: "Quick Actions" }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsx(Button, { onClick: () => navigate("/budgets"), className: "py-3 px-6 text-base font-medium", variant: "primary", children: "View All Budgets" }), _jsx(Button, { onClick: () => navigate("/budgets"), className: "py-3 px-6 text-base font-medium", variant: "outline", children: "Create New Budget" })] })] }), _jsxs("div", { className: "bg-white rounded-lg card-shadow p-6", children: [_jsx("h2", { className: "text-xl font-bold text-slate-900 mb-4", children: "Recent Activity" }), _jsxs("div", { className: "text-center py-8", children: [_jsx("p", { className: "text-gray-500", children: "No recent activity yet." }), _jsx("p", { className: "text-gray-400 text-sm mt-2", children: "Start by creating your first budget!" })] })] })] }) }));
}
