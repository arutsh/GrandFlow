import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { editBudget } from "@/api/budgetApi";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useMutation } from "@tanstack/react-query";
import { useEffect, useState } from "react";
export function EditBudgetModal({ isOpen, onClose, data, }) {
    const [budgetName, setBudgetName] = useState(data?.name || "");
    const [funderName, setFunderName] = useState(data?.funder?.name || "");
    const [errorMessage, setErrorMessage] = useState("");
    useEffect(() => {
        if (data) {
            setBudgetName(data.name || "");
            setFunderName(data.funder?.name || "");
        }
    }, [data]);
    const mutation = useMutation({
        mutationFn: ({ budgetName, funderName, }) => editBudget(data.id, {
            name: budgetName,
            external_funder_name: funderName,
        }),
        onSuccess: (updatedBudget) => {
            setErrorMessage("");
            onClose(updatedBudget);
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
    console.log("EditBudgetModal - data:", data);
    return (_jsxs(Modal, { isOpen: isOpen, onClose: () => onClose(null), title: "New Budget", children: [errorMessage && _jsx("p", { className: "text-red-500", children: errorMessage }), data && (_jsxs("form", { onSubmit: handleSubmit, className: "flex flex-col space-y-4", children: [_jsx("input", { type: "text", value: budgetName, onChange: (e) => setBudgetName(e.target.value), placeholder: "Budget Name", className: "border p-2 rounded w-full" }), _jsx("input", { type: "text", value: funderName, onChange: (e) => setFunderName(e.target.value), placeholder: "Funder name", className: "border p-2 rounded w-full" }), _jsxs("div", { className: "flex justify-end space-x-2", children: [_jsx(Button, { type: "submit", children: "Save" }), _jsx(Button, { variant: "secondary", onClick: () => onClose(null), children: "Cancel" })] })] }))] }));
}
