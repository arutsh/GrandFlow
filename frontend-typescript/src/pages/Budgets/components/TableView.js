import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Button from "@/components/ui/Button";
import { TableCommon } from "@/components/ui/Table";
import { utcToLocal } from "@/utils/datetime";
import { createColumnHelper } from "@tanstack/react-table";
import { Edit2, Trash2 } from "lucide-react";
const columnHelper = createColumnHelper();
export function TableView({ data, onEdit, onDelete, }) {
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
    const columns = [
        columnHelper.accessor("status", {
            header: "Status",
            cell: (info) => (_jsx("span", { className: `px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(info.getValue())}`, children: info.getValue() })),
        }),
        columnHelper.accessor("name", { header: "Name" }),
        columnHelper.accessor("funder", {
            header: "Funder",
            cell: (info) => info.getValue()?.name || "N/A",
        }),
        columnHelper.accessor("amount", {
            header: "Amount",
            cell: (info) => `$${info.getValue()?.toFixed(2) || ""}`,
        }),
        columnHelper.accessor("duration_months", {
            header: "Duration (months)",
            cell: (info) => info.getValue()?.toString() || "N/A",
        }),
        columnHelper.accessor("local_currency", {
            header: "Currency",
            cell: (info) => info.getValue() || "N/A",
        }),
        columnHelper.accessor("trace", {
            header: "Updated At",
            cell: (info) => utcToLocal(info.getValue()?.updated.event_date),
        }),
        columnHelper.accessor("trace", {
            header: "Updated By",
            cell: (info) => `${info.getValue()?.updated.user?.first_name || ""} ${info.getValue()?.updated.user?.last_name || ""}`,
        }),
        columnHelper.display({
            id: "actions",
            cell: (info) => (_jsxs("div", { className: "flex space-x-1 gap-1", onClick: (e) => e.stopPropagation(), children: [_jsx(Button, { onClick: () => onEdit(info.row.original), variant: "icon", title: "Edit budget", children: _jsx(Edit2, { size: 18 }) }), _jsx(Button, { variant: "icon-danger", onClick: () => onDelete(info.row.original.id), title: "Delete budget", children: _jsx(Trash2, { size: 18 }) })] })),
        }),
    ];
    const redirectToBudget = (budgetId) => {
        // Placeholder for redirect logic
        window.location.href = `/budgets/${budgetId}`;
    };
    return (_jsx(TableCommon, { data: data, columns: columns, onRowClick: (row) => redirectToBudget(row.id) }));
}
