import { createAxiosInstance } from "./axiosConfig";

const usersApi = createAxiosInstance(
  import.meta.env.API_USER_SERVICE || "http://localhost:8000/api"
);

// Example API calls
export const loginUser = async (email: string, password: string) => {
  const { data } = await usersApi.post("/auth/login", { email, password });
  return data;
};

export default usersApi;
