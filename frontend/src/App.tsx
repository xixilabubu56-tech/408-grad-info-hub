import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Institutions from './pages/Institutions'
import InstitutionDetail from './pages/InstitutionDetail'
import './App.css'

function App() {
  return (
    <Router>
      <div className="w-full min-h-screen bg-[#f5f5f7] dark:bg-black text-[#1d1d1f] dark:text-white flex flex-col items-center">
        <nav className="w-full h-14 bg-white/75 dark:bg-black/70 backdrop-blur-xl fixed top-0 flex justify-center items-center z-50 border-b border-gray-200/80 dark:border-gray-800">
          <div className="w-full max-w-6xl px-4 flex justify-between items-center text-sm font-medium">
            <Link to="/" className="font-bold tracking-tight text-base">408研招信息库</Link>
            <div className="flex gap-6 text-gray-500 dark:text-gray-300">
              <Link to="/institutions" className="hover:opacity-70 transition">院校大全</Link>
              <Link to="/institutions" className="hover:opacity-70 transition">招生简章</Link>
              <Link to="/institutions" className="hover:opacity-70 transition">历年数据</Link>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/institutions" element={<Institutions />} />
          <Route path="/institution/:id" element={<InstitutionDetail />} />
        </Routes>

        <footer className="w-full py-8 mt-20 border-t border-gray-200 dark:border-gray-800 flex justify-center">
          <p className="text-sm text-gray-500">© 2026 408研招信息库 · 聚合院校排名、学院官网、历年分数与官方通知</p>
        </footer>
      </div>
    </Router>
  )
}

export default App
