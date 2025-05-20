import { NextResponse } from 'next/server'

// List all protected base routes
const protectedRoutes = ['/dashboard']

export default function middleware(req) {
  const path = req.nextUrl.pathname

  // Check if the path is a protected route or a subroute
  const isProtected = protectedRoutes.some((protectedPath) =>
    path === protectedPath || path.startsWith(`${protectedPath}/`)
  )

  if (isProtected) {
    return NextResponse.redirect(new URL('/login', req.nextUrl))
  }

  return NextResponse.next()
}

// Middleware config: run on all routes except static and API
export const config = {
  matcher: ['/dashboard/:path*'],
}
