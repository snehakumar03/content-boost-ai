/**
 * Home/Landing page for ContentBoost AI.
 */
import React from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { Zap, Target, Bot, Menu, ArrowLeft } from 'lucide-react';

export default function Home() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-purple-dark via-navy-dark to-navy-dark overflow-hidden">
      {/* Animated Background Orbs */}
      <div className="glassmorphic-bg">
        <motion.div
          className="glow-orb glow-orb-purple"
          style={{ top: '10%', left: '-5%', width: '400px', height: '400px' }}
          animate={{ x: [0, 30, 0], y: [0, 50, 0] }}
          transition={{ duration: 8, repeat: Infinity }}
        />
        <motion.div
          className="glow-orb glow-orb-blue"
          style={{ bottom: '10%', right: '-5%', width: '500px', height: '500px' }}
          animate={{ x: [0, -30, 0], y: [0, -50, 0] }}
          transition={{ duration: 10, repeat: Infinity }}
        />
      </div>

      {/* Content Wrapper */}
      <div className="content-wrapper">
        {/* Navigation Bar */}
        <motion.nav
          className="glass-card-hover fixed top-0 left-0 right-0 glass-card mx-0 rounded-none border-b border-white/20 z-50"
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Back Button */}
              <button
                onClick={() => navigate(-1)}
                className="text-white/60 hover:text-white transition flex items-center gap-2"
                title="Go back"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <Link to="/" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-400 to-blue-400 rounded-lg flex items-center justify-center">
                  <Zap className="w-5 h-5 text-white" />
                </div>
                <span className="text-white font-bold text-xl">ContentBoost AI</span>
              </Link>
            </div>
            <div className="hidden md:flex items-center gap-6">
              <a href="#features" className="text-white/70 hover:text-white transition">
                Features
              </a>
              <a href="#pricing" className="text-white/70 hover:text-white transition">
                Pricing
              </a>
              <Link to="/login" className="text-white/70 hover:text-white transition">
                Login
              </Link>
              <Link to="/register" className="btn-gradient px-6 py-2 text-sm">
                Sign Up
              </Link>
            </div>
            <Menu className="md:hidden w-6 h-6 text-white cursor-pointer" />
          </div>
        </motion.nav>

        {/* Hero Section */}
        <motion.div
          className="pt-32 pb-16 px-6 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white via-purple-200 to-white">
            Generate High-Converting Content
          </h1>
          <p className="text-xl text-white/70 mb-4">for Social Media & Ecommerce 🚀</p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link to="/dashboard">
              <motion.button
                className="btn-gradient-lg"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Start Generating
              </motion.button>
            </Link>
            <motion.button
              className="glass-card px-8 py-4 text-white font-semibold rounded-lg glass-card-hover"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              ▶ Watch Demo
            </motion.button>
          </div>
        </motion.div>

        {/* Feature Grid */}
        <div id="features" className="max-w-7xl mx-auto px-6 pb-24">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <motion.div
              className="glass-card p-6 text-center"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              whileHover={{ scale: 1.05 }}
            >
              <Zap className="w-12 h-12 mx-auto mb-4 text-purple-400" />
              <h3 className="text-white font-bold mb-2">Lightning Fast</h3>
              <p className="text-white/60">Instantly get content</p>
            </motion.div>

            <motion.div
              className="glass-card p-6 text-center"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              whileHover={{ scale: 1.05 }}
            >
              <Target className="w-12 h-12 mx-auto mb-4 text-purple-400" />
              <h3 className="text-white font-bold mb-2">Targeted Content</h3>
              <p className="text-white/60">Tailored for your audience</p>
            </motion.div>

            <motion.div
              className="glass-card p-6 text-center"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              whileHover={{ scale: 1.05 }}
            >
              <Bot className="w-12 h-12 mx-auto mb-4 text-purple-400" />
              <h3 className="text-white font-bold mb-2">AI Powered</h3>
              <p className="text-white/60">Cutting-edge technology</p>
            </motion.div>
          </div>
        </div>

        {/* Pricing Section */}
        <div id="pricing" className="max-w-7xl mx-auto px-6 pb-24">
          <h2 className="text-3xl font-bold text-white text-center mb-12">Simple Pricing</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <motion.div
              className="glass-card p-8"
              whileHover={{ scale: 1.02 }}
            >
              <h3 className="text-2xl font-bold text-white mb-4">Free</h3>
              <p className="text-4xl font-bold text-white mb-6">$0<span className="text-lg text-white/60">/month</span></p>
              <ul className="text-white/80 space-y-3 mb-8">
                <li>✓ 5 generations per day</li>
                <li>✓ Basic content types</li>
                <li>✓ Community support</li>
              </ul>
              <Link to="/dashboard">
                <button className="glass-card w-full py-3 text-white font-semibold rounded-lg glass-card-hover">
                  Get Started
                </button>
              </Link>
            </motion.div>

            <motion.div
              className="glass-card p-8 border-2 border-purple-400"
              whileHover={{ scale: 1.02 }}
            >
              <h3 className="text-2xl font-bold text-white mb-4">Pro</h3>
              <p className="text-4xl font-bold text-white mb-6">$19<span className="text-lg text-white/60">/month</span></p>
              <ul className="text-white/80 space-y-3 mb-8">
                <li>✓ Unlimited generations</li>
                <li>✓ All content types</li>
                <li>✓ Priority support</li>
                <li>✓ Advanced AI features</li>
              </ul>
              <Link to="/register">
                <button className="btn-gradient w-full py-3 text-white font-semibold rounded-lg">
                  Upgrade Now
                </button>
              </Link>
            </motion.div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-white/50 pb-6 text-sm">
          © 2026 ContentBoost AI
        </div>
      </div>
    </div>
  );
}
