import { editBudget } from "@/api/budgetApi";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useMutation } from "@tanstack/react-query";
import { HandPlatter } from "lucide-react";
import { useEffect, useState } from "react";
import { Budget } from "../types/budget";

export function EditBudgetModal({
  isOpen,
  onClose,
  data,
}: {
  isOpen: boolean;
  onClose: (updatedBudget: Budget | null) => void;
  data: Budget;
}) {
  const [budgetName, setBudgetName] = useState(data?.name || "");
  const [funderName, setFunderName] = useState(data?.funder?.name || "");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (data) {
      setBudgetName(data.name || "");
      setFunderName(data.funder?.name || "");
    }
  }, [data]);

  const mutation = useMutation({
    mutationFn: ({
      budgetName,
      funderName,
    }: {
      budgetName: string;
      funderName: string;
    }) =>
      editBudget(data.id, {
        name: budgetName,
        external_funder_name: funderName,
      }),

    onSuccess: (updatedBudget) => {
      setErrorMessage("");
      onClose(updatedBudget);
    },
    onError: () => {
      setErrorMessage("Failed to update budget");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate({
      budgetName,
      funderName,
    });
  };

  console.log("EditBudgetModal - data:", data);
  return (
    <Modal isOpen={isOpen} onClose={() => onClose(null)} title="New Budget">
      {errorMessage && <p className="text-red-500">{errorMessage}</p>}
      {data && (
        <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
          <input
            type="text"
            value={budgetName}
            onChange={(e) => setBudgetName(e.target.value)}
            placeholder="Budget Name"
            className="border p-2 rounded w-full"
          />
          <input
            type="text"
            value={funderName}
            onChange={(e) => setFunderName(e.target.value)}
            placeholder="Funder name"
            className="border p-2 rounded w-full"
          />
          <div className="flex justify-end space-x-2">
            <Button type="submit">Save</Button>
            <Button variant="secondary" onClick={() => onClose(null)}>
              Cancel
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
}
