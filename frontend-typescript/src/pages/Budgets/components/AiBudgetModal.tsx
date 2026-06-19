import React, { useState, useRef } from "react";
import Button from "@/components/ui/Button";
import {
  streamParseBudget,
  createBudgetWithLines,
} from "@/api/budgetApi";
import {
  Budget,
  BudgetLinePreview,
  ParseBudgetResponse,
} from "../types/budget";

type Step = "input" | "streaming" | "preview" | "creating";

interface Props {
  isOpen: boolean;
  onClose: (created: Budget | null) => void;
}

export function AiBudgetModal({ isOpen, onClose }: Props) {
  const [step, setStep] = useState<Step>("input");
  const [description, setDescription] = useState("");
  const [progressMessage, setProgressMessage] = useState("");
  const [preview, setPreview] = useState<ParseBudgetResponse | null>(null);
  const [editedLines, setEditedLines] = useState<BudgetLinePreview[]>([]);
  const [budgetName, setBudgetName] = useState("");
  const [funderName, setFunderName] = useState("");
  const [durationMonths, setDurationMonths] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  if (!isOpen) return null;

  const handleGenerate = () => {
    if (!description.trim()) return;
    setStep("streaming");
    setProgressMessage("Starting...");
    setErrorMessage("");

    abortRef.current = streamParseBudget(
      description,
      (status) => setProgressMessage(status),
      (response) => {
        setPreview(response);
        setBudgetName(response.budget_name);
        setFunderName(response.external_funder_name || "");
        setDurationMonths(response.duration_months ?? null);
        setEditedLines(response.lines);
        setStep("preview");
      },
      (msg) => {
        setErrorMessage(msg || "Something went wrong. Try rephrasing.");
        setStep("input");
      },
      () => {
        setErrorMessage(
          "AI is not available right now. Use the manual form instead."
        );
        setStep("input");
      }
    );
  };

  const handleCancel = () => {
    abortRef.current?.abort();
    setStep("input");
  };

  const handleCreate = async () => {
    setStep("creating");
    try {
      const created = await createBudgetWithLines({
        budget_name: budgetName,
        external_funder_name: funderName || "",
        duration_months: durationMonths,
        lines: editedLines,
      });
      onClose(created);
    } catch {
      setErrorMessage("Failed to create budget. Please try again.");
      setStep("preview");
    }
  };

  const handleLineChange = (
    index: number,
    field: keyof BudgetLinePreview,
    value: string | number
  ) => {
    setEditedLines((lines) =>
      lines.map((line, i) => (i === index ? { ...line, [field]: value } : line))
    );
  };

  const handleRemoveLine = (index: number) => {
    setEditedLines((lines) => lines.filter((_, i) => i !== index));
  };

  const totalAmount = editedLines.reduce((s, l) => s + Number(l.amount), 0);

  return (
    <div className="fixed inset-0 bg-gray-900/80 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-lg w-full max-w-3xl max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200">
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              AI Budget Generator
            </h2>
            <p className="text-sm text-slate-500 mt-0.5">
              Describe your budget in plain language
            </p>
          </div>
          <Button
            variant="close"
            onClick={() => {
              abortRef.current?.abort();
              onClose(null);
            }}
          >
            ✕
          </Button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6">
          {errorMessage && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
              {errorMessage}
            </div>
          )}

          {step === "input" && (
            <textarea
              className="w-full border border-slate-300 rounded-lg p-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-slate-400"
              rows={6}
              placeholder="e.g. 12-month staff grant for community programs. Need a program coordinator at $50k, admin support at $25k, and $5k for supplies. Funded by the City Foundation."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          )}

          {step === "streaming" && (
            <div className="flex flex-col items-center justify-center py-12 space-y-4">
              <div className="w-8 h-8 border-4 border-slate-300 border-t-slate-700 rounded-full animate-spin" />
              <p className="text-sm text-slate-600">{progressMessage}</p>
            </div>
          )}

          {(step === "preview" || step === "creating") && preview && (
            <div className="space-y-5">
              {/* Budget metadata */}
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

              {/* Budget lines table */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-semibold text-slate-700">
                    Budget Lines
                  </h3>
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
                                handleLineChange(
                                  i,
                                  "category_name",
                                  e.target.value
                                )
                              }
                              className="w-full bg-transparent border border-transparent focus:border-slate-300 rounded px-1 py-0.5 focus:outline-none"
                            />
                          </td>
                          <td className="px-3 py-1.5">
                            <input
                              type="text"
                              value={line.description}
                              onChange={(e) =>
                                handleLineChange(
                                  i,
                                  "description",
                                  e.target.value
                                )
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
                              onClick={() => handleRemoveLine(i)}
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
                <p className="text-xs text-slate-400 mt-2">
                  Prompt version: {preview.prompt_version}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-slate-200 flex justify-end gap-3">
          {step === "input" && (
            <>
              <Button variant="secondary" onClick={() => onClose(null)}>
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={handleGenerate}
                disabled={!description.trim()}
              >
                Generate Budget
              </Button>
            </>
          )}
          {step === "streaming" && (
            <Button variant="secondary" onClick={handleCancel}>
              Cancel
            </Button>
          )}
          {step === "preview" && (
            <>
              <Button
                variant="secondary"
                onClick={() => {
                  setStep("input");
                  setPreview(null);
                }}
              >
                Start Over
              </Button>
              <Button
                variant="primary"
                onClick={handleCreate}
                disabled={!budgetName.trim() || editedLines.length === 0}
              >
                Create Budget
              </Button>
            </>
          )}
          {step === "creating" && (
            <Button variant="primary" disabled>
              Creating...
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
