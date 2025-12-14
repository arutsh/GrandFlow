import Button, { ConfirmDeleteButton } from "@/components/ui/Button";
import { TableCommon } from "@/components/ui/Table";
import { utcToLocal } from "@/utils/datetime";
import { createColumnHelper } from "@tanstack/react-table";

const columnHelper = createColumnHelper<any>();

export function TableView({
  data,
  onEdit,
  onDelete,
}: {
  data: any[];
  onEdit: (budget: any) => void;
  onDelete: (budget_id: string) => void;
}) {
  const columns = [
    columnHelper.accessor("status", { header: "Status" }),
    columnHelper.accessor("name", { header: "Name" }),

    columnHelper.accessor("funder", {
      header: "Funder",
      cell: (info) => info.getValue()?.name || "N/A",
    }),
    columnHelper.accessor("amount", {
      header: "Amount",
      cell: (info) => `$${info.getValue()?.toFixed(2) || ""}`,
    }),
    columnHelper.accessor("duration_months", {
      header: "Duration (months)",
      cell: (info) => info.getValue()?.toString() || "N/A",
    }),
    columnHelper.accessor("local_currency", {
      header: "Currency",
      cell: (info) => info.getValue() || "N/A",
    }),
    columnHelper.accessor("trace", {
      header: "Updated At",
      cell: (info) => utcToLocal(info.getValue()?.updated.event_date),
    }),
    columnHelper.accessor("trace", {
      header: "Updated By",
      cell: (info) =>
        `${info.getValue()?.updated.user?.first_name || ""} ${
          info.getValue()?.updated.user?.last_name || ""
        }`,
    }),
    columnHelper.display({
      id: "actions",
      cell: (info) => (
        <div className="flex space-x-2" onClick={(e) => e.stopPropagation()}>
          <Button onClick={() => onEdit(info.row.original)}>Edit</Button>

          <ConfirmDeleteButton
            onConfirm={() => onDelete(info.row.original.id)}
          />
        </div>
      ),
    }),
  ];

  const redirectToBudget = (budgetId: string) => {
    // Placeholder for redirect logic
    window.location.href = `/budgets/${budgetId}`;
  };

  return (
    <TableCommon
      data={data}
      columns={columns}
      onRowClick={(row) => redirectToBudget(row.id)}
    />
  );
}
