import { stat } from "fs";
import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
} from "react";
import { useNavigate } from "react-router-dom";

export const STATUS = {
  PENDING: "pending",
  ACTIVE: "active",
};

interface AuthContextType {
  username: string | null;
  token: string | null;
  isAuthenticated: boolean;
  isRegistering: boolean;
  login: (
    token: string,
    username: string,
    remember: boolean,
    status: string
  ) => void;
  logout: () => void;
  loading?: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );
  const [username, setUsername] = useState<string | null>(
    localStorage.getItem("username")
  );
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check both storages

    const tokenFromStorage =
      localStorage.getItem("token") || sessionStorage.getItem("token");
    console.log(
      "AuthProvider useEffect token",
      tokenFromStorage,
      "isAuthenticated, ",
      isAuthenticated
    );
    setToken(tokenFromStorage);
    const usernameFromStorage =
      localStorage.getItem("username") || sessionStorage.getItem("username");
    setUsername(usernameFromStorage);
    const status = sessionStorage.getItem("status");
    setIsRegistering(status === STATUS.PENDING);
    setIsAuthenticated(!!tokenFromStorage);
    console.log("token is true, is authenticated set as true");

    setLoading(false); // ✅ auth check finished
  }, []);

  const login = (
    token: string,
    username: string,
    remember: boolean,
    status: string
  ) => {
    setToken(token);
    setUsername(username);

    if (remember) {
      localStorage.setItem("token", token);
      localStorage.setItem("username", username);
    } else {
      sessionStorage.setItem("token", token);
      sessionStorage.setItem("username", username);
      sessionStorage.setItem("status", status);
    }
    setIsAuthenticated(true);
    setIsRegistering(status === STATUS.PENDING);
  };

  const logout = () => {
    setToken(null);
    setUsername(null);
    localStorage.clear();
    sessionStorage.clear();
    setIsAuthenticated(false);
    setIsRegistering(false);
  };

  // 🔹 Don’t render children until we finish checking storage
  if (loading) {
    return <div>Loading...</div>;
  }
  return (
    <AuthContext.Provider
      value={{
        username,
        token,
        isAuthenticated: !!token,
        login,
        logout,
        isRegistering,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
};
