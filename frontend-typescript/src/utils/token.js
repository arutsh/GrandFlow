import { jwtDecode } from "jwt-decode";
export function getUserIdFromToken(token) {
    if (!token)
        return null;
    try {
        const decoded = jwtDecode(token);
        return decoded.user_id || null;
    }
    catch (error) {
        console.error("Invalid token:", error);
        return null;
    }
}
