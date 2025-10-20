import Button from "@/components/ui/Button";
import { utcToLocal } from "@/utils/datetime";

export function CardsView({
  data,
  onEdit,
}: {
  data: any[];
  onEdit: (budget: any) => void;
}) {
  return (
    <ul className="space-y-4 w-full max-w-5xl mx-auto">
      {data.map((budget: any) => (
        <li
          key={budget.id}
          className="p-4 bg-white rounded shadow flex flex-col md:flex-row justify-between items-start md:items-center"
        >
          <div>
            <h2 className="text-lg font-semibold">{budget.name}</h2>
            <p>Funder: {budget.funder?.name}</p>
            <p>Amount: ${budget.amount}</p>
            <p>Created At: {utcToLocal(budget.created_at)}</p>
            <p>
              Created By: {budget.created_by?.first_name}{" "}
              {budget.created_by?.last_name}
            </p>
            <p>Updated At: {utcToLocal(budget.updated_at)}</p>
            <p>
              Updated By: {budget.updated_by?.first_name}{" "}
              {budget.updated_by?.last_name}
            </p>
          </div>
          <div className="flex space-x-2 mt-2 md:mt-0">
            <Button onClick={() => onEdit(budget)}>Edit</Button>
            <Button variant="danger">Delete</Button>
          </div>
        </li>
      ))}
    </ul>
  );
}
