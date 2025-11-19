import { TableCommon } from "@/components/ui/Table";
import { ColumnDef, createColumnHelper } from "@tanstack/react-table";
import { useMemo, useState } from "react";
import { BudgetLine, NewBudgetLine } from "../types/budget";
import Button, { ConfirmDeleteButton } from "@/components/ui/Button";
import { deleteBudgetLine } from "@/api/gatewayApi";
import { useMutation } from "@tanstack/react-query";
import { useDetailedBudget } from "../SingleBudgetViewContext";
const columnHelper = createColumnHelper<any>();

export function BudgetViewLinesTable({
  lines,
  onEdit,
  // onDelete,
  onNew,
  onClose,
}: {
  lines: BudgetLine[] | undefined;
  onEdit: (BudgetLine: any) => void;
  // onDelete: (budget_id: string) => void;
  onNew: () => void;
  onClose: () => void;
}) {
  const {
    budget,
    setBudget,
    budgetCategories,
    existingExtraKeys,
    budgetCategoryNames,
  } = useDetailedBudget();
  const extraFieldKeys = useMemo(() => {
    const keys = new Set<string>();
    lines.forEach((line) => {
      if (line.extra_fields) {
        Object.keys(line.extra_fields).forEach((key) => keys.add(key));
      }
    });
    return Array.from(keys);
  }, [lines]);

  const mutation = useMutation({
    mutationFn: (budget_line_id: string) => {
      // Call the API to delete the budget line
      return deleteBudgetLine(budget_line_id);
    },
    onSuccess: (_, budget_line_id) => {
      // On success, you might want to refetch the budget lines or update the state
      if (!budget) return;
      console.log(
        `Budget line with id ${budget_line_id} deleted successfully.`
      );
      const updatedBudget = {
        ...budget,
        lines: budget.lines?.filter((line) => line.id !== budget_line_id),
      };
      setBudget(updatedBudget);
    },
    onError: (error) => {
      console.error("Error deleting budget line:", error);
    },
  });

  const onDelete = (budget_line_id: string) => {
    console.log("Delete clicked for line id:", budget_line_id);
    mutation.mutate(budget_line_id);
  };
  const columns = useMemo<ColumnDef<BudgetLine>[]>(
    () => [
      {
        header: "Category",
        accessorFn: (row) => row.category?.name ?? "—",
        id: "category",
        enableSorting: true,
        enableGrouping: true,
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
        aggregationFn: "sum",
        aggregatedCell: (info) => {
          const value = info.getValue() as number;
          return (
            <span className="font-semibold">
              Subtotal: {value.toLocaleString()}
            </span>
          );
        },
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
      <div className="flex justify-end mb-4 w-full">
        <Button onClick={onNew}>New Budget Line</Button>
      </div>
      <TableCommon data={lines} columns={columns} />
    </>
  );
}
