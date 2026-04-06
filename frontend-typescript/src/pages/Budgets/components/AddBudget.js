import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { createBudget } from "@/api/budgetApi";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
export function AddBudgetModal({ isOpen, onClose, }) {
    const [budgetName, setBudgetName] = useState("");
    const [funderName, setFunderName] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const mutation = useMutation({
        mutationFn: ({ budgetName, funderName, }) => createBudget({
            name: budgetName,
            external_funder_name: funderName,
        }),
        onSuccess: (newBudget) => {
            setErrorMessage("");
            onClose(newBudget);
        },
        onError: () => {
            setErrorMessage("Failed to update budget");
        },
    });
    const handleSubmit = (e) => {
        e.preventDefault();
        mutation.mutate({
            budgetName,
            funderName,
        });
    };
    return (_jsxs(Modal, { isOpen: isOpen, onClose: () => onClose(null), title: "Edit Budget", children: [errorMessage && _jsx("p", { className: "text-red-500", children: errorMessage }), _jsxs("form", { onSubmit: handleSubmit, className: "flex flex-col space-y-4", children: [_jsx("input", { type: "text", value: budgetName, onChange: (e) => setBudgetName(e.target.value), placeholder: "Budget Name", className: "border p-2 rounded w-full" }), _jsx("input", { type: "text", value: funderName, onChange: (e) => setFunderName(e.target.value), placeholder: "Funder name", className: "border p-2 rounded w-full" }), _jsxs("div", { className: "flex justify-end space-x-2", children: [_jsx(Button, { type: "submit", children: "Save" }), _jsx(Button, { variant: "secondary", onClick: () => onClose(null), children: "Cancel" })] })] })] }));
}
