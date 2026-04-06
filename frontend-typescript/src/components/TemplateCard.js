import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function TemplateCard({ template }) {
    return (_jsxs("div", { className: "border rounded p-4 shadow-sm", children: [_jsx("h3", { className: "font-semibold", children: template.name }), _jsxs("p", { className: "text-sm text-gray-500", children: ["ID: ", template.id] })] }));
}
