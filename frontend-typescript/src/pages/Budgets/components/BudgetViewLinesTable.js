import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { TableCommon } from "@/components/ui/Table";
import { createColumnHelper } from "@tanstack/react-table";
import { useMemo } from "react";
import Button, { ConfirmDeleteButton } from "@/components/ui/Button";
import { deleteBudgetLine } from "@/api/gatewayApi";
import { useMutation } from "@tanstack/react-query";
import { useDetailedBudget } from "../SingleBudgetViewContext";
const columnHelper = createColumnHelper();
export function BudgetViewLinesTable({ lines, onEdit, 
// onDelete,
onNew, onClose, }) {
    const { budget, setBudget, budgetCategories, existingExtraKeys, budgetCategoryNames, } = useDetailedBudget();
    const extraFieldKeys = useMemo(() => {
        const keys = new Set();
        if (!lines)
            return [];
        lines.forEach((line) => {
            if (line.extra_fields) {
                Object.keys(line.extra_fields).forEach((key) => keys.add(key));
            }
        });
        return Array.from(keys);
    }, [lines]);
    const mutation = useMutation({
        mutationFn: (budget_line_id) => {
            // Call the API to delete the budget line
            return deleteBudgetLine(budget_line_id);
        },
        onSuccess: (_, budget_line_id) => {
            // On success, you might want to refetch the budget lines or update the state
            if (!budget)
                return;
            console.log(`Budget line with id ${budget_line_id} deleted successfully.`);
            const updatedBudget = {
                ...budget,
                lines: budget.lines?.filter((line) => line.id !== budget_line_id),
            };
            setBudget(updatedBudget);
        },
        onError: (error) => {
            console.error("Error deleting budget line:", error);
        },
    });
    const onDelete = (budget_line_id) => {
        console.log("Delete clicked for line id:", budget_line_id);
        mutation.mutate(budget_line_id);
    };
    const columns = useMemo(() => [
        {
            header: "Category",
            accessorFn: (row) => row.category?.name ?? "—",
            id: "category",
            enableSorting: true,
            enableGrouping: true,
        },
        {
            header: "Description",
            accessorKey: "description",
            enableSorting: true,
        },
        {
            header: "Amount (£)",
            accessorKey: "amount",
            cell: (info) => (_jsx("span", { className: "font-semibold", children: info.getValue().toLocaleString() })),
            aggregationFn: "sum",
            aggregatedCell: (info) => {
                const value = info.getValue();
                return (_jsxs("span", { className: "font-semibold", children: ["Subtotal: ", value.toLocaleString()] }));
            },
        },
        // Dynamically add columns for extra_fields
        ...extraFieldKeys.map((key) => ({
            header: key,
            accessorFn: (row) => row.extra_fields?.[key] ?? "—",
            id: key, // important for unique identification
        })),
        columnHelper.display({
            id: "actions",
            enableSorting: false,
            cell: (info) => (_jsxs("div", { className: "flex space-x-2", children: [_jsx(Button, { onClick: () => onEdit(info.row.original), children: "Edit" }), _jsx(ConfirmDeleteButton, { onConfirm: () => onDelete(info.row.original.id) })] })),
        }),
    ], [extraFieldKeys]);
    return (_jsxs(_Fragment, { children: [_jsx("h2", { className: "w-full text-lg py-5 font-semibold text-slate-700 mb-4", children: "Budget Lines" }), _jsx("div", { className: "flex justify-end mb-4 w-full", children: _jsx(Button, { onClick: onNew, children: "New Budget Line" }) }), _jsx(TableCommon, { data: lines || [], columns: columns })] }));
}
