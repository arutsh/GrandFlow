/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#0B1E3F",
          light: "#1C2B4A",
        },
        slate: {
          DEFAULT: oklch(0.279, 0.041, 260.031),
        },
        blue: {
          DEFAULT: oklch(0.929, 0.013, 255.508),
          light: oklch(0.929, 0.013, 255.508),
        },
        white: "#FFFFFF",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
