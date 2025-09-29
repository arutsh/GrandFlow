import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "./DashboardLayout";

export default function Dashboard() {
  const { username, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
        <h1 className="text-2xl font-bold">Welcome, {username} 👋</h1>
        <button
          onClick={handleLogout}
          className="mt-6 px-4 py-2 bg-slate-600 text-white rounded hover:bg-slate-700"
        >
          Logout
        </button>
      </div>
    </DashboardLayout>
  );
}
