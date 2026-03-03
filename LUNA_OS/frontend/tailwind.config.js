/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // LUNA OS — Soft Pink & Lavender Luxury Design System
        luna_pink: {
          50: '#fdf2f8', // Background
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4', // Secondary
          400: '#f472b6',
          500: '#ec4899', // Primary
          600: '#db2777', // hover / active
          700: '#be185d',
          800: '#9d174d',
          900: '#831843', // Text
          950: '#500724',
        },
        luna_violet: {
          // CTA 
          500: '#8b5cf6',
          600: '#7c3aed',
        },
        // Mantém aliases apontando para a escala base luna_pink/luna_violet
        bamboo: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ec4899',
          600: '#db2777',
          700: '#be185d',
          800: '#9d174d',
          900: '#831843',
          950: '#500724',
        },
        luna: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ec4899',
          600: '#db2777',
          700: '#be185d',
          900: '#831843',
        },
        primary: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ec4899',
          600: '#db2777',
          700: '#be185d',
          800: '#9d174d',
          900: '#831843',
          DEFAULT: '#ec4899',
        },
        cta: {
          DEFAULT: '#8b5cf6',
          hover: '#7c3aed',
        },
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        border: 'var(--border)',
        muted: {
          DEFAULT: 'var(--muted)',
          foreground: 'var(--muted-foreground)',
        }
      },
      boxShadow: {
        // Soft UI Evolution — sombras mais suaves, porém com contraste
        'card': '0 1px 3px rgba(131, 24, 67, 0.04), 0 1px 2px rgba(131, 24, 67, 0.02)',
        'card-md': '0 4px 12px rgba(131, 24, 67, 0.06), 0 2px 4px rgba(131, 24, 67, 0.03)',
        'card-lg': '0 8px 24px rgba(131, 24, 67, 0.08), 0 4px 8px rgba(131, 24, 67, 0.05)',
        'sidebar': '2px 0 16px rgba(131, 24, 67, 0.05)',
        'soft': '0 2px 8px rgba(131, 24, 67, 0.03), 0 1px 4px rgba(131, 24, 67, 0.02)',
      },
      fontFamily: {
        sans: ['Raleway', 'system-ui', 'sans-serif'],
        serif: ['Lora', 'Georgia', 'serif'],
      },
      backgroundImage: {
        'grad-premium': 'linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%)',
        'grad-soft': 'linear-gradient(135deg, #fdf2f8 0%, #ffffff 100%)',
        'grad-primary': 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
      },
      animation: {
        'float': 'float 3s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
      },
    },
  },
  plugins: [],
}
