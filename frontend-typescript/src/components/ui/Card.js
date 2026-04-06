import { jsx as _jsx } from "react/jsx-runtime";
export function Card({ children, className, }) {
    return (_jsx("div", { className: className ?? "w-full bg-slate-500 text-white p-6 mx-10", children: children }));
}
export function CardHeader({ children, className, }) {
    return _jsx("div", { className: className ?? "", children: children });
}
export function CardContent({ children, className, }) {
    return _jsx("div", { className: className ?? "", children: children });
}
