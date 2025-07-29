// tailwind.config.js
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',           // Scans the root templates folder
    './lea_app/templates/**/*.html', // Scans any templates inside your app
    './lea_app/**/*.py',             // Scans .py files for any dynamically added classes (good practice)
    './lea_app/static/js/**/*.js',     // Scans your app's JS files
  ],
  theme: {
    extend: {
      colors: {
        'msdp': '#4F46E5',
        'highway': '#10B981',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}