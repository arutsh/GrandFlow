import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Button from "./Button";
const Modal = ({ isOpen, onClose, title, children }) => {
    if (!isOpen)
        return null;
    return (_jsx("div", { className: "fixed inset-0 bg-gray-900/80 flex items-center justify-center z-50", children: _jsxs("div", { className: "bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative", children: [title && _jsx("h2", { className: "text-lg font-bold mb-4", children: title }), _jsx("div", { className: "absolute top-2 right-2", children: _jsx(Button, { variant: "close", onClick: onClose, children: "\u2715" }) }), children] }) }));
};
export default Modal;
