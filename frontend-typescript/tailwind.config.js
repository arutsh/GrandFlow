/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#2563eb",
          light: "#3b82f6",
          dark: "#1d4ed8",
        },
        secondary: {
          DEFAULT: "#10b981",
          light: "#34d399",
          dark: "#059669",
        },
        accent: {
          DEFAULT: "#ef4444",
          light: "#f87171",
          dark: "#dc2626",
        },
        neutral: "#f8fafc",
        dark: "#0f172a",
        sidebar: {
          DEFAULT: "#0b1e3f",
          hover: "#3b82f6",
        },
        navy: {
          DEFAULT: "#0B1E3F",
          light: "#1C2B4A",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
