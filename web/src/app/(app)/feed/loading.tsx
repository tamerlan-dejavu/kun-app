import { Skeleton } from "@/components/ui/Skeleton";

export default function Loading() {
  return (
    <div className="space-y-3 p-4">
      <Skeleton />
      <Skeleton />
      <Skeleton />
    </div>
  );
}
