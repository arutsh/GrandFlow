import { createAxiosInstance } from "./axiosConfig";

const budgetApi = createAxiosInstance(
  import.meta.env.API_BUDGET_SERVICE || "http://localhost:8001/api"
);

// Example API calls
export const getBudgetLines = async () => {
  const { data } = await budgetApi.get("/budget-lines");
  return data;
};

export default budgetApi;
