export interface Template {
  id: number;
  name: string;
  // optional: template may include fields for your real API
  fields?: Record<string, unknown> | Array<Record<string, unknown>>;
}
