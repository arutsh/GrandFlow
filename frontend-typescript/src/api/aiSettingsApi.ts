import gatewayApi from "@/api/gatewayApi";

export interface ProviderStatus {
  name: string;
  display_name: string;
  requires_key: boolean;
  has_key: boolean;
  model: string | null;
  base_url: string | null;
}

export interface AiSettings {
  providers: ProviderStatus[];
}

export const getAiSettings = async (): Promise<AiSettings> => {
  const { data } = await gatewayApi.get("/users/me/ai-settings");
  return data;
};

export const saveAiKey = async (
  provider: string,
  key: string | null,
  model: string,
  base_url?: string | null,
): Promise<AiSettings> => {
  const { data } = await gatewayApi.put("/users/me/ai-settings", {
    provider,
    key,
    model,
    base_url: base_url ?? null,
  });
  return data;
};

export const clearAiKey = async (provider: string): Promise<AiSettings> => {
  const { data } = await gatewayApi.delete(`/users/me/ai-settings/${provider}/key`);
  return data;
};
