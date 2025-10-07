import axios, { AxiosInstance } from "axios";


// 👇 add this outside the component
export const getAuthToken = (): string | null => {
 
  return localStorage.getItem("token") || sessionStorage.getItem("token");
};

// Shared interceptor logic
function createAxiosInstance(baseURL: string): AxiosInstance {
  const instance = axios.create({ baseURL });

  // Request interceptor
  instance.interceptors.request.use((config) => {
    // const token = localStorage.getItem("access_token"); // or use context
    console.log("Getting auth token for request...");
    const token = getAuthToken();
    console.log("Auth token:", token);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log("Request config:", config);
    return config;
  });

  // Response interceptor
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        // Handle refresh logic or redirect to login
        console.warn("Unauthorized, redirecting...");
      }
      return Promise.reject(error);
    }
  );

  return instance;
}

export { createAxiosInstance };
