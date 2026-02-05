import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'pm-navy': '#2C3E50',
        'pm-dark': '#1e293b',
        'pm-blue': '#3b82f6',
        'pm-blue-light': '#60a5fa',
        'pm-blue-lighter': '#93c5fd',
      },
    },
  },
  plugins: [],
}
export default config
