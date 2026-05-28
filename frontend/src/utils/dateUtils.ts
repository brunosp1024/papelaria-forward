// Globals utilities for date

/**
 * Convert a Date object to the datetime-local input format (YYYY-MM-DDTHH:mm)
 */
export function toInputValue(date: Date): string {
  const offset = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 16);
}

/**
 * Format an ISO string for friendly display in the pt-BR locale. Ex: "31/12/2023 23:59"
 */
export function toDisplayValue(iso: string): string {
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit", month: "2-digit", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  }).format(new Date(iso));
}
