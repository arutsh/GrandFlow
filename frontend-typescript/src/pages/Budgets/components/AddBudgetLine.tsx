import { editBudget, createBudget } from "@/api/budgetApi";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useMutation } from "@tanstack/react-query";
import { HandPlatter } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Budget } from "../types/budget";
import { useDetailedBudget } from "../SingleBudgetViewContext";
import Input from "@/components/ui/Input";
import Select from "@/components/ui/Select";

interface ExtraField {
  key: string;
  value: string;
}

export function AddBudgetLineModal({
  isOpen,
  onClose,
  onSave,
}: {
  isOpen: boolean;
  onClose: () => void;
  onSave: (line: any) => void; // Replace `any` with proper BudgetLine type
}) {
  const { budget, budgetCategories, budgetCategoryNames } = useDetailedBudget();
  const [categoryName, setCategoryName] = useState("");
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState<number>(0);
  const [extraFields, setExtraFields] = useState<ExtraField[]>([]);

  // 🧠 Extract all unique extra field keys from the existing budget lines
  const existingExtraKeys = useMemo(() => {
    if (!budget?.lines?.length) return [];
    const keys = new Set<string>();
    for (const line of budget.lines) {
      if (line.extra_fields) {
        Object.keys(line.extra_fields).forEach((key) => keys.add(key));
      }
    }
    return Array.from(keys);
  }, [budget]);

  // 🧩 When modal opens, prepopulate existing fields
  useEffect(() => {
    if (isOpen) {
      const prefilled = existingExtraKeys.map((key) => ({
        key,
        value: "",
      }));
      setExtraFields(prefilled);
    }
  }, [isOpen, existingExtraKeys]);

  const handleAddExtraField = () => {
    setExtraFields([...extraFields, { key: "", value: "" }]);
  };

  const handleRemoveExtraField = (index: number) => {
    setExtraFields(extraFields.filter((_, i) => i !== index));
  };

  const handleExtraFieldChange = (
    index: number,
    field: "key" | "value",
    value: string
  ) => {
    const newFields = [...extraFields];
    newFields[index][field] = value;
    setExtraFields(newFields);
  };

  const mutation = useMutation({
    mutationFn: ({
      budgetName,
      funderName,
    }: {
      budgetName: string;
      funderName: string;
    }) =>
      createBudget({
        name: budgetName,
        external_funder_name: funderName,
      }),

    onSuccess: (newBudget) => {
      setErrorMessage("");
      onClose(newBudget);
    },
    onError: () => {
      setErrorMessage("Failed to update budget");
    },
  });

  const handleSave = () => {
    // Construct extraFields as object
    const extraFieldsObj = extraFields.reduce((acc, { key, value }) => {
      if (key) acc[key] = value;
      return acc;
    }, {} as Record<string, string>);

    const newLine = {
      category: { name: categoryName },
      description,
      amount,
      extra_fields: extraFieldsObj,
    };

    onSave(newLine);
    // Reset form
    setCategoryName("");
    setDescription("");
    setAmount(0);
    setExtraFields([]);
  };

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={() => onClose()} title="New Budget Line">
      {/* Category */}
      <Select
        label="Category"
        name="category"
        value={categoryName}
        onChange={(e) => setCategoryName(e.target.value)}
        placeholder="-- Select Category --"
        allowCreate={true}
        createLabel="Create New..."
        options={
          budgetCategories?.map((c) => ({ label: c.name, value: c.id })) ?? []
        }
      />
      {categoryName === "__new" && (
        <Input
          name="categories"
          type="text"
          placeholder="New category name"
          value={categoryName === "__new" ? "" : categoryName}
          onChange={(e) => setCategoryName(e.target.value)}
          showLabel={false}
        />
      )}

      {/* Description */}
      <Input
        label="Description"
        name="description"
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      {/* Amount */}
      <Input
        label="Amount"
        name="amount"
        type="number"
        value={amount}
        onChange={(e) => setAmount(parseFloat(e.target.value))}
      />

      {/* Extra Fields */}
      <div className="mb-4">
        <h3 className="font-semibold mb-2">Extra Fields</h3>
        {extraFields.map((field, index) => (
          <div key={index} className="flex gap-2 mb-2">
            <Input
              name={field.key}
              showLabel={false}
              type="text"
              placeholder="Key"
              value={field.key}
              onChange={(e) =>
                handleExtraFieldChange(index, "key", e.target.value)
              }
              disabled={existingExtraKeys.includes(field.key)} // existing keys locked
            />
            <Input
              name={field.value}
              type="text"
              showLabel={false}
              placeholder="Value"
              value={field.value}
              onChange={(e) =>
                handleExtraFieldChange(index, "value", e.target.value)
              }
            />
            {!existingExtraKeys.includes(field.key) && (
              <Button
                type="button"
                onClick={() => handleRemoveExtraField(index)}
                variant="simpleX"
              >
                X
              </Button>
            )}
          </div>
        ))}
        <Button type="button" variant="text" onClick={handleAddExtraField}>
          + Add Field
        </Button>
      </div>

      {/* Actions */}
      <div className="flex justify-end gap-2">
        <Button variant="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleSave}>
          Save
        </Button>
      </div>
    </Modal>
  );
}
