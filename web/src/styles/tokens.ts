// Токены KUN. Единственный фирменный цвет — абрикосовый #FFB066 (раздел 7 ТЗ).
// Контраст проверен (WCAG AA >= 4.5:1). Белый текст на brand — 1.8:1: на абрикосовом только тёмный текст.
// TODO: сверить с дизайн-системой KUN в Figma и перенести значения без изменений.
export const tokens = {
  colors: {
    brand: {
      50: "#FFF6EC",
      100: "#FFEBD6",
      200: "#FFD6AD",
      300: "#FFC285",
      DEFAULT: "#FFB066",
      500: "#F59A42",
      600: "#D97C24",
      700: "#A35A12", // акцентный текст на белом (5.2:1)
      800: "#7A4210",
    },
    ink: {
      DEFAULT: "#1F1A17", // основной текст (17.2:1 на белом)
      muted: "#6B625C", // второстепенный текст (5.95:1)
      subtle: "#9C928A", // только декоративное — не для текста
    },
    canvas: "#FFF9F3", // фон приложения
    surface: "#FFFFFF", // карточки
    line: "#EFE5DA", // границы и разделители
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
    card: "0 1px 2px rgba(31, 26, 23, 0.04), 0 4px 16px rgba(31, 26, 23, 0.06)",
  },
};
