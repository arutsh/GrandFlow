import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import { useDetailedBudget } from "../SingleBudgetViewContext";
export function BudgetViewSummary() {
    const { budget, budgetCategoryNames, totalAmount } = useDetailedBudget();
    const categories = [...new Set(budget?.lines?.map((l) => l?.category?.name))];
    return (_jsxs(Card, { className: "w-full bg-gray-50  py-5 border-b border-gray-200", children: [_jsx(CardHeader, { children: _jsx("h2", { className: "text-lg font-semibold", children: "Budget Summary" }) }), _jsxs(CardContent, { children: [_jsxs("div", { children: ["Total Lines: ", budget?.lines?.length] }), _jsxs("div", { children: ["Total Amount: ", totalAmount.toLocaleString()] }), _jsxs("div", { children: ["Categories: ", categories.join(", ")] })] })] }));
}
