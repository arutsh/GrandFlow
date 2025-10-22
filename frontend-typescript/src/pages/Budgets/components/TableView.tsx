import Button from "@/components/ui/Button";
import { utcToLocal } from "@/utils/datetime";
import {
  createColumnHelper,
  useReactTable,
  getCoreRowModel,
} from "@tanstack/react-table";
import { flexRender } from "@tanstack/react-table";

const columnHelper = createColumnHelper<any>();

export function TableView({
  data,
  onEdit,
}: {
  data: any[];
  onEdit: (budget: any) => void;
}) {
  const columns = [
    columnHelper.accessor("name", { header: "Name" }),
    columnHelper.accessor("funder", {
      header: "Funder",
      cell: (info) => info.getValue()?.name || "N/A",
    }),
    columnHelper.accessor("amount", {
      header: "Amount",
      cell: (info) => `$${info.getValue()?.toFixed(2) || "0.00"}`,
    }),
    columnHelper.accessor("trace", {
      header: "Created At",
      cell: (info) => utcToLocal(info.getValue()?.created.event_date),
    }),
    columnHelper.accessor("trace", {
      header: "Created By",
      cell: (info) =>
        `${info.getValue()?.created.user?.first_name || ""} ${
          info.getValue()?.created.user?.last_name || ""
        }`,
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
        <div className="flex space-x-2">
          <Button onClick={() => onEdit(info.row.original)}>Edit</Button>
          <Button variant="danger">Delete</Button>
        </div>
      ),
    }),
  ];

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <table className="min-w-full divide-y divide-gray-200 bg-white shadow rounded">
      <thead className="bg-gray-50">
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th
                key={header.id}
                className="px-4 py-2 text-left text-sm font-medium text-gray-700"
              >
                {header.isPlaceholder
                  ? null
                  : flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody className="divide-y divide-gray-200">
        {table.getRowModel().rows.map((row) => (
          <tr key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <td key={cell.id} className="px-4 py-2 text-sm text-gray-700">
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
