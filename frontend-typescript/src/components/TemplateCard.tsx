import React from "react";
import { Template } from "../types";

export default function TemplateCard({ template }: { template: Template }) {
  return (
    <div className="border rounded p-4 shadow-sm">
      <h3 className="font-semibold">{template.name}</h3>
      <p className="text-sm text-gray-500">ID: {template.id}</p>
    </div>
  );
}
