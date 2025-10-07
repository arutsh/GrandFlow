// src/pages/Onboarding.tsx
import React, { useEffect, useState } from "react";
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
  const { isAuthenticated, token, login, isRegistering, setIsRegistering } =
    useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Onboarding - isAuthenticated:", isAuthenticated);
    if (!isRegistering) {
      navigate("/dashboard");
    }
  }, [isRegistering]);
  const mutation = useMutation({
    mutationFn: ({
      first_name,
      last_name,
      customer_name,
      user_id,
    }: {
      first_name: string;
      last_name: string;
      customer_name: string;
      user_id: string | null;
    }) => userOnboarding(first_name, last_name, customer_name, user_id),
    onSuccess: (data) => {
      console.log("User onboarding successful", data);
      sessionStorage.removeItem("status");
      setIsRegistering(false);
      navigate("/dashboard");
    },
    onError: (error: any) => {
      console.error("User onboarding failed", error);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
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

  return (
    <div className="flex items-center justify-center h-screen bg-slate-100">
      <div>{mutation.isPending && <p>Loading...</p>}</div>
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-md rounded-lg p-8 w-full max-w-md space-y-4"
      >
        <h1 className="text-2xl font-bold text-center text-slate-800">
          Tell us about you
        </h1>
        <Input
          label="First Name"
          name="firstName"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          required
        />
        <Input
          label="Last Name"
          name="lastName"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          required
        />
        <Input
          label="Organization / NGO"
          name="org"
          value={orgName}
          onChange={(e) => setOrgName(e.target.value)}
          required
        />
        <Button type="submit">Finish Setup</Button>
      </form>
    </div>
  );
}
