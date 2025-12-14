import Button, { ConfirmDeleteButton } from "@/components/ui/Button";
import { utcToLocal } from "@/utils/datetime";
import { Budget } from "../types/budget";

export function CardsView({
  data,
  onEdit,
  onDelete,
}: {
  data: Budget[];
  onEdit: (budget: Budget) => void;
  onDelete: (budget_id: string) => void;
}) {
  const redirectToBudget = (budgetId: string) => {
    // Placeholder for redirect logic
    window.location.href = `/budgets/${budgetId}`;
  };

  return (
    <ul className="space-y-4 w-full max-w-5xl mx-auto">
      {data.map((budget: Budget) => (
        <li
          key={budget.id}
          className="p-4 bg-white rounded shadow flex flex-col md:flex-row justify-between items-start md:items-center hover:bg-slate-300 cursor-pointer"
          onClick={() => redirectToBudget(budget.id)}
        >
          <div>
            <h2 className="text-lg font-semibold">{budget.name}</h2>
            <p>Funder: {budget.funder?.name}</p>
            <p>Status: {budget.status}</p>
            <p>Duration (months): {budget.duration_months}</p>
            <p>Local Currency: {budget.local_currency}</p>
            <p>
              Created: {budget?.trace?.created?.user?.first_name}{" "}
              {budget?.trace?.created?.user?.last_name} -{" "}
              {utcToLocal(budget?.trace?.created?.event_date)}
            </p>
            <p>
              Updated: {budget?.trace?.updated?.user?.first_name}{" "}
              {budget?.trace?.updated?.user?.last_name} -{" "}
              {utcToLocal(budget?.trace?.updated?.event_date)}
            </p>
          </div>
          <div className="flex space-x-2 mt-2 md:mt-0" onClick={(e) => e.stopPropagation()}>
            <Button onClick={() => onEdit(budget)}>Edit</Button>
            <ConfirmDeleteButton onConfirm={() => onDelete(budget.id)} />
          </div>
        </li>
      ))}
    </ul>
  );
}
