import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { FileText, TrendingUp, BarChart3, DollarSign } from "lucide-react";
import Button from "@/components/ui/Button";

export default function Dashboard() {
  const { username, logout, isRegistering } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Dashboard - isRegistering:", isRegistering);
    if (isRegistering) {
      navigate("/onboarding");
    }
  }, [isRegistering]);

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  // Mock stats data - replace with real data from API
  const stats = [
    {
      title: "Total Budgets",
      value: "12",
      icon: FileText,
      color: "text-slate-700",
      bgColor: "bg-slate-100",
    },
    {
      title: "On Track",
      value: "9",
      icon: TrendingUp,
      color: "text-green-600",
      bgColor: "bg-green-50",
    },
    {
      title: "Over Budget",
      value: "2",
      icon: BarChart3,
      color: "text-red-600",
      bgColor: "bg-red-50",
    },
    {
      title: "Total Allocated",
      value: "$125K",
      icon: DollarSign,
      color: "text-slate-700",
      bgColor: "bg-slate-100",
    },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
        {/* Welcome Section */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-2">
            <h1 className="text-4xl font-bold text-slate-900">
              Welcome back,{" "}
              <span className="text-slate-800 font-bold">{username}</span> 👋
            </h1>
            <Button
              onClick={handleLogout}
              variant="secondary"
              className="py-2 px-4"
            >
              Logout
            </Button>
          </div>
          <p className="text-gray-600">
            Here's what's happening with your budgets today.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {stats.map((stat, idx) => {
            const Icon = stat.icon;

            return (
              <div
                key={idx}
                className={`${stat.bgColor} rounded-lg card-shadow-hover p-6 transition-all`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium mb-1">
                      {stat.title}
                    </p>
                    <p className="text-3xl font-bold text-slate-900">
                      {stat.value}
                    </p>
                  </div>
                  <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                    <Icon size={24} className={stat.color} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Quick Actions */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-slate-900 mb-6">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Button
              onClick={() => navigate("/budgets")}
              className="py-3 px-6 text-base font-medium"
              variant="primary"
            >
              View All Budgets
            </Button>
            <Button
              onClick={() => navigate("/budgets")}
              className="py-3 px-6 text-base font-medium"
              variant="outline"
            >
              Create New Budget
            </Button>
          </div>
        </div>

        {/* Recent Activity Placeholder */}
        <div className="bg-white rounded-lg card-shadow p-6">
          <h2 className="text-xl font-bold text-slate-900 mb-4">
            Recent Activity
          </h2>
          <div className="text-center py-8">
            <p className="text-gray-500">No recent activity yet.</p>
            <p className="text-gray-400 text-sm mt-2">
              Start by creating your first budget!
            </p>
          </div>
        </div>
      </div>
  );
}
