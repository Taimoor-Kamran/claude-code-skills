import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable React strict mode for better development experience
  reactStrictMode: true,

  // Image optimization settings
  images: {
    remotePatterns: [
      // Add allowed image domains here
      // { protocol: "https", hostname: "example.com" },
    ],
  },

  // Experimental features
  experimental: {
    // Enable typed routes
    typedRoutes: true,
  },
};

export default nextConfig;
