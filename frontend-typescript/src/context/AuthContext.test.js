import { jsxs as _jsxs, jsx as _jsx } from "react/jsx-runtime";
import { render, screen, waitFor } from "@testing-library/react";
import { AuthProvider, useAuth } from "./AuthContext";
import userEvent from "@testing-library/user-event";
function TestComponent() {
    const { isAuthenticated, login, logout, username } = useAuth();
    return (_jsxs("div", { children: [_jsxs("div", { children: ["Auth: ", isAuthenticated ? "Yes" : "No"] }), _jsx("button", { onClick: () => login("fake-token", "john", true, "active", "refresh-token"), children: "LoginRemember" }), _jsx("button", { onClick: () => login("fake-token", "john", false, "active", "refresh-token"), children: "Login" }), _jsx("button", { onClick: logout, children: "Logout" })] }));
}
describe("AuthProvider", () => {
    beforeEach(() => {
        localStorage.clear();
        sessionStorage.clear();
    });
    it("starts unauthenticated", () => {
        render(_jsx(AuthProvider, { children: _jsx(TestComponent, {}) }));
        expect(screen.getByText("Auth: No")).toBeInTheDocument();
    });
    it("should login and persist token in localStorage when remember=true", async () => {
        render(_jsx(AuthProvider, { children: _jsx(TestComponent, {}) }));
        userEvent.click(screen.getByText("LoginRemember"));
        await waitFor(() => {
            expect(screen.getByText("Auth: Yes")).toBeInTheDocument();
        });
        expect(localStorage.getItem("token")).toBe("fake-token");
    });
    it("should login and persist token in sessionStorage when remember=false", async () => {
        render(_jsx(AuthProvider, { children: _jsx(TestComponent, {}) }));
        userEvent.click(screen.getByText("Login"));
        await waitFor(() => {
            expect(screen.getByText("Auth: Yes")).toBeInTheDocument();
        });
        expect(sessionStorage.getItem("token")).toBe("fake-token");
    });
    it("should logout and clear storage", async () => {
        render(_jsx(AuthProvider, { children: _jsx(TestComponent, {}) }));
        userEvent.click(screen.getByText("Login"));
        await waitFor(() => screen.getByText(/Auth: yes/i));
        userEvent.click(screen.getByText("Logout"));
        await waitFor(() => {
            expect(screen.getByText(/Auth: no/i)).toBeInTheDocument();
        });
        expect(localStorage.getItem("token")).toBeNull();
    });
});
