import {
  createColumnHelper,
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
  ColumnDef,
  SortingState,
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
    <th
      key={key}
      className="px-4 py-2 text-left text-sm font-medium  text-gray-700"
      onClick={onClick}
    >
      {children}
    </th>
  );
}
export function TableCell({ key, children }: { key?: any; children: any }) {
  return (
    <th
      key={key}
      className="px-4 py-2 text-left text-sm font-normal  text-gray-700"
    >
      {children}
    </th>
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
  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
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
      <TableBody>
        {table.getRowModel().rows.map((row) => (
          <TableRow key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <TableCell key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
