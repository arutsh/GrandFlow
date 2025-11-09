import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import { useDetailedBudget } from "../SingleBudgetViewContext";

export function BudgetViewSummary() {
  const { budget, budgetCategoryNames, totalAmount } = useDetailedBudget();

  const categories = [...new Set(budget?.lines?.map((l) => l?.category?.name))];
  return (
    <Card className="w-full bg-gray-50  py-5 border-b border-gray-200">
      <CardHeader>
        <h2 className="text-lg font-semibold">Budget Summary</h2>
      </CardHeader>
      <CardContent>
        <div>Total Lines: {budget?.lines?.length}</div>
        <div>Total Amount: {totalAmount.toLocaleString()}</div>
        <div>Categories: {categories.join(", ")}</div>
      </CardContent>
    </Card>
  );
}
