import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
// src/pages/Onboarding.tsx
import { useEffect, useState } from "react";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { useMutation } from "@tanstack/react-query";
import { userOnboarding } from "@/api/usersApi";
import { useAuth } from "@/context/AuthContext";
import { getUserIdFromToken } from "@/utils/token";
import { useNavigate } from "react-router-dom";
export default function Onboarding() {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [orgName, setOrgName] = useState("");
    const { isAuthenticated, token, login, isRegistering, setIsRegistering } = useAuth();
    const navigate = useNavigate();
    useEffect(() => {
        console.log("Onboarding - isAuthenticated:", isAuthenticated);
        if (!isRegistering) {
            navigate("/dashboard");
        }
    }, [isRegistering]);
    const mutation = useMutation({
        mutationFn: ({ first_name, last_name, customer_name, user_id, }) => userOnboarding(first_name, last_name, customer_name, user_id),
        onSuccess: (data) => {
            console.log("User onboarding successful", data);
            sessionStorage.removeItem("status");
            setIsRegistering(false);
            navigate("/dashboard");
        },
        onError: (error) => {
            console.error("User onboarding failed", error);
        },
    });
    const handleSubmit = (e) => {
        e.preventDefault();
        // call API: saveUserProfile(form)
        console.log({ firstName, lastName, orgName });
        let userId = getUserIdFromToken(token);
        if (!userId) {
            console.error("User ID not found in token");
            return;
        }
        mutation.mutate({
            first_name: firstName,
            last_name: lastName,
            customer_name: orgName,
            user_id: userId,
        });
    };
    return (_jsxs("div", { className: "flex items-center justify-center h-screen bg-slate-100", children: [_jsx("div", { children: mutation.isPending && _jsx("p", { children: "Loading..." }) }), _jsxs("form", { onSubmit: handleSubmit, className: "bg-white shadow-md rounded-lg p-8 w-full max-w-md space-y-4", children: [_jsx("h1", { className: "text-2xl font-bold text-center text-slate-800", children: "Tell us about you" }), _jsx(Input, { label: "First Name", name: "firstName", value: firstName, onChange: (e) => setFirstName(e.target.value), required: true }), _jsx(Input, { label: "Last Name", name: "lastName", value: lastName, onChange: (e) => setLastName(e.target.value), required: true }), _jsx(Input, { label: "Organization / NGO", name: "org", value: orgName, onChange: (e) => setOrgName(e.target.value), required: true }), _jsx(Button, { type: "submit", children: "Finish Setup" })] })] }));
}
