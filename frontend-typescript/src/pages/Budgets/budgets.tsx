import React, { useEffect, useState } from "react";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import {
  useMutation,
  useQueries,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import DashboardLayout from "../Dashboard/DashboardLayout";
import { fetchAllBudgets } from "@/api/gatewayApi";
import { utcToLocal } from "@/utils/datetime";
import { HiPlus } from "react-icons/hi";
import { TableView } from "./components/TableView";
import { CardsView } from "./components/CardsView";

import { CardTableToggle } from "@/components/ui/CardTableToggle";
import { Budget, BudgetPatched } from "./types/budget";
import { deleteBudget } from "@/api/budgetApi";
import { AddBudgetModal } from "./components/AddBudget";
import { EditBudgetModal } from "./components/EditBudget";

const BudgetsPage: React.FC = () => {
  // Placeholder content for the Budgets page
  const [view, setView] = useState<"cards" | "table">();
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [editingBudget, setEditingBudget] = useState<Budget | null>(null);

  const queryClient = useQueryClient();
  const openEditModal = (budget: Budget) => {
    setEditingBudget(budget);

    setIsEditOpen(true);
  };

  const closeAddModal = (newBudget: Budget | null) => {
    if (newBudget) {
      queryClient.setQueryData(["budgets"], (oldData: Budget[] | undefined) => {
        if (!oldData) return [];
        return [...oldData, newBudget];
      });
    }
    setIsAddOpen(false);
  };

  const closeEditModal = (updatedBudget: BudgetPatched | null) => {
    if (updatedBudget) {
      queryClient.setQueryData(["budgets"], (oldData: Budget[] | undefined) => {
        if (!oldData) return [];
        return oldData.map((b) => {
          if (b.id === updatedBudget.id) {
            b.name = updatedBudget.name;
            b.funder = {};
            b.funder.name = updatedBudget?.external_funder_name;
            b.funder.id = updatedBudget?.funding_customer_id;
          }
          return b;
        });
      });
    }
    setEditingBudget(null);
    setIsEditOpen(false);
  };
  const deleteBudgetMutation = useMutation({
    mutationFn: async (budgetId: string) => deleteBudget(budgetId),
    onSuccess: (_, budgetId) => {
      // Invalidate and refetch budgets after deletion
      queryClient.setQueryData(["budgets"], (oldData: Budget[] | undefined) => {
        if (!oldData) return [];
        return oldData.filter((b) => b.id !== budgetId);
      });
    },
  });
  const { isPending, isError, data, error } = useQuery({
    queryKey: ["budgets"],
    queryFn: fetchAllBudgets,
  });

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <DashboardLayout>
      {isEditOpen && editingBudget && (
        <EditBudgetModal
          isOpen={isEditOpen}
          onClose={(val) => closeEditModal(val)}
          data={editingBudget}
        />
      )}
      {isAddOpen && (
        <AddBudgetModal
          isOpen={isAddOpen}
          onClose={(val) => closeAddModal(val)}
        />
      )}
      <div className="flex flex-col items-center  min-h-screen bg-gray-50">
        <h1 className="text-2xl font-bold mb-4">Budgets Page</h1>
        <div className="flex border-amber-300 w-full px-15 justify-end mb-4 space-x-2">
          <div>
            <Button onClick={() => setIsAddOpen(!isAddOpen)}>
              <span className="flex items-center text-sm space-x-2 ">
                <HiPlus size={20} /> Add Budget
              </span>
            </Button>
          </div>
          <CardTableToggle
            view={view}
            onViewChange={(newView) => setView(newView)}
          />
        </div>
        {data && data.length > 0 ? (
          <>
            {view === "cards" ? (
              <CardsView
                data={data}
                onEdit={openEditModal}
                onDelete={deleteBudgetMutation.mutate}
              />
            ) : (
              <TableView
                data={data}
                onEdit={openEditModal}
                onDelete={deleteBudgetMutation.mutate}
              />
            )}
          </>
        ) : (
          <p>No budgets found.</p>
        )}
      </div>
    </DashboardLayout>
  );
};

export default BudgetsPage;
