import { api } from "./axiosConfig";
import type { Template } from "../types";

export async function fetchTemplates(): Promise<Template[]> {
    // return mock when backend unavailable:
  return (await fetch("/mock-templates.json").then(r => r.json())) as Template[];
  const res = await api.get<Template[]>("/donor-mapping/templates");
  return res.data;
}
