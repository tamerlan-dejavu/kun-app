// Тексты информационных страниц. Лежат рядом с i18n: казахская версия — content/kk (этап 2).
export type Block = string | { list: string[] };

export type Section = { id: string; title: string; blocks: Block[] };

export type TextDoc = {
  title: string;
  lead?: string;
  /** Юридический текст ещё не согласован с юристом — показываем плашку. */
  draft?: boolean;
  updated?: string;
  sections: Section[];
};

export type FaqDoc = {
  title: string;
  lead?: string;
  groups: { title: string; items: { q: string; a: string }[] }[];
};
