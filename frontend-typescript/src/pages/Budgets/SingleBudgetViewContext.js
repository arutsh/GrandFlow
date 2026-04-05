import { jsx as _jsx } from "react/jsx-runtime";
import { createContext, useContext, useMemo, } from "react";
import { fetchBudgetById } from "@/api/gatewayApi";
import { useQuery, useQueryClient } from "@tanstack/react-query";
const SingleBudgetViewContext = createContext(undefined);
export const SingleBudgetViewContextProvider = ({ id, children }) => {
    // const [budget, setBudget] = useState<Budget | null>(null);
    const queryClient = useQueryClient();
    // ✅ Fetch budget here
    const { data: budget, isPending, isError, error, refetch, } = useQuery({
        queryKey: ["budgetDetails", id],
        queryFn: () => (id ? fetchBudgetById(id) : Promise.resolve(null)),
        enabled: !!id,
    });
    const totalAmount = useMemo(() => {
        if (!budget?.lines)
            return 0;
        return budget.lines.reduce((sum, line) => sum + (line.amount || 0), 0);
    }, [budget]);
    // ✅ Derive unique categories from budget lines
    const budgetCategories = useMemo(() => {
        if (!budget?.lines)
            return [];
        const unique = Object.values(budget.lines.reduce((acc, { category }) => {
            if (category && !acc[category.id])
                acc[category.id] = category;
            return acc;
        }, {}));
        return unique;
    }, [budget]);
    const existingExtraKeys = useMemo(() => {
        if (!budget?.lines?.length)
            return [];
        const keys = new Set();
        for (const line of budget.lines) {
            if (line.extra_fields) {
                Object.keys(line.extra_fields).forEach((key) => keys.add(key));
            }
        }
        return Array.from(keys);
    }, [budget]);
    // ✅ Extract category names from categories
    const budgetCategoryNames = useMemo(() => {
        return budgetCategories
            .filter((c) => c !== null && c !== undefined)
            .map((c) => c.name)
            .filter(Boolean);
    }, [budgetCategories]);
    // ✅ Wrapper setter (updates both state + query cache)
    const setBudget = (updated) => {
        queryClient.setQueryData(["budgetDetails", id], updated);
    };
    return (_jsx(SingleBudgetViewContext.Provider, { value: {
            budget,
            setBudget,
            budgetCategories,
            budgetCategoryNames,
            totalAmount,
            existingExtraKeys,
        }, children: children }));
};
export const useDetailedBudget = () => {
    const ctx = useContext(SingleBudgetViewContext);
    if (!ctx)
        throw new Error("useDetailedBudget must be used within a SingleBudgetViewContextProvider");
    return ctx;
};
