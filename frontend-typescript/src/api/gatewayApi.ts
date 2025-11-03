import { getUserIdFromToken } from "@/utils/token";
import { createAxiosInstance } from "./axiosConfig";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "@/context/AuthContext";



const gatewayApi = createAxiosInstance(
  import.meta.env.API_GATEWAY || "http://localhost:8082/api/v1"
);

// Example API calls
export const loginUser = async (email: string, password: string) => {
  const { data } = await gatewayApi.post("/login", { email, password });
  return data;
};

export const registerUser = async (
  email: string,
  password: string) => {
  const { data } = await gatewayApi.post("/register", {
    email,
    password,
  });
  return data;
}

export const refreshToken = async (refresh_token: string) => {
  const { data } = await gatewayApi.post(`auth/refresh/refresh-token?refresh_token=${refresh_token}`, {
  });
  return data;
}


export const userOnboarding = async (
  first_name: string,
  last_name: string,
  customer_name: string,
  user_id: string | null
) => {
  
    const { data } = await gatewayApi.patch(`/users/${user_id}/`, {
    first_name: first_name,
    last_name: last_name,
    new_customer_name: customer_name
  });
  return data;
}


/**
 * Fetch all budgets from the API Gateway 
 * based on the user's permissions.
 * If user is superuser, fetch all budgets.
 * @returns All budgets from the API Gateway
 */
export const fetchAllBudgets = async () => {
  const { data } = await gatewayApi.get(`/budgets/`);
  return data;
}
export default gatewayApi;