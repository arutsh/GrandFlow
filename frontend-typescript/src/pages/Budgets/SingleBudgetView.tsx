import React, { createContext, useEffect, useState } from "react";
import {
  useMutation,
  useQueries,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { useNavigate, useParams } from "react-router-dom";
import DashboardLayout from "../Dashboard/DashboardLayout";
import { fetchBudgetById } from "@/api/gatewayApi";

import { BudgetViewHeader } from "./components/BudgetViewHeader";

import { BudgetViewLinesTable } from "./components/BudgetViewLinesTable";
import { BudgetViewTraces } from "./components/BudgetViewTraces";
import { BudgetViewSummary } from "./components/BudgetViewSummary";
import { AddBudgetModal } from "./components/AddBudget";
import { Budget } from "./types/budget";
import {
  SingleBudgetViewContextProvider,
  useDetailedBudget,
} from "./SingleBudgetViewContext";
import { AddBudgetLineModal } from "./components/AddBudgetLine";

export function SingleBudgetViewContainer() {
  const { id } = useParams<{ id: string }>();
  return (
    <DashboardLayout>
      <SingleBudgetViewContextProvider>
        <SingleBudgetView id={id} />
      </SingleBudgetViewContextProvider>
    </DashboardLayout>
  );
}

function SingleBudgetView({ id }: { id: string }) {
  const [isAddOpen, setIsAddOpen] = useState(false);
  const { budget, setBudget } = useDetailedBudget();

  const { isPending, isError, isSuccess, data, error } = useQuery({
    queryKey: ["budgetDetails", id],
    queryFn: ({ queryKey }) => fetchBudgetById(queryKey[1] as string),
  });

  if (isSuccess) {
    setBudget(data);
  }
  if (isPending) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error: {error.message}</div>;
  }
  if (data) {
    console.log("fetched data is ", data);
  }
  return (
    <>
      {isAddOpen && (
        <AddBudgetLineModal
          isOpen={isAddOpen}
          onClose={() => {
            setIsAddOpen(!isAddOpen);
          }}
          onSave={() => {}}
        />
      )}
      {budget && (
        <div className="flex flex-col items-center px-10 min-h-screen bg-gray-50">
          <BudgetViewHeader budget={budget} />
          <BudgetViewSummary />
          <BudgetViewLinesTable
            lines={budget.lines}
            onEdit={() => {}}
            onDelete={() => {}}
            onNew={() => setIsAddOpen(!isAddOpen)}
          />
          <BudgetViewTraces budget={budget} />
        </div>
      )}
    </>
  );
}

export default SingleBudgetView;
