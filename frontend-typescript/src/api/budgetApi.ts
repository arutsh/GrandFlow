import { createAxiosInstance } from "./axiosConfig";
import gatewayApi from "@/api/gatewayApi";

// const budgetApi = createAxiosInstance(
//   import.meta.env.API_BUDGET_SERVICE || "http://localhost:8001/api"
// );
// export default budgetApi;

// // Example API calls
// export const getBudgetLines = async () => {
//   const { data } = await budgetApi.get("/budget-lines");
//   return data;
// };


export const editBudget = async (id: string, budgetData: any) => {
  const { data } = await gatewayApi.put(`/budgets/${id}/`, budgetData);
  return data;
};

export const deleteBudget = async (id: string) => {
  const { data } = await gatewayApi.delete(`/budgets/${id}/`);
  return data;
}