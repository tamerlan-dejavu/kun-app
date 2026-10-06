// Токены KUN. Палитра: Storm Blue #537179 (основной) и Vanilla Dust #BFAE99 (второй).
// Шкалы построены от этих двух цветов. Контраст проверен (WCAG AA >= 4.5:1):
//   белый на brand (storm-500) — 5.24:1, ink на canvas — 12.5:1, sand-800 на sand-100 — 7.9:1.
// НЕЛЬЗЯ: vanilla-текст на storm-500 — 2.43:1. Vanilla-текст — только на brand-800 (4.88:1).
// TODO: сверить с дизайн-системой KUN в Figma.
export const tokens = {
  colors: {
    brand: {
      50: "#F1F4F4",
      100: "#E3E8EA",
      200: "#C5CFD1",
      300: "#9BADB1",
      400: "#758D94",
      DEFAULT: "#537179", // Storm Blue: кнопки, акценты; текст на нём — белый
      600: "#476269",
      700: "#3C5259",
      800: "#2F4248", // тёмные полосы: на нём белый или vanilla-текст
      900: "#223136",
    },
    sand: {
      50: "#F3F0ED",
      100: "#E7E0D8",
      200: "#D9CEC2",
      300: "#CBBDAB",
      DEFAULT: "#BFAE99", // Vanilla Dust: фоны, плашки, декор
      500: "#A69682",
      600: "#8E7E6A",
      700: "#6B5E4E",
      800: "#493F33",
    },
    ink: {
      DEFAULT: "#223136", // основной текст
      muted: "#56656A", // второстепенный текст
      subtle: "#8C9A9E", // только декоративное — не для текста
    },
    canvas: "#F8F6F3", // фон приложения
    surface: "#FFFFFF", // карточки
    line: "#E6DFD6", // границы и разделители
    danger: "#B42318",
    success: "#2F7D4F",
  },
  fontFamily: {
    heading: ["var(--font-unbounded)", "sans-serif"],
    sans: ["var(--font-manrope)", "sans-serif"],
  },
  radius: {
    card: "20px",
    button: "16px",
    chip: "999px",
  },
  shadow: {
    card: "0 1px 2px rgba(34, 49, 54, 0.04), 0 4px 16px rgba(34, 49, 54, 0.07)",
  },
};
