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
      maxWidth: { app: "480px" },
      minHeight: { tap: "44px" },
      minWidth: { tap: "44px" },
    },
  },
  plugins: [],
};

export default config;
