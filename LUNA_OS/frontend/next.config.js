/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',  // Necessário para Docker production

  // Desativa o redirect automático de trailing slash — evita 308 chegando ao browser
  trailingSlash: false,

  // 🔑 PROXY SOBERANO — Toda chamada /api/* vai para o backend
  // Em Docker: NEXT_PUBLIC_API_URL=http://luna-backend:8000
  // Em Dev Local: fallback para http://localhost:8000
  async rewrites() {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    return [
      {
        source: '/api/:path*/',
        destination: `${backendUrl}/api/:path*/`,
      },
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
