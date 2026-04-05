import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Menu, X, Home, FileText, BarChart3 } from "lucide-react"; // icons
import Button from "../../components/ui/Button";
export default function DashboardLayout({ children, }) {
    const [isOpen, setIsOpen] = useState(true);
    return (_jsxs("div", { className: "flex w-full h-screen bg-gray-50", children: [_jsxs("aside", { className: `
          fixed md:static top-0 left-0 h-full z-20
          bg-slate-900 text-white transition-all duration-300
          ${isOpen ? "w-64" : "w-16"}
        `, children: [_jsxs("div", { className: "flex items-center justify-between p-4", children: [_jsx("span", { className: `font-bold text-lg ${!isOpen && "hidden md:block"}`, children: "GF" }), _jsx(Button, { variant: "icon", onClick: () => setIsOpen(!isOpen), className: "text-white md:hidden", children: isOpen ? _jsx(X, { size: 24 }) : _jsx(Menu, { size: 24 }) })] }), _jsx("nav", { className: "flex-1", children: _jsxs("ul", { className: "space-y-2", children: [_jsx("li", { children: _jsxs("a", { href: "/dashboard", className: "flex items-center gap-3 px-4 py-2 hover:bg-blue-600/60 rounded transition-colors", children: [_jsx(Home, { size: 20 }), isOpen && _jsx("span", { children: "Home" })] }) }), _jsx("li", { children: _jsxs("a", { href: "/budgets", className: "flex items-center gap-3 px-4 py-2 hover:bg-blue-600/60 rounded transition-colors", children: [_jsx(FileText, { size: 20 }), isOpen && _jsx("span", { children: "Budgets" })] }) }), _jsx("li", { children: _jsxs("a", { href: "/reports", className: "flex items-center gap-3 px-4 py-2 hover:bg-blue-600/60 rounded transition-colors", children: [_jsx(BarChart3, { size: 20 }), isOpen && _jsx("span", { children: "Reports" })] }) })] }) })] }), isOpen && (_jsx("div", { className: "fixed inset-0 bg-black/50 z-10 md:hidden", onClick: () => setIsOpen(false) })), _jsx("main", { className: "flex-1 p-8 overflow-auto bg-gray-50", children: children })] }));
}
