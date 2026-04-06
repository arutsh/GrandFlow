import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function Select({ label = "", name, value, options, onChange, required = false, showLabel = true, disabled = false, placeholder = "-- Select --", allowCreate = false, createLabel = "➕ Create new...", }) {
    const combinedOptions = allowCreate
        ? [...options, { label: createLabel, value: "__new" }]
        : options;
    return (_jsxs("div", { className: "mb-4", children: [showLabel && (_jsxs("label", { htmlFor: name, className: "block text-sm font-medium text-gray-700 mb-1", children: [label, " ", required && _jsx("span", { className: "text-red-500", children: "*" })] })), _jsxs("select", { id: name, name: name, value: value, onChange: (e) => onChange?.(e.target.value), required: required, disabled: disabled, className: "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm", children: [_jsx("option", { value: "", children: placeholder }), combinedOptions.map((opt) => (_jsx("option", { value: opt.value, children: opt.label }, opt.value)))] })] }));
}
