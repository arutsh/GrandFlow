import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from "react";
import { useParams } from "react-router-dom";
import DashboardLayout from "../Dashboard/DashboardLayout";
import { BudgetViewHeader } from "./components/BudgetViewHeader";
import { BudgetViewLinesTable } from "./components/BudgetViewLinesTable";
import { BudgetViewTraces } from "./components/BudgetViewTraces";
import { BudgetViewSummary } from "./components/BudgetViewSummary";
import { SingleBudgetViewContextProvider, useDetailedBudget, } from "./SingleBudgetViewContext";
import { AddBudgetLineModal } from "./components/AddBudgetLine";
export function SingleBudgetViewContainer() {
    const { id } = useParams();
    return (_jsx(DashboardLayout, { children: _jsx(SingleBudgetViewContextProvider, { id: id, children: _jsx(SingleBudgetView, { id: id }) }) }));
}
function SingleBudgetView({ id }) {
    const [isAddOpen, setIsAddOpen] = useState(false);
    const [isEditOpen, setIsEditOpen] = useState(undefined);
    // const
    const { budget } = useDetailedBudget();
    return (_jsxs(_Fragment, { children: [isAddOpen && (_jsx(AddBudgetLineModal, { isOpen: isAddOpen, onClose: () => {
                    setIsAddOpen(!isAddOpen);
                }, budgetLine: undefined, onSave: () => { } })), isEditOpen && (_jsx(AddBudgetLineModal, { budgetLine: isEditOpen, isOpen: !!isEditOpen, onClose: () => {
                    setIsEditOpen(undefined);
                }, onSave: () => { } })), budget && (_jsxs("div", { className: "flex flex-col items-center px-10 min-h-screen bg-gray-50", children: [_jsx(BudgetViewHeader, { budget: budget }), _jsx(BudgetViewSummary, {}), _jsx(BudgetViewLinesTable, { lines: budget.lines, onEdit: (value) => {
                            console.log("eesit button cliekd = ", value);
                            setIsEditOpen(value);
                        }, 
                        // onDelete={() => {}}
                        onNew: () => setIsAddOpen(!isAddOpen), onClose: () => {
                            (setIsAddOpen(false), setIsEditOpen(undefined));
                        } }), _jsx(BudgetViewTraces, { budget: budget })] }))] }));
}
export default SingleBudgetView;
