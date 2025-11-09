import { Card, CardContent, CardHeader } from "@/components/ui/Card";

export function BudgetViewHeader({ budget }: { budget: any }) {
  return (
    <Card className="w-full bg-gray-50  py-5 border-b border-gray-200">
      <CardHeader className=" ">
        <h1 className="text-2xl font-semibold">{budget.name}</h1>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-300 mt-1">
          Owner: {budget.owner.name} ({budget.owner.type})
        </p>
        <p className="text-sm text-gray-300">Funder: {budget.funder.name}</p>
      </CardContent>
    </Card>
  );
}
