/** @type {import('next').NextConfig} */
const nextConfig = { output: "export", trailingSlash: true, images: { unoptimized: true }, ...(process.env.NEXT_PUBLIC_BASE_PATH ? { basePath: process.env.NEXT_PUBLIC_BASE_PATH } : {}) };
export default nextConfig;
