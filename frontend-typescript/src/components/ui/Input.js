import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { forwardRef } from "react";
const Input = forwardRef(({ label = "", name, type = "text", value, onChange, required = false, placeholder, showLabel = true, disabled = false, errorMsg = null, }, ref) => {
    return (_jsxs("div", { className: "mb-4", children: [showLabel && (_jsxs("label", { htmlFor: name, className: "block text-sm font-medium text-gray-700 mb-1", children: [label, " ", required && _jsx("span", { className: "text-red-500", children: "*" })] })), _jsx("input", { ref: ref, id: name, name: name, type: type, value: value, onChange: onChange, required: required, placeholder: placeholder, disabled: disabled, className: `w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm ${errorMsg ? "border-red-500" : "border-gray-300"}` }), errorMsg && (_jsx("div", { className: "text-red-500 text-xs px-1 py-1", children: errorMsg }))] }));
});
Input.displayName = "Input";
export default Input;
