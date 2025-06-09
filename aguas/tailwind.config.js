// tailwind.config.js (en la raíz junto a manage.py)
module.exports = {
  content: [
    './app/templates/**/*.html',      // tu app “app”
    './theme/templates/**/*.html',    // si usas la app theme de django-tailwind
    './**/templates/**/*.html',       // cualquier otra carpeta templates
    './static/js/**/*.js',            // si tienes JS que use clases Tailwind
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
