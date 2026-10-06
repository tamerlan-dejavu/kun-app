import Link from "next/link";

// Схема Алматы: не навигационная карта, а графика бренда — магистрали чёрными линиями,
// горы штриховкой, сборы терракотовыми точками. Линии проспектов приблизительные.
export type MapPoint = { slug: string; title: string; emoji?: string; lat: number; lng: number };

const BOUNDS = { west: 76.8, east: 77.06, south: 43.15, north: 43.33 };
const W = 1000;
// Высота с поправкой на широту (градус долготы на 43° короче градуса широты)
const H = Math.round(
  (W * (BOUNDS.north - BOUNDS.south)) / ((BOUNDS.east - BOUNDS.west) * Math.cos((43.24 * Math.PI) / 180)),
);

const x = (lng: number) => ((lng - BOUNDS.west) / (BOUNDS.east - BOUNDS.west)) * W;
const y = (lat: number) => ((BOUNDS.north - lat) / (BOUNDS.north - BOUNDS.south)) * H;
const path = (pts: [number, number][]) => pts.map(([lng, lat], i) => `${i ? "L" : "M"}${x(lng)},${y(lat)}`).join(" ");

const STREETS: { name: string; pts: [number, number][]; label: [number, number]; vertical?: boolean }[] = [
  { name: "РАЙЫМБЕКА", pts: [[76.81, 43.268], [76.98, 43.272]], label: [76.83, 43.272] },
  { name: "ТОЛЕ БИ", pts: [[76.81, 43.251], [76.955, 43.256]], label: [76.83, 43.255] },
  { name: "АБАЯ", pts: [[76.81, 43.236], [76.96, 43.242]], label: [76.83, 43.24] },
  { name: "АЛЬ-ФАРАБИ", pts: [[76.81, 43.203], [76.87, 43.207], [76.928, 43.218], [76.957, 43.233], [77.0, 43.234]], label: [76.83, 43.208] },
  { name: "САИНА", pts: [[76.845, 43.195], [76.842, 43.3]], label: [76.846, 43.293], vertical: true },
  { name: "РОЗЫБАКИЕВА", pts: [[76.889, 43.19], [76.889, 43.29]], label: [76.892, 43.29], vertical: true },
  { name: "СЕЙФУЛЛИНА", pts: [[76.937, 43.212], [76.934, 43.3]], label: [76.937, 43.3], vertical: true },
  { name: "ДОСТЫК", pts: [[76.957, 43.29], [76.957, 43.233], [76.966, 43.214], [76.99, 43.192], [77.058, 43.158]], label: [76.96, 43.29], vertical: true },
];

const MOUNTAINS: [number, number][] = [
  [76.8, 43.15], [76.8, 43.186], [76.86, 43.191], [76.92, 43.198], [76.97, 43.204], [77.02, 43.196], [77.06, 43.2], [77.06, 43.15],
];

const CENTER = { lat: 43.2389, lng: 76.8897 };

export function CityMap({ points, label }: { points: MapPoint[]; label: string }) {
  // Точки в одной клетке (огрублённые координаты) слегка разводим, чтобы не слипались
  const seen = new Map<string, number>();
  const placed = points.map((p) => {
    const key = `${p.lat},${p.lng}`;
    const n = seen.get(key) ?? 0;
    seen.set(key, n + 1);
    return { ...p, cx: x(p.lng) + n * 16, cy: y(p.lat) - n * 10 };
  });

  return (
    <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={label} className="h-auto w-full bg-surface">
      <defs>
        <pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="10" stroke="#111" strokeWidth="1.2" />
        </pattern>
        <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
          <path d="M50 0H0V50" fill="none" stroke="#111" strokeOpacity="0.08" />
        </pattern>
      </defs>
      <rect width={W} height={H} fill="url(#grid)" />
      <path d={`${path(MOUNTAINS)} Z`} fill="url(#hatch)" stroke="#111" strokeWidth="2" />
      <text x={x(76.83)} y={y(43.165)} className="fill-ink font-mono" fontSize="18" fontWeight="700" stroke="#FBFAF6" strokeWidth="6" paintOrder="stroke">
        ИЛЕ-АЛАТАУ ↓
      </text>

      {/* Сначала все линии, потом все подписи — иначе поздние линии перечёркивают ранние подписи */}
      {STREETS.map((s) => (
        <path key={s.name} d={path(s.pts)} fill="none" stroke="#111" strokeWidth="3" strokeLinejoin="round" />
      ))}
      {STREETS.map((s) => {
        const lx = x(s.label[0]);
        const ly = y(s.label[1]) - 8;
        return (
          <text
            key={s.name}
            x={lx}
            y={ly}
            fontSize="14"
            fontWeight="700"
            // Подложка цвета бумаги поверх линий
            stroke="#FBFAF6"
            strokeWidth="6"
            paintOrder="stroke"
            className="fill-ink font-mono"
            transform={s.vertical ? `rotate(-90 ${lx} ${ly})` : undefined}
          >
            {s.name}
          </text>
        );
      })}

      {/* Перекрестье центра — координаты из шапки сайта */}
      <g stroke="#3155FF" strokeWidth="2">
        <line x1={x(CENTER.lng) - 14} y1={y(CENTER.lat)} x2={x(CENTER.lng) + 14} y2={y(CENTER.lat)} />
        <line x1={x(CENTER.lng)} y1={y(CENTER.lat) - 14} x2={x(CENTER.lng)} y2={y(CENTER.lat) + 14} />
      </g>

      {placed.map((p) => (
        <Link key={p.slug} href={`/g/${p.slug}`} aria-label={p.title}>
          <title>{p.title}</title>
          <g className="transition-transform duration-100 hover:-translate-y-1">
            <rect x={p.cx - 11} y={p.cy - 11} width="22" height="22" fill="#111" transform="translate(4 4)" />
            <rect x={p.cx - 11} y={p.cy - 11} width="22" height="22" fill="#E84A2A" stroke="#111" strokeWidth="2.5" />
          </g>
        </Link>
      ))}
    </svg>
  );
}
