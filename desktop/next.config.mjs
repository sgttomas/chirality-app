/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Chirality serves local artifacts directly; the image optimizer is unused.
  images: { unoptimized: true },
  transpilePackages: ['@chirality/runtime-contracts']
};

export default nextConfig;
