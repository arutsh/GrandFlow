import { Card, CardContent, CardHeader } from "@/components/ui/Card";

function ownerTypeLabel(owner?: { is_ngo?: boolean; is_donor?: boolean } | null): string {
  const tags = [owner?.is_ngo && "NGO", owner?.is_donor && "Donor"].filter(Boolean);
  return tags.length ? ` (${tags.join(" / ")})` : "";
}

export function BudgetViewHeader({ budget }: { budget: any }) {
  return (
    <Card className="w-full bg-gray-50  py-5 border-b border-gray-200">
      <CardHeader className=" ">
        <h1 className="text-2xl font-semibold">{budget.name}</h1>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-300 mt-1">
          Owner: {budget.owner?.name ?? "Unknown"}{ownerTypeLabel(budget.owner)}
        </p>
        <p className="text-sm text-gray-300">Funder: {budget.funder?.name ?? "—"}</p>
      </CardContent>
    </Card>
  );
}
