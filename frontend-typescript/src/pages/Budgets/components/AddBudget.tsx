import { editBudget, createBudget } from "@/api/budgetApi";
import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";
import { useMutation } from "@tanstack/react-query";

import { useState } from "react";
import { Budget } from "../types/budget";

export function AddBudgetModal({
  isOpen,
  onClose,
}: {
  isOpen: boolean;
  onClose: (updatedBudget: Budget | null) => void;
}) {
  const [budgetName, setBudgetName] = useState("");
  const [funderName, setFunderName] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate({
      budgetName,
      funderName,
    });
  };

  return (
    <Modal isOpen={isOpen} onClose={() => onClose(null)} title="Edit Budget">
      {errorMessage && <p className="text-red-500">{errorMessage}</p>}
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
    </Modal>
  );
}
