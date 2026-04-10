/**
 * Dashboard page - Protected content generator.
 */
import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import { Zap, Copy, RotateCcw, Bot, LogOut, Menu, TrendingUp, ArrowLeft } from 'lucide-react';
import axios from 'axios';

export default function Dashboard() {
  const { user, isAuthenticated, logout, getRateLimitStatus } = useAuth();
  const navigate = useNavigate();

  const [platform, setPlatform] = useState('Social Media');
  const [contentType, setContentType] = useState('Caption');
  const [tone, setTone] = useState('Engaging');
  const [prompt, setPrompt] = useState('Write a caption for our new sneaker sale!');
  const [generatedContent, setGeneratedContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);
  const [rateLimit, setRateLimit] = useState(null);
  const responseEndRef = useRef(null);

  useEffect(() => {
    // Redirect if not authenticated (for full implementation)
    // For now, allow anonymous access with rate limiting
    fetchRateLimit();
  }, []);

  const fetchRateLimit = async () => {
    const status = await getRateLimitStatus();
    setRateLimit(status);
  };

  const scrollToBottom = () => {
    responseEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [generatedContent]);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setIsLoading(true);
    setGeneratedContent('');

    try {
      // Get token for authenticated requests
      const token = localStorage.getItem('access_token');
      const headers = {
        'Content-Type': 'application/json',
      };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await axios.post(
        'http://localhost:8000/generate',
        { prompt, tone, platform },
        { headers }
      );

      if (response.status !== 200) {
        throw new Error(`Error: ${response.statusText}`);
      }

      // Handle streaming response
      const reader = response.data.body?.getReader();
      if (reader) {
        const decoder = new TextDecoder();
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value);
          setGeneratedContent((prev) => prev + chunk);
        }
      } else {
        // Fallback for non-streaming
        setGeneratedContent(response.data);
      }

      // Update rate limit after generation
      await fetchRateLimit();
    } catch (error) {
      console.error('Generate error:', error);
      if (error.response?.status === 429) {
        setGeneratedContent(
          error.response.data.detail || 'Rate limit exceeded. Sign up for unlimited access!'
        );
      } else {
        setGeneratedContent(
          'Error generating content. Please check that your backend is running and your API key is set.'
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedContent).then(() => {
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    });
  };

  const handleRegenerate = () => {
    handleGenerate();
  };

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

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
              <Link to="/dashboard" className="text-white font-semibold">
                Dashboard
              </Link>
              {isAuthenticated ? (
                <>
                  <span className="text-white/70">
                    {user?.name || user?.email}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="glass-card px-4 py-2 text-white rounded-lg glass-card-hover flex items-center gap-2"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="text-white/70 hover:text-white transition">
                    Login
                  </Link>
                  <Link to="/register" className="btn-gradient px-6 py-2 text-sm">
                    Sign Up
                  </Link>
                </>
              )}
            </div>
            <Menu className="md:hidden w-6 h-6 text-white cursor-pointer" />
          </div>
        </motion.nav>

        {/* Rate Limit Banner (for unauthenticated users) */}
        {!isAuthenticated && rateLimit && (
          <motion.div
            className="fixed top-20 left-0 right-0 z-40 bg-yellow-500/20 backdrop-blur-lg border-b border-yellow-500/30 py-3 px-6"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="max-w-7xl mx-auto flex items-center justify-between">
              <div className="flex items-center gap-3 text-white">
                <TrendingUp className="w-5 h-5 text-yellow-400" />
                <span className="text-sm">
                  Free tier: <strong>{rateLimit.remaining}</strong> generations remaining today
                  ({rateLimit.current_count}/{rateLimit.daily_limit} used)
                </span>
              </div>
              <Link to="/register">
                <button className="btn-gradient px-4 py-2 text-sm rounded-lg">
                  Get Unlimited
                </button>
              </Link>
            </div>
          </motion.div>
        )}

        {/* Main Content Section */}
        <div className="pt-24 pb-16 px-6 max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-4xl font-bold text-white mb-2">
              {isAuthenticated ? `Welcome back, ${user?.name || 'User'}!` : 'Content Generator'}
            </h1>
            <p className="text-white/70 mb-8">
              {isAuthenticated
                ? 'Generate unlimited amazing content with AI'
                : 'Generate up to 5 contents per day for free'}
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Panel - Inputs */}
            <motion.div
              className="glass-card p-8"
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <h2 className="text-2xl font-bold text-white mb-6">Create Content</h2>

              {/* Platform Toggle */}
              <div className="mb-6">
                <label className="block text-white/80 font-semibold mb-3">Platform</label>
                <div className="flex gap-2 flex-wrap">
                  {['Social Media', 'Ecommerce', 'Ads'].map((p) => (
                    <motion.button
                      key={p}
                      className={`platform-pill ${platform === p ? 'active' : ''}`}
                      onClick={() => setPlatform(p)}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      {p}
                    </motion.button>
                  ))}
                </div>
              </div>

              {/* Content Type Dropdown */}
              <div className="mb-6">
                <label className="block text-white/80 font-semibold mb-3">Content Type</label>
                <select
                  value={contentType}
                  onChange={(e) => setContentType(e.target.value)}
                  className="glass-dropdown"
                >
                  <option>Caption</option>
                  <option>Description</option>
                  <option>Headline</option>
                  <option>Email</option>
                </select>
              </div>

              {/* Tone Dropdown */}
              <div className="mb-6">
                <label className="block text-white/80 font-semibold mb-3">Tone</label>
                <select
                  value={tone}
                  onChange={(e) => setTone(e.target.value)}
                  className="glass-dropdown"
                >
                  <option>Engaging</option>
                  <option>Professional</option>
                  <option>Funny</option>
                  <option>Inspirational</option>
                  <option>Casual</option>
                </select>
              </div>

              {/* Prompt Input */}
              <div className="mb-6">
                <label className="block text-white/80 font-semibold mb-3">Your Prompt</label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Write a caption for our new sneaker sale!"
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:border-purple-400 focus:bg-white/10 transition-all resize-none h-32"
                />
              </div>

              {/* Generate Button */}
              <motion.button
                className="btn-gradient w-full"
                onClick={handleGenerate}
                disabled={isLoading}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {isLoading ? 'Generating...' : 'Generate Content'}
              </motion.button>
            </motion.div>

            {/* Right Panel - AI Response */}
            <motion.div
              className="glass-card p-8 flex flex-col"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                  <Bot className="w-6 h-6" />
                  AI Response
                </h2>
                <div className="text-white/50 text-sm">...</div>
              </div>

              {/* Generated Content Display */}
              <div className="glass-card bg-white/5 p-6 rounded-lg mb-6 flex-grow overflow-y-auto max-h-80">
                <p className="text-white/90 leading-relaxed whitespace-pre-wrap">
                  {generatedContent || (
                    <span className="text-white/40">
                      Your AI-generated content will appear here...
                    </span>
                  )}
                </p>
                <div ref={responseEndRef} />
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4">
                <motion.button
                  className="glass-card px-6 py-3 text-white font-semibold rounded-lg glass-card-hover flex items-center gap-2 flex-1"
                  onClick={handleCopy}
                  disabled={!generatedContent}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Copy className="w-4 h-4" />
                  {copySuccess ? 'Copied!' : 'Copy'}
                </motion.button>
                <motion.button
                  className="glass-card px-6 py-3 text-white font-semibold rounded-lg glass-card-hover flex items-center gap-2 flex-1"
                  onClick={handleRegenerate}
                  disabled={!generatedContent || isLoading}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <RotateCcw className="w-4 h-4" />
                  Regenerate
                </motion.button>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
