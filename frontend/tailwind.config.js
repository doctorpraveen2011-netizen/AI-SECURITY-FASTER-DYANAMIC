/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0A0A0C",
        surface: "#14161D",
        "surface-card": "#181B24",
        "surface-hover": "#1F2330",
        border: "#252936",
        "border-subtle": "#1B1E28",
        brand: {
          orange: "#FF8A00",
          orangeGlow: "rgba(255, 138, 0, 0.35)",
          orangeLight: "#FFA333",
          orangeDark: "#D97500",
        },
        risk: {
          critical: "#EF4444",
          high: "#F97316",
          medium: "#F59E0B",
          low: "#10B981",
        }
      },
      boxShadow: {
        'glow-orange': '0 0 25px -5px rgba(255, 138, 0, 0.35)',
        'glow-orange-sm': '0 0 15px -3px rgba(255, 138, 0, 0.25)',
        'glow-green': '0 0 20px -5px rgba(16, 185, 129, 0.3)',
        'glow-red': '0 0 20px -5px rgba(239, 68, 68, 0.3)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace']
      }
    },
  },
  plugins: [],
}
