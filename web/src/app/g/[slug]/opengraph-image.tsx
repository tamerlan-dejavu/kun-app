import { ImageResponse } from "next/og";

export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

// Карточка-превью сбора для мессенджеров.
export default async function OgImage() {
  // TODO: категория, название, время, «идут N из M» в стиле KUN
  return new ImageResponse(<div style={{ background: "#FFB066", width: "100%", height: "100%" }} />, size);
}
