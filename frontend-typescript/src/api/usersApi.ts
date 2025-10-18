import { getUserIdFromToken } from "@/utils/token";
import { createAxiosInstance } from "./axiosConfig";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "@/context/AuthContext";

const usersApi = createAxiosInstance(
  import.meta.env.API_USER_SERVICE || "http://localhost:8000/api"
);

const gatewayApi = createAxiosInstance(
  import.meta.env.API_GATEWAY_SERVICE || "http://localhost:8080/api"
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
export default usersApi;


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
