import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { registerUser } from "@/api/usersApi";
import { useAuth } from "@/context/AuthContext";

export default function Register() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, login } = useAuth();
  const queryClient = useQueryClient();
  // const form = { first_name, last_name, email, customer_name, password };

  const mutation = useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      registerUser(email, password),
    onSuccess: (data) => {
      login(data.access_token, email, false, data.status);
      console.log("Registration successful");
      navigate("/onboarding");
    },
    onError: (error: any) => {
      console.error("Registration failed", error);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate({ email, password });
  };
  if (mutation.isPending) {
    return <div>Loading...</div>;
  }
  return (
    <div className="flex items-center justify-center h-screen bg-slate-100">
      {error && <p className="text-red-500">{error}</p>}
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-md rounded-lg p-8 w-full max-w-sm space-y-4"
      >
        <h1 className="text-2xl font-bold text-center text-slate-800">
          Create Account
        </h1>
        <Input
          label="Email"
          type="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          label="Password"
          type="password"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Button type="submit">Continue</Button>
      </form>
    </div>
  );
}
