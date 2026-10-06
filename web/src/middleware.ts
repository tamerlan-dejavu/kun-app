import { NextResponse, type NextRequest } from "next/server";

// Закрытые страницы без сессии -> /login?next=...
const PROTECTED = ["/feed", "/map", "/new", "/my", "/profile", "/settings", "/onboarding", "/u/"];

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const isProtected =
    PROTECTED.some((p) => pathname.startsWith(p)) || /^\/g\/[^/]+\/(chat|after)/.test(pathname);
  if (isProtected && !req.cookies.has("sessionid")) {
    const url = req.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next|icons|fonts|sw.js|manifest.webmanifest).*)"],
};
