import React, { useEffect, useState } from "react";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { useMutation, useQueries, useQuery } from "@tanstack/react-query";
import { userOnboarding } from "@/api/usersApi";
import { useAuth } from "@/context/AuthContext";
import { getUserIdFromToken } from "@/utils/token";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../Dashboard/DashboardLayout";
import { fetchAllBudgets } from "@/api/gatewayApi";
import { utcToLocal } from "@/utils/datetime";
import { HiViewGrid, HiViewList } from "react-icons/hi";
import { TableView } from "./components/TableView";
import { CardsView } from "./components/CardsView";
import { EditBudgetModal } from "./components/EditBudget";
import { CardTableToggle } from "@/components/ui/CardTableToggle";

const BudgetsPage: React.FC = () => {
  // Placeholder content for the Budgets page
  const [view, setView] = useState<"cards" | "table">("cards");
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [editingBudget, setEditingBudget] = useState<any>(null);

  const openEditModal = (budget: any) => {
    setEditingBudget(budget);
    setIsEditOpen(true);
  };

  const closeEditModal = () => {
    setEditingBudget(null);
    setIsEditOpen(false);
  };

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
      <EditBudgetModal
        isOpen={isEditOpen}
        onClose={closeEditModal}
        data={editingBudget}
      />
      <div className="flex bg-blue-700 flex-col items-center  min-h-screen bg-gray-50">
        <h1 className="text-2xl font-bold mb-4">Budgets Page</h1>
        <CardTableToggle
          view={view}
          onViewChange={(newView) => setView(newView)}
        />
        {data && data.length > 0 ? (
          <>
            {view === "cards" ? (
              <CardsView data={data} onEdit={openEditModal} />
            ) : (
              <TableView data={data} onEdit={openEditModal} />
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
