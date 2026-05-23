import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        parchment: "#faf8f3",
        cream: "#f4efe4",
        ink: {
          50: "#e8e2d4",
          100: "#c4b8a0",
          200: "#9c8d72",
          300: "#6f6553",
          400: "#3a3528",
          500: "#1a1a1a",
          900: "#0a0e1a",
        },
        burgundy: {
          DEFAULT: "#7a1f1f",
          dark: "#5e1414",
        },
        umber: "#3a2a18",
      },
      fontFamily: {
        serif: ['"Iowan Old Style"', "Georgia", "ui-serif", "serif"],
        sans: ["ui-sans-serif", "system-ui", "-apple-system", "sans-serif"],
        mono: ['"SF Mono"', "Menlo", "Monaco", "ui-monospace", "monospace"],
      },
      letterSpacing: {
        widest: "0.18em",
      },
    },
  },
  plugins: [],
};

export default config;
