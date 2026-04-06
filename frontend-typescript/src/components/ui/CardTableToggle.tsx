import { HiViewGrid, HiViewList } from "react-icons/hi";
import Button from "./Button";

export function CardTableToggle({
  view,
  onViewChange,
}: {
  view: "cards" | "table";
  onViewChange: (view: "cards" | "table") => void;
}) {
  return (
    <div className="flex justify-end mb-4 space-x-2">
      <Button
        variant="toggle"
        active={view === "cards"}
        onClick={() => onViewChange("cards")}
      >
        <HiViewGrid size={20} />
      </Button>
      <Button
        variant="toggle"
        active={view === "table"}
        onClick={() => onViewChange("table")}
      >
        <HiViewList size={20} />
      </Button>
    </div>
  );
}
