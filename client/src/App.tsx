import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import Analyzer from './pages/Analyzer';
import About from './pages/About';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app-wrapper">
        {/* Background Effects */}
        <div className="bg-effects">
          <div className="bg-gradient-1" />
          <div className="bg-gradient-2" />
          <div className="bg-gradient-3" />
          <div className="bg-grid" />
        </div>

        <Navbar />

        <main className="main-content-router">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/analyze" element={<Analyzer />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}

export default App;