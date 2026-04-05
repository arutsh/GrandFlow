import React, { useState } from "react";
import { Menu, X, Home, FileText, BarChart3 } from "lucide-react"; // icons
import Button from "../../components/ui/Button";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="flex w-full h-screen bg-gray-50">
      {/* Sidebar */}
      <aside
        className={`
          fixed md:static top-0 left-0 h-full z-20
          bg-slate-900 text-white transition-all duration-300
          ${isOpen ? "w-64" : "w-16"}
        `}
      >
        <div className="flex items-center justify-between p-4">
          <span className={`font-bold text-lg ${!isOpen && "hidden md:block"}`}>
            GF
          </span>
          {/* toggle button for mobile/desktop */}
          <Button
            variant="icon"
            onClick={() => setIsOpen(!isOpen)}
            className="text-white md:hidden"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </Button>
        </div>

        <nav className="flex-1">
          <ul className="space-y-2">
            <li>
              <a
                href="/dashboard"
                className="flex items-center gap-3 px-4 py-2 hover:bg-blue-600/60 rounded transition-colors"
              >
                <Home size={20} />
                {isOpen && <span>Home</span>}
              </a>
            </li>
            <li>
              <a
                href="/budgets"
                className="flex items-center gap-3 px-4 py-2 hover:bg-blue-600/60 rounded transition-colors"
              >
                <FileText size={20} />
                {isOpen && <span>Budgets</span>}
              </a>
            </li>
            <li>
              <a
                href="/reports"
                className="flex items-center gap-3 px-4 py-2 hover:bg-blue-600/60 rounded transition-colors"
              >
                <BarChart3 size={20} />
                {isOpen && <span>Reports</span>}
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-10 md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-auto bg-gray-50">{children}</main>
    </div>
  );
}
