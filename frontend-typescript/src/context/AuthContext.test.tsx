import { render, screen, waitFor } from "@testing-library/react";
import { AuthProvider, useAuth } from "./AuthContext";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import App from "@/App";

function TestComponent() {
  const { isAuthenticated, login, logout, username, password } = useAuth();
  return (
    <div>
      <div>Auth: {isAuthenticated ? "Yes" : "No"}</div>
      <button onClick={() => login("fake-token", "john", true)}>
        LoginRemember
      </button>
      <button onClick={() => login("fake-token", "john", false)}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

describe("AuthProvider", () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
  });

  it("starts unauthenticated", () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );
    expect(screen.getByText("Auth: No")).toBeInTheDocument();
  });

  it("should login and persist token in localStorage when remember=true", async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    userEvent.click(screen.getByText("LoginRemember"));

    await waitFor(() => {
      expect(screen.getByText("Auth: Yes")).toBeInTheDocument();
    });

    expect(localStorage.getItem("token")).toBe("fake-token");
  });

  it("should login and persist token in sessionStorage when remember=false", async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    userEvent.click(screen.getByText("Login"));

    await waitFor(() => {
      expect(screen.getByText("Auth: Yes")).toBeInTheDocument();
    });

    expect(sessionStorage.getItem("token")).toBe("fake-token");
  });

  it("should logout and clear storage", async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    userEvent.click(screen.getByText("Login"));

    await waitFor(() => screen.getByText(/Auth: yes/i));

    userEvent.click(screen.getByText("Logout"));

    await waitFor(() => {
      expect(screen.getByText(/Auth: no/i)).toBeInTheDocument();
    });
    expect(localStorage.getItem("token")).toBeNull();
  });
});


