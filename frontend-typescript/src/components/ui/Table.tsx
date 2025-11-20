import {
  createColumnHelper,
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
  ColumnDef,
  SortingState,
  getGroupedRowModel,
  getExpandedRowModel,
} from "@tanstack/react-table";
import { useState } from "react";

export function Table({ children }: { children: any }) {
  return (
    <table className="min-w-full divide-y divide-gray-200 bg-white shadow rounded">
      {children}
    </table>
  );
}

export function TableHead({ children }: { children: any }) {
  return <thead className="bg-gray-50 font-medium">{children}</thead>;
}
export function TableRow({ key, children }: { key: any; children: any }) {
  return <tr key={key}>{children}</tr>;
}

export function TableHeaderCell({
  key,
  children,
  onClick,
}: {
  key: any;
  children: any;
  onClick?: (value: any) => void;
}) {
  return (
    <td
      key={key}
      className="px-4 py-2 text-left text-sm font-medium  text-gray-700"
      onClick={onClick}
    >
      {children}
    </td>
  );
}
export function TableCell({ children }: { children: any }) {
  return (
    <td className="px-4 py-2 text-left text-sm font-normal  text-gray-700">
      {children}
    </td>
  );
}

export function TableBody({ children }: { children: any }) {
  return <tbody className="divide-y divide-gray-200">{children}</tbody>;
}

export function TableCommon({
  data,
  columns,
}: {
  data: any[];
  columns: any[];
}) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});
  const table = useReactTable({
    data,
    columns,
    // state: { sorting, grouping: ["category"], expanded },
    initialState: { grouping: ["category"] }, // let table manage expanded/sorting
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getGroupedRowModel: getGroupedRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
  });

  return (
    <Table>
      <TableHead>
        {table.getHeaderGroups().map((headerGroup) => (
          <TableRow key={headerGroup.id}>
            {headerGroup.headers.map((header) => {
              const sorted = header.column.getIsSorted();
              const canSort = header.column.getCanSort();
              return (
                <TableHeaderCell
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                  {canSort && (
                    <>
                      {sorted ? (
                        sorted === "asc" ? (
                          <span>↑</span>
                        ) : (
                          <span>↓</span>
                        )
                      ) : (
                        <span className="opacity-50 text-xs">↕</span>
                      )}
                    </>
                  )}
                </TableHeaderCell>
              );
            })}
          </TableRow>
        ))}
      </TableHead>
      <tbody className="divide-y divide-gray-200">
        {table.getRowModel().rows.map((row) => (
          <tr key={row.id}>
            {row.getVisibleCells().map((cell) => {
              // IMPORTANT: use cell-level helpers (v8)
              const isGrouped = cell.getIsGrouped();
              const isAggregated = cell.getIsAggregated();
              const isPlaceholder = cell.getIsPlaceholder();

              // Render grouped row: usually only one column (the grouped column) should show
              if (isGrouped) {
                // show expander + the grouped value + count of subRows
                return (
                  <td
                    key={cell.id}
                    className="px-4 py-2 text-left text-sm font-normal text-gray-700"
                  >
                    <button
                      onClick={row.getToggleExpandedHandler()}
                      aria-label="Toggle group"
                      className="mr-2"
                    >
                      {row.getIsExpanded() ? "▼" : "▶"}
                    </button>
                    <strong className="mr-2">
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </strong>
                    <span className="text-gray-400">
                      ({row.subRows.length})
                    </span>
                  </td>
                );
              }

              // Aggregated (subtotal) cell
              if (isAggregated) {
                return (
                  <td
                    key={cell.id}
                    className="px-4 py-2 text-left text-sm font-normal text-gray-700"
                  >
                    {flexRender(
                      cell.column.columnDef.aggregatedCell ??
                        cell.column.columnDef.cell,
                      cell.getContext()
                    )}
                  </td>
                );
              }

              // Placeholder cell for grouped layout (keep cell empty)
              if (isPlaceholder) {
                return <td key={cell.id} className="px-4 py-2" />;
              }

              // Normal cell
              return (
                <td
                  key={cell.id}
                  className="px-4 py-2 text-left text-sm font-normal text-gray-700"
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              );
            })}
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
