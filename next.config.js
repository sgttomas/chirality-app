/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Enable standalone output for CI/CD deployments
  output: 'standalone',
  
  // Experimental features
  experimental: {
    optimizeCss: true,
    scrollRestoration: true
  },
  
  // Disable ESLint during builds to avoid hangs
  eslint: {
    ignoreDuringBuilds: true
  },
  
  // Production optimizations
  compress: true,
  poweredByHeader: false,
  
  // Bundle analysis
  env: {
    ANALYZE: process.env.ANALYZE || 'false'
  },
  
  // Security and PWA headers
  async headers() {
    return [
      {
        source: '/sw.js',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=0, must-revalidate'
          }
        ]
      },
      {
        source: '/manifest.json',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable'
          }
        ]
      },
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin'
          }
        ]
      }
    ]
  },
  
  // Image optimization
  images: {
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 60
  },
  
  // Compiler optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
      ? { exclude: ['error', 'warn'] }
      : false
  }
}

module.exports = nextConfig
