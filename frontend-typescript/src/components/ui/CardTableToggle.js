import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { HiViewGrid, HiViewList } from "react-icons/hi";
import Button from "./Button";
export function CardTableToggle({ view, onViewChange, }) {
    return (_jsxs("div", { className: "flex justify-end mb-4 space-x-2", children: [_jsx(Button, { variant: "toggle", active: view === "cards", onClick: () => onViewChange("cards"), children: _jsx(HiViewGrid, { size: 20 }) }), _jsx(Button, { variant: "toggle", active: view === "table", onClick: () => onViewChange("table"), children: _jsx(HiViewList, { size: 20 }) })] }));
}
