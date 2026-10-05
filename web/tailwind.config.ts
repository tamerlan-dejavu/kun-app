import type { Config } from "tailwindcss";
import { tokens } from "./src/styles/tokens";

// Токены дизайн-системы KUN переносятся без изменений (раздел 7 ТЗ).
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: tokens.colors,
      fontFamily: tokens.fontFamily,
      borderRadius: tokens.radius,
      boxShadow: tokens.shadow,
      maxWidth: { app: "480px" },
      // Области нажатия не меньше 44x44 (WCAG 2.1 AA)
      minHeight: { tap: "44px" },
      minWidth: { tap: "44px" },
      height: { tap: "44px" },
    },
  },
  plugins: [],
};

export default config;
