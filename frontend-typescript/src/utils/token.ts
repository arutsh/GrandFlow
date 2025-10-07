import {jwtDecode} from "jwt-decode";

export interface JwtPayload {
  user_id: string; // standard field for user ID
  exp?: number;
  iat?: number;
  [key: string]: any; // allow extra fields
}

export function getUserIdFromToken(token: string | null): string | null {
  if (!token) return null;

  try {
    const decoded = jwtDecode<JwtPayload>(token);
    return decoded.user_id || null;
  } catch (error) {
    console.error("Invalid token:", error);
    return null;
  }
}
