import React, { useState, useEffect } from "react";
import Button from "@/components/ui/Button";
import {
  Budget,
  BudgetLinePreview,
  ParseBudgetResponse,
} from "../types/budget";
import { createBudgetWithLines } from "@/api/budgetApi";

interface Props {
  preview: ParseBudgetResponse;
  onCreated: (budget: Budget) => void;
  onDismiss: () => void;
}

export function AiBudgetPreviewCard({ preview, onCreated, onDismiss }: Props) {
  const [budgetName, setBudgetName] = useState(preview.budget_name);
  const [funderName, setFunderName] = useState(
    preview.external_funder_name || ""
  );
  const [durationMonths, setDurationMonths] = useState<number | null>(
    preview.duration_months
  );
  const [editedLines, setEditedLines] = useState<BudgetLinePreview[]>(
    preview.lines
  );
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setBudgetName(preview.budget_name);
    setFunderName(preview.external_funder_name || "");
    setDurationMonths(preview.duration_months);
    setEditedLines(preview.lines);
    setError("");
  }, [preview]);

  const handleCreate = async () => {
    setIsCreating(true);
    try {
      const created = await createBudgetWithLines({
        budget_name: budgetName,
        external_funder_name: funderName || "",
        duration_months: durationMonths,
        lines: editedLines,
      });
      if (!created?.id) {
        setError("Budget was created but the response was invalid. Check the budget list.");
        setIsCreating(false);
        return;
      }
      onCreated(created);
    } catch {
      setError("Failed to create budget. Please try again.");
      setIsCreating(false);
    }
  };

  const handleLineChange = (
    i: number,
    field: keyof BudgetLinePreview,
    value: string | number
  ) => {
    setEditedLines((lines) =>
      lines.map((l, idx) => (idx === i ? { ...l, [field]: value } : l))
    );
  };

  const totalAmount = editedLines.reduce((s, l) => s + Number(l.amount), 0);

  return (
    <div className="mb-6 flex-shrink-0 bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Card header */}
      <div className="flex items-center justify-between px-5 py-3 bg-slate-50 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
            AI Preview
          </span>
          <span className="text-xs text-slate-400">
            · prompt v{preview.prompt_version}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            onClick={onDismiss}
            className="text-xs py-1 px-3"
          >
            Discard
          </Button>
          <Button
            variant="primary"
            onClick={handleCreate}
            disabled={
              isCreating || !budgetName.trim() || editedLines.length === 0
            }
            className="text-xs py-1 px-3"
          >
            {isCreating ? "Creating..." : "Create Budget"}
          </Button>
        </div>
      </div>

      <div className="p-5 space-y-4">
        {error && <p className="text-sm text-red-600">{error}</p>}

        {/* Metadata */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-medium text-slate-500 mb-1">
              Budget Name
            </label>
            <input
              type="text"
              value={budgetName}
              onChange={(e) => setBudgetName(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-500 mb-1">
              Funder Name
            </label>
            <input
              type="text"
              value={funderName}
              onChange={(e) => setFunderName(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-500 mb-1">
              Duration (months)
            </label>
            <input
              type="number"
              min={1}
              value={durationMonths ?? ""}
              onChange={(e) =>
                setDurationMonths(
                  e.target.value ? parseInt(e.target.value) : null
                )
              }
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
            />
          </div>
        </div>

        {/* Lines table */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold text-slate-700">
              Budget Lines
            </span>
            <span className="text-xs font-medium text-slate-500">
              Total: ${totalAmount.toLocaleString()}
            </span>
          </div>
          <div className="overflow-x-auto border border-slate-200 rounded-lg">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="text-left px-3 py-2 font-medium text-slate-600">
                    Category
                  </th>
                  <th className="text-left px-3 py-2 font-medium text-slate-600">
                    Description
                  </th>
                  <th className="text-right px-3 py-2 font-medium text-slate-600">
                    Amount ($)
                  </th>
                  <th className="px-2 py-2" />
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {editedLines.map((line, i) => (
                  <tr key={i} className="hover:bg-slate-50">
                    <td className="px-3 py-1.5">
                      <input
                        type="text"
                        value={line.category_name}
                        onChange={(e) =>
                          handleLineChange(i, "category_name", e.target.value)
                        }
                        className="w-full bg-transparent border border-transparent focus:border-slate-300 rounded px-1 py-0.5 focus:outline-none"
                      />
                    </td>
                    <td className="px-3 py-1.5">
                      <input
                        type="text"
                        value={line.description}
                        onChange={(e) =>
                          handleLineChange(i, "description", e.target.value)
                        }
                        className="w-full bg-transparent border border-transparent focus:border-slate-300 rounded px-1 py-0.5 focus:outline-none"
                      />
                    </td>
                    <td className="px-3 py-1.5">
                      <input
                        type="number"
                        min={0}
                        value={line.amount}
                        onChange={(e) =>
                          handleLineChange(
                            i,
                            "amount",
                            parseFloat(e.target.value) || 0
                          )
                        }
                        className="w-full text-right bg-transparent border border-transparent focus:border-slate-300 rounded px-1 py-0.5 focus:outline-none"
                      />
                    </td>
                    <td className="px-2 py-1.5 text-center">
                      <Button
                        variant="icon-danger"
                        onClick={() =>
                          setEditedLines((lines) =>
                            lines.filter((_, idx) => idx !== i)
                          )
                        }
                        title="Remove line"
                      >
                        ✕
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
