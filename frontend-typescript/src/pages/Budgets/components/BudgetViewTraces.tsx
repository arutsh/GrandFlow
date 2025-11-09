import { Card, CardContent, CardHeader } from "@/components/ui/Card";

export function BudgetViewTraces({ budget }: { budget: any }) {
  return (
    <Card className="grid md:grid-cols-2 gap-4 m-5 p-6 bg-gray-50 border-b border-gray-200">
      <CardHeader className="p-4 bg-white rounded-lg border border-gray-200">
        <h3 className="text-slate-700 font-semibold mb-2">Created</h3>
        <p className="text-sm text-gray-700">
          {budget.trace.created.user.first_name}{" "}
          {budget.trace.created.user.last_name}
        </p>
        <p className="text-sm text-gray-500">
          {budget.trace.created.user.email}
        </p>
        <p className="text-xs text-gray-400 mt-1">
          {new Date(budget.trace.created.event_date).toLocaleString()}
        </p>
      </CardHeader>
      <CardContent className="p-4 bg-white rounded-lg border border-gray-200">
        <h3 className="text-slate-700 font-semibold mb-2">Last Updated</h3>
        <p className="text-sm text-gray-700">
          {budget.trace.updated.user.first_name}{" "}
          {budget.trace.updated.user.last_name}
        </p>
        <p className="text-sm text-gray-500">
          {budget.trace.updated.user.email}
        </p>
        <p className="text-xs text-gray-400 mt-1">
          {new Date(budget.trace.updated.event_date).toLocaleString()}
        </p>
      </CardContent>
    </Card>
  );
}
