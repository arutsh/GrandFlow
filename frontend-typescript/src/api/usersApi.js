import { createAxiosInstance } from "./axiosConfig";
const usersApi = createAxiosInstance(import.meta.env.API_USER_SERVICE || "http://localhost:8000/api");
const gatewayApi = createAxiosInstance(import.meta.env.API_GATEWAY || "http://localhost:8082/api/v1");
// Example API calls
export const loginUser = async (email, password) => {
    const { data } = await gatewayApi.post("/auth/login", { email, password });
    return data;
};
export const registerUser = async (email, password) => {
    const { data } = await gatewayApi.post("/register", {
        email,
        password,
    });
    return data;
};
export default usersApi;
export const userOnboarding = async (first_name, last_name, customer_name, user_id) => {
    const { data } = await gatewayApi.patch(`/users/${user_id}/`, {
        first_name: first_name,
        last_name: last_name,
        new_customer_name: customer_name
    });
    return data;
};
