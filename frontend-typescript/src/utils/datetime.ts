import moment from "moment";


/**
 * Convert UTC datetime string to local datetime string
 * @param utcDate - UTC datetime string (ISO format)
 * @param format - Optional display format, e.g., "YYYY-MM-DD HH:mm"
 * @returns Local datetime string
 */
export function utcToLocal(utcDate: string | null | undefined, format: string = "YYYY-MM-DD HH:mm") {
  if (!utcDate) return "N/A";
  const m = moment.utc(utcDate);
  if (!m.isValid()) return "N/A";
  return m.local().format(format);
}
