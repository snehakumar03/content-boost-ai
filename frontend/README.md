# Frontend - ContentBoost AI

React-based UI for ContentBoost AI with glassmorphism design, real-time streaming, and smooth animations.

## 🎨 Features

- **Modern UI**: Glassmorphism design with dark theme
- **Responsive**: Works on desktop, tablet, and mobile
- **Animated**: Smooth transitions and glowing effects
- **Real-time Streaming**: Content appears letter-by-letter
- **Easy to Use**: Intuitive form with platform and tone selection

## 🚀 Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

Open http://localhost:5173 in your browser

### 3. Build for Production
```bash
npm run build
```

Output in `dist/` folder

## 📦 Dependencies

- **React**: UI library
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations
- **Lucide React**: Icons

## 🎯 File Structure

```
src/
├── App.jsx          # Main component (entire UI)
├── index.css        # Tailwind imports + custom styles
└── main.jsx         # React entry point

Configuration:
├── vite.config.js       # Vite settings
├── tailwind.config.js   # Tailwind theme customization
└── postcss.config.js    # PostCSS plugins
```

## 🔧 Customization

### Change Colors

Edit `tailwind.config.js`:
```javascript
colors: {
  'purple-dark': '#1a0033',  // Primary dark color
  'navy-dark': '#0a0e27',    // Secondary dark color
}
```

### Change Animations

Edit `src/index.css`:
```css
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);  /* Change distance */
  }
}
```

### Adjust API Endpoint

In `src/App.jsx`, line ~59:
```javascript
const response = await fetch('http://localhost:8000/generate', {
  // Change to your backend URL here
});
```

## 🌐 Environment Configuration

For production, update the backend URL in `App.jsx`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

## 📱 Mobile Responsive

The UI is fully responsive with:
- Mobile-first approach
- Breakpoints: `sm: 384px`, `md: 768px`, `lg: 1024px`
- Adaptive font sizes

## 🎬 Animations

Powered by Framer Motion:
- Initial page load animations
- Hover scale effects
- Button interactions
- Smooth transitions
- Floating orb animations

## ❌ Troubleshooting

**Nothing appears**: Check browser console (F12) for JavaScript errors

**Backend connection fails**: Verify backend is running at http://localhost:8000/health

**Styling looks wrong**: Run `npm install` to ensure Tailwind CSS is installed

**Slow performance**: Check if Vite dev server is running (`npm run dev`)

---

**Built with React 18 + Tailwind CSS + Framer Motion**
