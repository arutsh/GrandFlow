import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  // const form = { first_name, last_name, email, customer_name, password };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: call backend API to register user
    // console.log("Register form submitted:", form);
    navigate("/dashboard"); // redirect after success
  };

  return (
    <div className="flex items-center justify-center h-screen bg-slate-100">
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
