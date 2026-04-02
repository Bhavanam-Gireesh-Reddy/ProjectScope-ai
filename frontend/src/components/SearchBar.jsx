import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

export default function SearchBar({ onSearch, isLoading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto group">
      <div className="relative flex flex-col sm:block">
        <div className="absolute left-0 top-[18px] sm:top-0 sm:inset-y-0 pl-4 flex items-center pointer-events-none z-20">
          <Search className="h-5 w-5 text-slate-400 group-focus-within:text-primary transition-colors" />
        </div>
        <input
          type="text"
          className="block w-full pl-12 pr-4 sm:pr-32 py-4 bg-slate-800 border border-slate-700 rounded-2xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all shadow-lg text-base"
          placeholder="Describe your project idea in natural language..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="w-full sm:w-auto mt-4 sm:mt-0 relative sm:absolute sm:right-2 sm:top-2 sm:bottom-2 px-8 py-4 sm:py-0 bg-primary hover:bg-blue-600 text-white font-bold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shadow-lg active:scale-95 z-30"
        >
          {isLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : 'Discover'}
        </button>
      </div>
    </form>
  );
}
