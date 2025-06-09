export default {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#1E3A8A', // Deep blue for headers/buttons
        secondary: '#F59E0B', // Amber for alerts/highlights
        success: '#10B981', // Green for success states
        danger: '#EF4444', // Red for errors/warnings
        background: '#F9FAFB', // Light gray background
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Modern font for readability
      },
      spacing: {
        '128': '32rem', // For larger components
      },
      boxShadow: {
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)', // For cards
      },
    },
  },
  plugins: [],
};