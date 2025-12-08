/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Note: API calls are handled directly by the frontend using NEXT_PUBLIC_API_URL
  // Rewrites are not needed since we're calling the backend URL directly
  // Exclude /api routes from Next.js handling - they're handled by Python serverless function
  async rewrites() {
    return [];
  },
};

module.exports = nextConfig;
