# Better Auth Common Patterns

Quick reference for common Better Auth patterns and best practices.

## Email/Password Authentication

### Server Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: /* your database */,
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
    requireEmailVerification: true,
  },
})
```

### Client Sign Up

```typescript
import { authClient } from "@/lib/auth-client"

const { data, error } = await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "John Doe",
  callbackURL: "/dashboard",
})
```

### Client Sign In

```typescript
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
  callbackURL: "/dashboard",
  rememberMe: true,
})
```

### Password Reset Flow

```typescript
// Server: Configure password reset
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    sendResetPassword: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Reset your password",
        body: `Click here to reset: ${url}`,
      })
    },
  },
})

// Client: Request reset
await authClient.forgetPassword({ email: "user@example.com" })

// Client: Complete reset
await authClient.resetPassword({
  newPassword: "newSecurePassword",
  token: tokenFromUrl,
})
```

### Email Verification

```typescript
// Server: Configure email verification
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Verify your email",
        body: `Click to verify: ${url}`,
      })
    },
  },
})

// Client: Resend verification
await authClient.sendVerificationEmail({ email: "user@example.com" })
```

## Social Providers

### Configuration

```typescript
// lib/auth.ts
export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    apple: {
      clientId: process.env.APPLE_CLIENT_ID!,
      clientSecret: process.env.APPLE_CLIENT_SECRET!,
    },
    discord: {
      clientId: process.env.DISCORD_CLIENT_ID!,
      clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    },
  },
})
```

### Client Social Sign In

```typescript
await authClient.signIn.social({
  provider: "github",
  callbackURL: "/dashboard",
  errorCallbackURL: "/login?error=true",
  newUserCallbackURL: "/welcome",
})
```

### Link Social Account

```typescript
await authClient.linkSocial({ provider: "google" })
```

## Session Management

### Get Session (Client)

```typescript
// React hook
const { data: session, isPending } = authClient.useSession()

// One-time fetch
const { data: session } = await authClient.getSession()
```

### Get Session (Server)

```typescript
import { auth } from "@/lib/auth"
import { headers } from "next/headers"

const session = await auth.api.getSession({
  headers: await headers(),
})
```

### Session Configuration

```typescript
export const auth = betterAuth({
  session: {
    expiresIn: 60 * 60 * 24 * 7,   // 7 days
    updateAge: 60 * 60 * 24,       // Update every 24 hours
    freshAge: 60 * 60 * 24,        // Fresh for 24 hours
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60,              // 5 minutes
    },
  },
})
```

### Sign Out

```typescript
await authClient.signOut()

// Revoke all sessions
await authClient.revokeOtherSessions()
```

### List Active Sessions

```typescript
const { data: sessions } = await authClient.listSessions()

// Revoke specific session
await authClient.revokeSession({ sessionId: "session-id" })
```

## Two-Factor Authentication

### Server Setup

```typescript
import { betterAuth } from "better-auth"
import { twoFactor } from "better-auth/plugins"

export const auth = betterAuth({
  plugins: [
    twoFactor({
      issuer: "MyApp",
      otpOptions: {
        sendOTP: async ({ user, otp }) => {
          await sendSMS(user.phone, `Your code: ${otp}`)
        },
      },
    }),
  ],
})
```

### Client Setup

```typescript
import { createAuthClient } from "better-auth/react"
import { twoFactorClient } from "better-auth/client/plugins"

export const authClient = createAuthClient({
  plugins: [twoFactorClient()],
})
```

### Enable TOTP

```typescript
// Get TOTP URI for QR code
const { data } = await authClient.twoFactor.getTotpUri()
// Display QR code with data.totpURI

// Verify and enable
await authClient.twoFactor.enable({
  password: "currentPassword",
})
```

### Verify TOTP on Sign In

```typescript
const { data, error } = await authClient.twoFactor.verifyTotp({
  code: "123456",
  trustDevice: true,
})
```

### Backup Codes

```typescript
// Generate backup codes
const { data } = await authClient.twoFactor.generateBackupCodes()

// Use backup code
await authClient.twoFactor.verifyBackupCode({ code: "backup-code" })
```

## Database Adapters

### PostgreSQL

```typescript
import { Pool } from "pg"

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
})
```

### SQLite

```typescript
import Database from "better-sqlite3"

export const auth = betterAuth({
  database: new Database("./sqlite.db"),
})
```

### MySQL

```typescript
import mysql from "mysql2/promise"

export const auth = betterAuth({
  database: await mysql.createConnection({
    uri: process.env.DATABASE_URL,
  }),
})
```

### Drizzle ORM

```typescript
import { drizzleAdapter } from "better-auth/adapters/drizzle"
import { db } from "@/db"

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
  }),
})
```

### Prisma

```typescript
import { prismaAdapter } from "better-auth/adapters/prisma"
import { prisma } from "@/db"

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
})
```

## Framework Integrations

### Next.js (App Router)

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth"
import { toNextJsHandler } from "better-auth/next-js"

export const { GET, POST } = toNextJsHandler(auth.handler)
```

### Next.js Middleware

```typescript
// middleware.ts
import { NextRequest, NextResponse } from "next/server"
import { auth } from "@/lib/auth"

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  })

  if (!session) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*"],
}
```

### Express

```typescript
import express from "express"
import { toNodeHandler } from "better-auth/node"
import { auth } from "./auth"

const app = express()
app.all("/api/auth/*", toNodeHandler(auth))
```

### Hono

```typescript
import { Hono } from "hono"
import { auth } from "./auth"

const app = new Hono()
app.on(["GET", "POST"], "/api/auth/*", (c) => auth.handler(c.req.raw))
```

## Client Setup

### Create Auth Client

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient()
export const { signIn, signUp, signOut, useSession } = authClient
```

### With Base URL

```typescript
export const authClient = createAuthClient({
  baseURL: "http://localhost:3000",
})
```

## Server Configuration

### Basic Setup

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"
import Database from "better-sqlite3"

export const auth = betterAuth({
  database: new Database("./sqlite.db"),
  emailAndPassword: {
    enabled: true,
  },
})
```

### Full Configuration

```typescript
export const auth = betterAuth({
  database: /* your database */,
  baseURL: process.env.BETTER_AUTH_URL,
  secret: process.env.BETTER_AUTH_SECRET,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
  },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7,
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60,
    },
  },
})
```

## Environment Variables

```bash
BETTER_AUTH_SECRET="<32+ character random string>"
BETTER_AUTH_URL="http://localhost:3000"
DATABASE_URL="<your database connection string>"

# Social providers (if used)
GITHUB_CLIENT_ID=""
GITHUB_CLIENT_SECRET=""
GOOGLE_CLIENT_ID=""
GOOGLE_CLIENT_SECRET=""
```

Generate secret:
```bash
openssl rand -base64 32
```

## CLI Commands

```bash
# Generate database schema/migrations
npx @better-auth/cli generate

# Apply migrations directly
npx @better-auth/cli migrate

# Set up MCP for Claude Code
npx @better-auth/cli mcp --claude-code
```

## Best Practices

1. **Always use HTTPS** in production for secure cookie transmission
2. **Set strong secrets** - use `openssl rand -base64 32` for generation
3. **Enable email verification** for email/password auth
4. **Use cookie caching** to reduce database queries
5. **Implement 2FA** for sensitive applications
6. **Protect routes** with middleware for authenticated sections
7. **Handle errors** consistently across auth flows
8. **Use TypeScript** for type-safe auth configuration
