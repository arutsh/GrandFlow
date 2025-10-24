import { HiViewGrid, HiViewList } from "react-icons/hi";

export function CardTableToggle({
  view,
  onViewChange,
}: {
  view: "cards" | "table";
  onViewChange: (view: "cards" | "table") => void;
}) {
  return (
    <div className="flex justify-end mb-4 space-x-2">
      <button
        onClick={() => onViewChange("cards")}
        className={`p-2 rounded ${
          view === "cards" ? "bg-slate-600 text-white" : "bg-gray-200"
        }`}
      >
        <HiViewGrid size={20} />
      </button>
      <button
        onClick={() => onViewChange("table")}
        className={`p-2 rounded ${
          view === "table" ? "bg-slate-600 text-white" : "bg-gray-200"
        }`}
      >
        <HiViewList size={20} />
      </button>
    </div>
  );
}
