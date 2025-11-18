import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/categorias/:path*',
        destination: 'http://backend:3000/categorias/:path*',
      },
      {
        source: '/api/productos/:path*',
        destination: 'http://backend:3000/productos/:path*',
      },
      {
        source: '/api/reservas/:path*',
        destination: 'http://backend:3000/reservas/:path*',
      },
    ]
  },
};

export default nextConfig;