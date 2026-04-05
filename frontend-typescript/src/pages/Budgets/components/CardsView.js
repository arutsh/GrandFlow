import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Button from "@/components/ui/Button";
import { utcToLocal } from "@/utils/datetime";
import { Edit2, Trash2, DollarSign, Calendar, User } from "lucide-react";
export function CardsView({ data, onEdit, onDelete, }) {
    const getTotalAmount = (lines) => {
        if (!lines)
            return 0;
        return lines.reduce((sum, line) => sum + (line.amount || 0), 0);
    };
    const getStatusColor = (status) => {
        switch (status?.toLowerCase()) {
            case "approved":
                return "bg-green-100 text-green-800";
            case "draft":
                return "bg-yellow-100 text-yellow-800";
            case "rejected":
                return "bg-red-100 text-red-800";
            default:
                return "bg-slate-100 text-slate-800";
        }
    };
    return (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full", children: data.map((budget) => (_jsxs("div", { className: "bg-white rounded-lg border border-slate-200 shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden group", children: [_jsxs("div", { className: "px-4 py-3 border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white", children: [_jsxs("div", { className: "flex items-start justify-between gap-3 mb-2", children: [_jsx("h2", { className: "text-lg font-bold text-slate-900 flex-1", children: budget.name }), _jsx("span", { className: `px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(budget.status)}`, children: budget.status })] }), _jsx("p", { className: "text-sm text-slate-600", children: budget.funder?.name || "No funder" })] }), _jsxs("div", { className: "px-4 py-3 space-y-3", children: [_jsxs("div", { className: "flex items-center gap-3 p-3 bg-slate-50 rounded-lg", children: [_jsx("div", { className: "p-2 bg-slate-100 rounded", children: _jsx(DollarSign, { size: 18, className: "text-slate-600" }) }), _jsxs("div", { children: [_jsx("p", { className: "text-xs text-slate-500 font-medium", children: "Total Amount" }), _jsxs("p", { className: "text-lg font-bold text-slate-900", children: [budget.local_currency, " ", getTotalAmount(budget.lines)?.toLocaleString() || "0"] })] })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2", children: [_jsxs("div", { className: "p-2 bg-slate-50 rounded text-center", children: [_jsx("div", { className: "flex items-center justify-center gap-1 mb-1", children: _jsx(Calendar, { size: 14, className: "text-slate-600" }) }), _jsx("p", { className: "text-xs text-slate-500", children: "Duration" }), _jsxs("p", { className: "font-semibold text-slate-900", children: [budget.duration_months || 0, " mo"] })] }), _jsxs("div", { className: "p-2 bg-slate-50 rounded text-center", children: [_jsx("p", { className: "text-xs text-slate-500 mb-1", children: "Currency" }), _jsx("p", { className: "font-semibold text-slate-900", children: budget.local_currency })] })] }), _jsxs("div", { className: "pt-2 border-t border-slate-100 space-y-1 text-xs text-slate-500", children: [_jsxs("div", { className: "flex items-center gap-1", children: [_jsx(User, { size: 12 }), _jsxs("span", { children: ["Updated by ", budget?.trace?.updated?.user?.first_name, " ", budget?.trace?.updated?.user?.last_name] })] }), _jsx("div", { children: utcToLocal(budget?.trace?.updated?.event_date) })] })] }), _jsxs("div", { className: "px-4 py-3 bg-slate-50 border-t border-slate-100 flex gap-2 justify-end", children: [_jsxs(Button, { variant: "secondary", onClick: () => onEdit(budget), className: "flex items-center justify-center gap-1 py-1 px-3 text-sm", children: [_jsx(Edit2, { size: 14 }), " Edit"] }), _jsxs(Button, { variant: "danger", onClick: () => onDelete(budget.id), className: "flex items-center justify-center gap-1 py-1 px-3 text-sm", children: [_jsx(Trash2, { size: 14 }), " Delete"] })] })] }, budget.id))) }));
}
