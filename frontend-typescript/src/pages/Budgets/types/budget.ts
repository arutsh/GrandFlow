export interface UserOut {
  id?: string;
  first_name?: string;
  last_name?: string;
  email?: string;
}

export interface CustomerOut {
  id?: string;
  name?: string;
  type?: string;
}

export interface TraceEvent {
  user?: UserOut;
  event_date?: string | null; // ISO date string
}

export interface TraceOut {
  created?: TraceEvent;
  updated?: TraceEvent;
}

export interface Budget {
  id: string;
  name?: string;
  owner?: CustomerOut;
  funder?: CustomerOut | { name?: string , id?: string};
  trace?: TraceOut;
}

// Define a separate type for editing (input data)
export interface BudgetUpdate {
  name?: string;
  owner_id?: string;
  funding_customer_id?: string;
  external_funder_name?: string;
}

export interface BudgetPatched {
  id:string, 
  name?: string;
  owner_id?: string;
  funding_customer_id?: string;
  external_funder_name?: string;
}

