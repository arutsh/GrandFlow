import gatewayApi from "@/api/gatewayApi";

export const editBudget = async (id: string, budgetData: any) => {
  const { data } = await gatewayApi.put(`/budgets/${id}/`, budgetData);
  return data;
};

export const deleteBudget = async (id: string) => {
  const { data } = await gatewayApi.delete(`/budgets/${id}/`);
  return data;
}