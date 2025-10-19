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

const BudgetsPage: React.FC = () => {
  // Placeholder content for the Budgets page
  const [view, setView] = useState<"cards" | "table">("cards");
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
      <div className="flex flex-col items-center  min-h-screen bg-gray-50">
        <h1 className="text-2xl font-bold mb-4">Budgets Page</h1>
        <div className="flex justify-end mb-4 space-x-2">
          <button
            onClick={() => setView("cards")}
            className={`p-2 rounded ${
              view === "cards" ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            <HiViewGrid size={20} />
          </button>
          <button
            onClick={() => setView("table")}
            className={`p-2 rounded ${
              view === "table" ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            <HiViewList size={20} />
          </button>
        </div>

        {data && data.length > 0 ? (
          <>
            {view === "cards" ? (
              <CardsView data={data} />
            ) : (
              <TableView data={data} />
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
