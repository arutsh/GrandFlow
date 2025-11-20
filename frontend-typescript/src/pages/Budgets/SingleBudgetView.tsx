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
import { Budget, BudgetLine } from "./types/budget";
import {
  SingleBudgetViewContextProvider,
  useDetailedBudget,
} from "./SingleBudgetViewContext";
import { AddBudgetLineModal } from "./components/AddBudgetLine";

export function SingleBudgetViewContainer() {
  const { id } = useParams<{ id: string }>();
  return (
    <DashboardLayout>
      <SingleBudgetViewContextProvider id={id}>
        <SingleBudgetView id={id} />
      </SingleBudgetViewContextProvider>
    </DashboardLayout>
  );
}

function SingleBudgetView({ id }: { id: string }) {
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState<BudgetLine | boolean>(false);
  // const
  const { budget } = useDetailedBudget();

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
      {isEditOpen && (
        <AddBudgetLineModal
          budgetLine={isEditOpen}
          isOpen={isEditOpen}
          onClose={() => {
            setIsEditOpen(false);
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
            onEdit={(value) => {
              console.log("eesit button cliekd = ", value);
              setIsEditOpen(value);
            }}
            // onDelete={() => {}}
            onNew={() => setIsAddOpen(!isAddOpen)}
            onClose={() => {
              setIsAddOpen(false), setIsEditOpen(false);
            }}
          />
          <BudgetViewTraces budget={budget} />
        </div>
      )}
    </>
  );
}

export default SingleBudgetView;
