import type { components } from "./schema";

// Короткие имена для типов из OpenAPI (генерируются: npm run gen:api)
type S = components["schemas"];
export type Category = S["Category"];
export type GatheringCard = S["GatheringList"];
export type GatheringDetail = S["GatheringDetail"];
export type GatheringPublic = S["GatheringPublic"];
export type Participant = S["Participant"];
export type UserShort = S["UserShort"];
export type Message = S["Message"];
export type Me = S["Me"];
