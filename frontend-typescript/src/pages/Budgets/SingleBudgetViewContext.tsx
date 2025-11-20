import React, {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

import { useNavigate, useParams } from "react-router-dom";
import DashboardLayout from "../Dashboard/DashboardLayout";
import { fetchBudgetById } from "@/api/gatewayApi";

import { BudgetViewHeader } from "./components/BudgetViewHeader";

import { BudgetViewLinesTable } from "./components/BudgetViewLinesTable";
import { BudgetViewTraces } from "./components/BudgetViewTraces";
import { BudgetViewSummary } from "./components/BudgetViewSummary";
import { AddBudgetModal } from "./components/AddBudget";
import { Budget, BudgetCategory } from "./types/budget";
import { useQuery, useQueryClient } from "@tanstack/react-query";

interface SingleBudgetViewContextType {
  budget: Budget | null;
  setBudget: (b: Budget | null) => void;
  budgetCategories: BudgetCategory[];
  budgetCategoryNames: string[];
  totalAmount: Number;
  existingExtraKeys?: string[];
  // isAddOpen: boolean;
  // openAddModal: () => void;
  // closeAddModal: () => void;
}
const SingleBudgetViewContext = createContext<
  SingleBudgetViewContextType | undefined
>(undefined);

export const SingleBudgetViewContextProvider: React.FC<{
  id: string; // ✅ pass budget ID as prop
  children: React.ReactNode;
}> = ({ id, children }) => {
  // const [budget, setBudget] = useState<Budget | null>(null);
  const queryClient = useQueryClient();
  // ✅ Fetch budget here
  const {
    data: budget,
    isPending,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ["budgetDetails", id],
    queryFn: () => fetchBudgetById(id),
  });

  const totalAmount = useMemo(() => {
    if (!budget?.lines) return 0;
    return budget.lines.reduce((sum, line) => sum + (line.amount || 0), 0);
  }, [budget]);

  // ✅ Derive unique categories from budget lines
  const budgetCategories = useMemo(() => {
    if (!budget?.lines) return [];

    const unique = Object.values(
      budget.lines.reduce((acc, { category }) => {
        if (category && !acc[category.id]) acc[category.id] = category;
        return acc;
      }, {} as Record<string, BudgetCategory>)
    );

    return unique;
  }, [budget]);

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

  // ✅ Extract category names from categories
  const budgetCategoryNames = useMemo(() => {
    return budgetCategories.map((c) => c?.name).filter(Boolean) as string[];
  }, [budgetCategories]);

  // ✅ Wrapper setter (updates both state + query cache)
  const setBudget = (updated: Budget | null) => {
    queryClient.setQueryData(["budgetDetails", id], updated);
  };

  return (
    <SingleBudgetViewContext.Provider
      value={{
        budget,
        setBudget,
        budgetCategories,
        budgetCategoryNames,
        totalAmount,
        existingExtraKeys,
      }}
    >
      {children}
    </SingleBudgetViewContext.Provider>
  );
};

export const useDetailedBudget = (): SingleBudgetViewContextType => {
  const ctx = useContext(SingleBudgetViewContext);
  if (!ctx)
    throw new Error(
      "useDetailedBudget must be used within a SingleBudgetViewContextProvider"
    );
  return ctx;
};
