// src/pages/Onboarding.tsx
import React, { useState } from "react";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

export default function Onboarding() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [orgName, setOrgName] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // call API: saveUserProfile(form)
  };

  return (
    <div className="flex items-center justify-center h-screen bg-slate-100">
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
