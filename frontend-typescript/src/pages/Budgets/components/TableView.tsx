import Button, { ConfirmDeleteButton } from "@/components/ui/Button";
import { TableCommon } from "@/components/ui/Table";
import { utcToLocal } from "@/utils/datetime";
import { createColumnHelper } from "@tanstack/react-table";
import { Edit2, Trash2 } from "lucide-react";

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
  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case "approved":
        return "bg-green-100 text-green-800";
      case "draft":
        return "bg-yellow-100 text-yellow-800";
      case "rejected":
        return "bg-red-100 text-red-800";
      default:
        return "bg-slate-100 text-slate-800";
    }
  };

  const columns = [
    columnHelper.accessor("status", {
      header: "Status",
      cell: (info) => (
        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(info.getValue())}`}
        >
          {info.getValue()}
        </span>
      ),
    }),
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
      id: "trace_updated_by",
      header: "Updated By",
      cell: (info) =>
        `${info.getValue()?.updated.user?.first_name || ""} ${
          info.getValue()?.updated.user?.last_name || ""
        }`,
    }),
    columnHelper.display({
      id: "actions",
      cell: (info) => (
        <div
          className="flex space-x-1 gap-1"
          onClick={(e) => e.stopPropagation()}
        >
          <Button
            onClick={() => onEdit(info.row.original)}
            variant="icon"
            title="Edit budget"
          >
            <Edit2 size={18} />
          </Button>

          <Button
            variant="icon-danger"
            onClick={() => onDelete(info.row.original.id)}
            title="Delete budget"
          >
            <Trash2 size={18} />
          </Button>
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
