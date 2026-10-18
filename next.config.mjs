/** @type {import('next').NextConfig} */
const isGhPages = process.env.GITHUB_PAGES === 'true' || process.env.NEXT_PUBLIC_BASE_PATH === '/WEBE';
const nextConfig = {
  output: 'export',
  distDir: 'out',
  images: { unoptimized: true },
  trailingSlash: true,
  basePath: isGhPages ? '/WEBE' : '',
  assetPrefix: isGhPages ? '/WEBE/' : undefined,
};

export default nextConfig;
