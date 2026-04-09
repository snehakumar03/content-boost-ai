module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'purple-dark': '#1a0033',
        'navy-dark': '#0a0e27',
      },
      backdropBlur: {
        lg: '30px',
      },
      animation: {
        'glow-pulse': 'glow-pulse 3s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        'glow-pulse': {
          '0%, 100%': {
            boxShadow: '0 0 20px rgba(168, 85, 247, 0.5)',
          },
          '50%': {
            boxShadow: '0 0 40px rgba(168, 85, 247, 0.8)',
          },
        },
        'float': {
          '0%, 100%': {
            transform: 'translateY(0px)',
          },
          '50%': {
            transform: 'translateY(-20px)',
          },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-hero': 'radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.3) 0%, rgba(59, 130, 246, 0.2) 40%, transparent 70%)',
      },
    },
  },
  plugins: [],
}
