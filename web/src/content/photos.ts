// Места под фотографии Алматы. Положите файл в web/public/photos/<file> — он встанет сам.
// Нужен настоящий город, не реклама: дворы, горы, советские здания, кофейни, рынки, вечерние улицы.
// На сайте фото показываются в ч/б с лёгким контрастом — цветные исходники подойдут.
export type PhotoSlot = { file: string; caption: string; hint: string; aspect: string };

export const photos = {
  hero: {
    file: "hero.jpg",
    caption: "Алматы, вечер",
    hint: "Вертикальный кадр: двор или улица на фоне гор, люди в кадре",
    aspect: "aspect-[4/5]",
  },
  places1: {
    file: "places-1.jpg",
    caption: "Двор в центре",
    hint: "Горизонтальный: советский двор, лавочки, деревья",
    aspect: "aspect-[16/10]",
  },
  places2: {
    file: "places-2.jpg",
    caption: "Маленькая кофейня",
    hint: "Квадрат: интерьер или вход небольшой кофейни",
    aspect: "aspect-square",
  },
  people: {
    file: "people.jpg",
    caption: "Компания на прогулке",
    hint: "Горизонтальный: 3–5 человек со спины или вполоборота",
    aspect: "aspect-[3/2]",
  },
} satisfies Record<string, PhotoSlot>;
