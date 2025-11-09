import { TableCommon } from "@/components/ui/Table";
import { ColumnDef, createColumnHelper } from "@tanstack/react-table";
import { useMemo, useState } from "react";
import { BudgetLine, NewBudgetLine } from "../types/budget";
import Button, { ConfirmDeleteButton } from "@/components/ui/Button";
const columnHelper = createColumnHelper<any>();

export function BudgetViewLinesTable({
  lines,
  onEdit,
  onDelete,
  onNew,
}: {
  lines: BudgetLine[] | undefined;
  onEdit: (BudgetLine: any) => void;
  onDelete: (budget_id: string) => void;
  onNew: () => void;
}) {

  
  const extraFieldKeys = useMemo(() => {
    const keys = new Set<string>();
    lines.forEach((line) => {
      if (line.extra_fields) {
        Object.keys(line.extra_fields).forEach((key) => keys.add(key));
      }
    });
    return Array.from(keys);
  }, [lines]);

  const columns = useMemo<ColumnDef<BudgetLine>[]>(
    () => [
      {
        header: "Category",
        accessorFn: (row) => row.category?.name ?? "—",
        id: "category",
        enableSorting: true,
      },
      {
        header: "Description",
        accessorKey: "description",
        enableSorting: true,
      },
      {
        header: "Amount (£)",
        accessorKey: "amount",
        cell: (info) => (
          <span className="font-semibold">
            {info.getValue<number>().toLocaleString()}
          </span>
        ),
      },
      // Dynamically add columns for extra_fields
      ...extraFieldKeys.map((key) => ({
        header: key,
        accessorFn: (row) => row.extra_fields?.[key] ?? "—",
        id: key, // important for unique identification
      })),
      columnHelper.display({
        id: "actions",
        enableSorting: false,
        cell: (info) => (
          <div className="flex space-x-2">
            <Button onClick={() => onEdit(info.row.original)}>Edit</Button>

            <ConfirmDeleteButton
              onConfirm={() => onDelete(info.row.original.id)}
            />
          </div>
        ),
      }),
    ],
    [extraFieldKeys]
  );

  return (
    <>
      <h2 className="w-full text-lg py-5 font-semibold text-slate-700 mb-4">
        Budget Lines
      </h2>
      <div>
        <Button onClick={onNew}>New expense</Button>
      </div>
      <TableCommon data={lines} columns={columns} />
    </>
  );
}
