import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useReactTable, getCoreRowModel, getSortedRowModel, flexRender, getGroupedRowModel, getExpandedRowModel, } from "@tanstack/react-table";
import { useState } from "react";
import Button from "./Button";
export function Table({ children }) {
    return (_jsx("table", { className: "min-w-full divide-y divide-gray-200 bg-white shadow rounded", children: children }));
}
export function TableHead({ children }) {
    return _jsx("thead", { className: "bg-gray-50 font-medium", children: children });
}
export function TableRow({ key, children }) {
    return _jsx("tr", { children: children }, key);
}
export function TableHeaderCell({ key, children, onClick, }) {
    return (_jsx("td", { className: "px-4 py-2 text-left text-sm font-medium  text-gray-700", onClick: onClick, children: children }, key));
}
export function TableCell({ children }) {
    return (_jsx("td", { className: "px-4 py-2 text-left text-sm font-normal  text-gray-700", children: children }));
}
export function TableBody({ children }) {
    return _jsx("tbody", { className: "divide-y divide-gray-200", children: children });
}
export function TableCommon({ data, columns, onRowClick, }) {
    const [sorting, setSorting] = useState([]);
    const [expanded, setExpanded] = useState({});
    const table = useReactTable({
        data,
        columns,
        // state: { sorting, grouping: ["category"], expanded },
        initialState: { grouping: ["category"] }, // let table manage expanded/sorting
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getGroupedRowModel: getGroupedRowModel(),
        getExpandedRowModel: getExpandedRowModel(),
    });
    return (_jsxs(Table, { children: [_jsx(TableHead, { children: table.getHeaderGroups().map((headerGroup) => (_jsx(TableRow, { children: headerGroup.headers.map((header) => {
                        const sorted = header.column.getIsSorted();
                        const canSort = header.column.getCanSort();
                        return (_jsxs(TableHeaderCell, { onClick: header.column.getToggleSortingHandler(), children: [header.isPlaceholder
                                    ? null
                                    : flexRender(header.column.columnDef.header, header.getContext()), canSort && (_jsx(_Fragment, { children: sorted ? (sorted === "asc" ? (_jsx("span", { children: "\u2191" })) : (_jsx("span", { children: "\u2193" }))) : (_jsx("span", { className: "opacity-50 text-xs", children: "\u2195" })) }))] }, header.id));
                    }) }, headerGroup.id))) }), _jsx("tbody", { className: "divide-y divide-gray-200", children: table.getRowModel().rows.map((row) => (_jsx("tr", { onClick: () => onRowClick?.(row.original), className: "hover:bg-slate-50 cursor-pointer", children: row.getVisibleCells().map((cell) => {
                        // IMPORTANT: use cell-level helpers (v8)
                        const isGrouped = cell.getIsGrouped();
                        const isAggregated = cell.getIsAggregated();
                        const isPlaceholder = cell.getIsPlaceholder();
                        // Render grouped row: usually only one column (the grouped column) should show
                        if (isGrouped) {
                            // show expander + the grouped value + count of subRows
                            return (_jsxs("td", { className: "px-4 py-2 text-left text-sm font-normal text-gray-700", children: [_jsx(Button, { variant: "expander", onClick: row.getToggleExpandedHandler(), className: "mr-2", children: row.getIsExpanded() ? "▼" : "▶" }), _jsx("strong", { className: "mr-2", children: flexRender(cell.column.columnDef.cell, cell.getContext()) }), _jsxs("span", { className: "text-gray-400", children: ["(", row.subRows.length, ")"] })] }, cell.id));
                        }
                        // Aggregated (subtotal) cell
                        if (isAggregated) {
                            return (_jsx("td", { className: "px-4 py-2 text-left text-sm font-normal text-gray-700", children: flexRender(cell.column.columnDef.aggregatedCell ??
                                    cell.column.columnDef.cell, cell.getContext()) }, cell.id));
                        }
                        // Placeholder cell for grouped layout (keep cell empty)
                        if (isPlaceholder) {
                            return _jsx("td", { className: "px-4 py-2" }, cell.id);
                        }
                        // Normal cell
                        return (_jsx("td", { className: "px-4 py-2 text-left text-sm font-normal text-gray-700", children: flexRender(cell.column.columnDef.cell, cell.getContext()) }, cell.id));
                    }) }, row.id))) })] }));
}
