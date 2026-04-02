import React, { useState } from 'react';
import { Sparkles, History, Search } from 'lucide-react';
import SearchBar from './components/SearchBar';
import ResultTabs from './components/ResultTabs';
import HistoryList from './components/HistoryList';
import { searchProjectInfo } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('search'); // 'search' | 'history'

  const handleSearch = async (query) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await searchProjectInfo(query);
      setData(response);
    } catch (err) {
      setError('Failed to fetch project insights. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0f1c] text-slate-200 selection:bg-primary/30 font-sans">
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none mix-blend-overlay"></div>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-12 relative z-10 flex flex-col items-center">
        
        {/* Header Hero */}
        <div className={`transition-all duration-700 w-full flex flex-col items-center justify-center ${data || viewMode === 'history' ? 'mt-4 mb-10' : 'mt-12 md:mt-32 mb-12'}`}>
          <div className="flex flex-col sm:flex-row items-center gap-4 mb-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary border border-primary/20 text-sm font-medium">
              <Sparkles className="w-4 h-4" /> Graph-Augmented Discovery
            </div>
            
            <button 
              onClick={() => setViewMode(viewMode === 'search' ? 'history' : 'search')}
              className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700 hover:text-white transition-all shadow-sm text-sm font-medium w-full sm:w-auto justify-center"
            >
              {viewMode === 'search' ? (
                <><History className="w-4 h-4" /> View History</>
              ) : (
                <><Search className="w-4 h-4" /> Back to Search</>
              )}
            </button>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-center mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-primary leading-tight">
            ProjectScope AI
          </h1>
          <p className="text-base sm:text-lg text-slate-400 text-center max-w-2xl px-2">
            Describe your idea naturally. We cross-reference ArXiv, GitHub, and our Neo4j Graph to construct a unique implementation roadmap.
          </p>
        </div>

        {/* Main Content Area */}
        {viewMode === 'history' ? (
          <div className="w-full animate-in fade-in slide-in-from-bottom-8 duration-700">
            <HistoryList onSelectSearch={(record) => {
              setData(record);
              setViewMode('search');
            }} />
          </div>
        ) : (
          <>
            {/* Search Bar */}
            <div className="w-full mb-16">
              <SearchBar onSearch={handleSearch} isLoading={isLoading} />
              {error && (
                <div className="text-red-400 text-center mt-4 p-4 bg-red-400/10 rounded-xl border border-red-400/20 max-w-2xl mx-auto">
                  {error}
                </div>
              )}
            </div>

            {/* Results Area */}
            {data && (
              <div className="w-full animate-in fade-in slide-in-from-bottom-8 duration-700">
                <ResultTabs data={data} />
              </div>
            )}
          </>
        )}

      </main>
    </div>
  );
}

export default App;
