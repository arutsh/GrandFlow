import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useEffect, useState, useMemo } from "react";
import Button from "@/components/ui/Button";
import { useMutation, useQuery, useQueryClient, } from "@tanstack/react-query";
import DashboardLayout from "../Dashboard/DashboardLayout";
import { fetchAllBudgets } from "@/api/gatewayApi";
import { HiPlus } from "react-icons/hi";
import { HiXMark, HiMagnifyingGlass } from "react-icons/hi2";
import { TableView } from "./components/TableView";
import { CardsView } from "./components/CardsView";
import { CardTableToggle } from "@/components/ui/CardTableToggle";
import { archiveBudget } from "@/api/budgetApi";
import { AddBudgetModal } from "./components/AddBudget";
import { EditBudgetModal } from "./components/EditBudget";
const BudgetsPage = () => {
    // Placeholder content for the Budgets page
    const [view, setView] = useState();
    const [isEditOpen, setIsEditOpen] = useState(false);
    const [isAddOpen, setIsAddOpen] = useState(false);
    const [editingBudget, setEditingBudget] = useState(null);
    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    // Filter states
    const [searchTerm, setSearchTerm] = useState("");
    const [filterStatuses, setFilterStatuses] = useState([]);
    const [showStatusDropdown, setShowStatusDropdown] = useState(false);
    const [filterCurrencies, setFilterCurrencies] = useState([]);
    const [showCurrencyDropdown, setShowCurrencyDropdown] = useState(false);
    const [filterDuration, setFilterDuration] = useState("");
    const [showDurationDropdown, setShowDurationDropdown] = useState(false);
    useEffect(() => {
        const handleResize = () => {
            const mobile = window.innerWidth < 768;
            setIsMobile(mobile);
            // Auto-switch: cards on mobile, table on desktop
            if (mobile && view === "table") {
                setView("cards");
            }
            else if (!mobile && view === undefined) {
                setView("table");
            }
        };
        window.addEventListener("resize", handleResize);
        // Set initial view
        if (view === undefined) {
            setView(isMobile ? "cards" : "table");
        }
        return () => window.removeEventListener("resize", handleResize);
    }, [isMobile, view]);
    const queryClient = useQueryClient();
    const openEditModal = (budget) => {
        setEditingBudget(budget);
        setIsEditOpen(true);
    };
    const closeAddModal = (newBudget) => {
        if (newBudget) {
            queryClient.setQueryData(["budgets"], (oldData) => {
                if (!oldData)
                    return [];
                return [...oldData, newBudget];
            });
        }
        setIsAddOpen(false);
    };
    const closeEditModal = (updatedBudget) => {
        if (updatedBudget) {
            queryClient.setQueryData(["budgets"], (oldData) => {
                if (!oldData)
                    return [];
                return oldData.map((b) => {
                    if (b.id === updatedBudget.id) {
                        b.name = updatedBudget.name;
                        b.funder = {};
                        b.funder.name = updatedBudget?.external_funder_name;
                        b.funder.id = updatedBudget?.funding_customer_id;
                    }
                    return b;
                });
            });
        }
        setEditingBudget(null);
        setIsEditOpen(false);
    };
    const deleteBudgetMutation = useMutation({
        mutationFn: async (budgetId) => archiveBudget(budgetId),
        onSuccess: (_, budgetId) => {
            // Invalidate and refetch budgets after deletion
            queryClient.setQueryData(["budgets"], (oldData) => {
                if (!oldData)
                    return [];
                return oldData.filter((b) => b.id !== budgetId);
            });
        },
    });
    const { isPending, isError, data, error } = useQuery({
        queryKey: ["budgets"],
        queryFn: fetchAllBudgets,
    });
    // Filter logic
    const filteredData = useMemo(() => {
        if (!data)
            return [];
        return data.filter((budget) => {
            const matchesSearch = (budget.name?.toLowerCase() ?? "").includes(searchTerm.toLowerCase()) ||
                (budget.funder?.name?.toLowerCase() ?? "").includes(searchTerm.toLowerCase());
            const matchesStatus = filterStatuses.length === 0 || filterStatuses.includes(budget.status);
            const matchesCurrency = filterCurrencies.length === 0 ||
                (budget.local_currency &&
                    filterCurrencies.includes(budget.local_currency));
            let matchesDuration = true;
            if (filterDuration) {
                const duration = budget.duration_months || 0;
                if (filterDuration === "short")
                    matchesDuration = duration <= 6;
                if (filterDuration === "medium")
                    matchesDuration = duration > 6 && duration <= 12;
                if (filterDuration === "long")
                    matchesDuration = duration > 12;
            }
            return (matchesSearch && matchesStatus && matchesCurrency && matchesDuration);
        });
    }, [data, searchTerm, filterStatuses, filterCurrencies, filterDuration]);
    // Get unique values for filters
    const uniqueStatuses = useMemo(() => {
        if (!data)
            return [];
        const statuses = new Set();
        data.forEach((b) => {
            if (b.status)
                statuses.add(b.status);
        });
        return Array.from(statuses);
    }, [data]);
    const uniqueCurrencies = useMemo(() => {
        if (!data)
            return [];
        const currencies = new Set();
        data.forEach((b) => {
            if (b.local_currency)
                currencies.add(b.local_currency);
        });
        return Array.from(currencies);
    }, [data]);
    const clearFilters = () => {
        setSearchTerm("");
        setFilterStatuses([]);
        setFilterCurrencies([]);
        setFilterDuration("");
    };
    if (isPending) {
        return _jsx("div", { children: "Loading..." });
    }
    if (isError) {
        return _jsxs("div", { children: ["Error: ", error.message] });
    }
    return (_jsxs(DashboardLayout, { children: [isEditOpen && editingBudget && (_jsx(EditBudgetModal, { isOpen: isEditOpen, onClose: (val) => closeEditModal(val), data: editingBudget })), isAddOpen && (_jsx(AddBudgetModal, { isOpen: isAddOpen, onClose: (val) => closeAddModal(val) })), _jsxs("div", { className: "flex flex-col min-h-screen bg-gray-50", children: [_jsxs("div", { className: "mb-8", children: [_jsx("h1", { className: "text-4xl font-bold text-slate-900 mb-2", children: "Budgets" }), _jsx("p", { className: "text-gray-600", children: "Manage and track all your budgets in one place." })] }), _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-8", children: [_jsx("div", { className: "flex gap-3 w-full md:w-auto", children: _jsxs(Button, { onClick: () => setIsAddOpen(!isAddOpen), variant: "primary", className: "flex items-center gap-2", children: [_jsx(HiPlus, { size: 18 }), " Add Budget"] }) }), !isMobile && view && (_jsx(CardTableToggle, { view: view, onViewChange: (newView) => setView(newView) }))] }), _jsxs("div", { className: "mb-6 p-4 bg-white rounded-lg border border-slate-200 shadow-sm", children: [(filterStatuses.length > 0 ||
                                filterCurrencies.length > 0 ||
                                filterDuration) && (_jsxs("div", { className: "mb-4 flex flex-wrap gap-2", children: [filterStatuses.map((status) => (_jsxs("div", { className: `flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold capitalize ${status === "draft"
                                            ? "bg-yellow-100 text-yellow-800"
                                            : status === "approved"
                                                ? "bg-green-100 text-green-800"
                                                : status === "rejected"
                                                    ? "bg-red-100 text-red-800"
                                                    : "bg-slate-100 text-slate-800"}`, children: [status, _jsx("button", { onClick: () => setFilterStatuses(filterStatuses.filter((s) => s !== status)), className: "hover:opacity-70 transition-opacity", children: _jsx(HiXMark, { size: 16 }) })] }, `status-${status}`))), filterCurrencies.map((currency) => (_jsxs("div", { className: "flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold bg-blue-100 text-blue-800", children: [currency, _jsx("button", { onClick: () => setFilterCurrencies(filterCurrencies.filter((c) => c !== currency)), className: "hover:opacity-70 transition-opacity", children: _jsx(HiXMark, { size: 16 }) })] }, `currency-${currency}`))), filterDuration && (_jsxs("div", { className: "flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold bg-purple-100 text-purple-800", children: [filterDuration === "short"
                                                ? "≤ 6 mo"
                                                : filterDuration === "medium"
                                                    ? "7-12 mo"
                                                    : "> 12 mo", _jsx("button", { onClick: () => setFilterDuration(""), className: "hover:opacity-70 transition-opacity", children: _jsx(HiXMark, { size: 16 }) })] }))] })), _jsxs("div", { className: "flex flex-col lg:flex-row items-start lg:items-center gap-3", children: [_jsxs("div", { className: "relative flex-shrink-0 w-full lg:w-64", children: [_jsx(HiMagnifyingGlass, { className: "absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" }), _jsx("input", { type: "text", placeholder: "Search...", value: searchTerm, onChange: (e) => setSearchTerm(e.target.value), className: "pl-9 pr-3 py-2 w-full border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-400" })] }), _jsxs("div", { className: "relative flex-shrink-0 w-full lg:w-auto", children: [_jsxs("button", { onClick: () => setShowStatusDropdown(!showStatusDropdown), className: "w-full lg:w-auto px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white hover:bg-slate-50 flex items-center justify-between gap-2 focus:outline-none focus:ring-2 focus:ring-slate-400", children: [_jsx("span", { className: "text-slate-700", children: filterStatuses.length === 0
                                                            ? "Status"
                                                            : `${filterStatuses.length} selected` }), _jsx("svg", { className: `w-4 h-4 text-slate-400 transition-transform ${showStatusDropdown ? "rotate-180" : ""}`, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24", children: _jsx("path", { strokeLinecap: "round", strokeLinejoin: "round", strokeWidth: 2, d: "M19 14l-7 7m0 0l-7-7m7 7V3" }) })] }), showStatusDropdown && (_jsx("div", { className: "absolute top-full left-0 mt-1 w-56 bg-white border border-slate-300 rounded-lg shadow-lg z-10", children: _jsx("div", { className: "p-2", children: uniqueStatuses.map((status) => (_jsxs("label", { className: "flex items-center gap-2 px-3 py-2 rounded hover:bg-slate-50 cursor-pointer", children: [_jsx("input", { type: "checkbox", checked: filterStatuses.includes(status), onChange: (e) => {
                                                                    if (e.target.checked) {
                                                                        setFilterStatuses([...filterStatuses, status]);
                                                                    }
                                                                    else {
                                                                        setFilterStatuses(filterStatuses.filter((s) => s !== status));
                                                                    }
                                                                }, className: "w-4 h-4 rounded border-slate-300 text-slate-700 focus:ring-slate-400" }), _jsx("span", { className: "text-sm text-slate-700 capitalize", children: status })] }, status))) }) }))] }), _jsxs("div", { className: "relative flex-shrink-0 w-full lg:w-auto", children: [_jsxs("button", { onClick: () => setShowCurrencyDropdown(!showCurrencyDropdown), className: "w-full lg:w-auto px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white hover:bg-slate-50 flex items-center justify-between gap-2 focus:outline-none focus:ring-2 focus:ring-slate-400", children: [_jsx("span", { className: "text-slate-700", children: filterCurrencies.length === 0
                                                            ? "Currency"
                                                            : `${filterCurrencies.length} selected` }), _jsx("svg", { className: `w-4 h-4 text-slate-400 transition-transform ${showCurrencyDropdown ? "rotate-180" : ""}`, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24", children: _jsx("path", { strokeLinecap: "round", strokeLinejoin: "round", strokeWidth: 2, d: "M19 14l-7 7m0 0l-7-7m7 7V3" }) })] }), showCurrencyDropdown && (_jsx("div", { className: "absolute top-full left-0 mt-1 w-56 bg-white border border-slate-300 rounded-lg shadow-lg z-10", children: _jsx("div", { className: "p-2", children: uniqueCurrencies.map((currency) => (_jsxs("label", { className: "flex items-center gap-2 px-3 py-2 rounded hover:bg-slate-50 cursor-pointer", children: [_jsx("input", { type: "checkbox", checked: filterCurrencies.includes(currency), onChange: (e) => {
                                                                    if (e.target.checked) {
                                                                        setFilterCurrencies([
                                                                            ...filterCurrencies,
                                                                            currency,
                                                                        ]);
                                                                    }
                                                                    else {
                                                                        setFilterCurrencies(filterCurrencies.filter((c) => c !== currency));
                                                                    }
                                                                }, className: "w-4 h-4 rounded border-slate-300 text-slate-700 focus:ring-slate-400" }), _jsx("span", { className: "text-sm text-slate-700", children: currency })] }, currency))) }) }))] }), _jsxs("div", { className: "relative flex-shrink-0 w-full lg:w-auto", children: [_jsxs("button", { onClick: () => setShowDurationDropdown(!showDurationDropdown), className: "w-full lg:w-auto px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white hover:bg-slate-50 flex items-center justify-between gap-2 focus:outline-none focus:ring-2 focus:ring-slate-400", children: [_jsx("span", { className: "text-slate-700", children: filterDuration === ""
                                                            ? "Duration"
                                                            : filterDuration === "short"
                                                                ? "≤ 6 mo"
                                                                : filterDuration === "medium"
                                                                    ? "7-12 mo"
                                                                    : "> 12 mo" }), _jsx("svg", { className: `w-4 h-4 text-slate-400 transition-transform ${showDurationDropdown ? "rotate-180" : ""}`, fill: "none", stroke: "currentColor", viewBox: "0 0 24 24", children: _jsx("path", { strokeLinecap: "round", strokeLinejoin: "round", strokeWidth: 2, d: "M19 14l-7 7m0 0l-7-7m7 7V3" }) })] }), showDurationDropdown && (_jsx("div", { className: "absolute top-full left-0 mt-1 w-56 bg-white border border-slate-300 rounded-lg shadow-lg z-10", children: _jsx("div", { className: "p-2", children: [
                                                        { value: "short", label: "Short (≤ 6 mo)" },
                                                        { value: "medium", label: "Medium (7-12 mo)" },
                                                        { value: "long", label: "Long (> 12 mo)" },
                                                    ].map((option) => (_jsxs("label", { className: "flex items-center gap-2 px-3 py-2 rounded hover:bg-slate-50 cursor-pointer", children: [_jsx("input", { type: "radio", name: "duration", value: option.value, checked: filterDuration === option.value, onChange: (e) => {
                                                                    setFilterDuration(e.target.value);
                                                                    setShowDurationDropdown(false);
                                                                }, className: "w-4 h-4 border-slate-300 text-slate-700 focus:ring-slate-400" }), _jsx("span", { className: "text-sm text-slate-700", children: option.label })] }, option.value))) }) }))] }), (searchTerm ||
                                        filterStatuses.length > 0 ||
                                        filterCurrencies.length > 0 ||
                                        filterDuration) && (_jsxs(Button, { onClick: clearFilters, variant: "outline", className: "w-full lg:w-auto flex items-center justify-center gap-1 py-2 px-3", children: [_jsx(HiXMark, { size: 14 }), " Clear All"] }))] }), _jsxs("div", { className: "text-xs text-slate-600 mt-3", children: [filteredData.length, " of ", data?.length || 0, " budgets"] })] }), filteredData && filteredData.length > 0 ? (_jsx(_Fragment, { children: view === "cards" ? (_jsx(CardsView, { data: filteredData, onEdit: openEditModal, onDelete: deleteBudgetMutation.mutate })) : view === "table" ? (_jsx(TableView, { data: filteredData, onEdit: openEditModal, onDelete: deleteBudgetMutation.mutate })) : null })) : (_jsx("div", { className: "flex items-center justify-center py-16 bg-white rounded-lg border border-slate-200", children: _jsxs("div", { className: "text-center", children: [_jsx("div", { className: "mb-4", children: _jsx(HiPlus, { size: 48, className: "text-gray-300 mx-auto" }) }), data && data.length === 0 ? (_jsxs(_Fragment, { children: [_jsx("p", { className: "text-xl font-semibold text-slate-900 mb-2", children: "No budgets yet" }), _jsx("p", { className: "text-gray-600 mb-6", children: "Create your first budget to start managing your finances" }), _jsx(Button, { onClick: () => setIsAddOpen(true), variant: "primary", children: "Create Your First Budget" })] })) : (_jsxs(_Fragment, { children: [_jsx("p", { className: "text-xl font-semibold text-slate-900 mb-2", children: "No budgets match your filters" }), _jsx("p", { className: "text-gray-600 mb-6", children: "Try adjusting your search or filter criteria" }), _jsx(Button, { onClick: clearFilters, variant: "secondary", children: "Clear Filters" })] }))] }) }))] })] }));
};
export default BudgetsPage;
