import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
export function BudgetViewHeader({ budget }) {
    return (_jsxs(Card, { className: "w-full bg-gray-50  py-5 border-b border-gray-200", children: [_jsx(CardHeader, { className: " ", children: _jsx("h1", { className: "text-2xl font-semibold", children: budget.name }) }), _jsxs(CardContent, { children: [_jsxs("p", { className: "text-sm text-gray-300 mt-1", children: ["Owner: ", budget.owner.name, " (", budget.owner.type, ")"] }), _jsxs("p", { className: "text-sm text-gray-300", children: ["Funder: ", budget.funder.name] })] })] }));
}
