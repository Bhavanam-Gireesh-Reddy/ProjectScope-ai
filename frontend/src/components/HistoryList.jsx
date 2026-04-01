import React, { useEffect, useState } from 'react';
import { fetchSearchHistory } from '../services/api';
import { Clock, Loader2, ChevronRight, Activity } from 'lucide-react';

export default function HistoryList({ onSelectSearch }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      try {
        const data = await fetchSearchHistory();
        setHistory(data.history || []);
      } catch (err) {
        console.error("Failed to load history:", err);
      } finally {
        setLoading(false);
      }
    }
    loadHistory();
  }, []);

  if (loading) return (
    <div className="flex justify-center py-20">
      <Loader2 className="w-8 h-8 animate-spin text-primary opacity-50" />
    </div>
  );

  if (history.length === 0) return (
    <div className="text-center py-20 text-slate-500">
      No previous searches found in the database.
    </div>
  );

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
        <Clock className="w-6 h-6 text-indigo-400" /> Database Search History
      </h2>
      
      {history.map((record, idx) => (
        <div 
          key={record._id || idx} 
          onClick={() => onSelectSearch(record)}
          className="group flex flex-col md:flex-row md:items-center justify-between p-5 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:border-primary/50 cursor-pointer transition-all duration-300"
        >
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-white group-hover:text-primary transition-colors">
              "{record.query}"
            </h3>
            <div className="text-sm text-slate-400 mt-1 flex gap-4">
              <span className="flex items-center gap-1">
                <Activity className="w-4 h-4" /> {record.total_results || 0} Fetched Results
              </span>
              <span>•</span>
              <span>{new Date(record.timestamp).toLocaleString()}</span>
            </div>
            {record.insights && (
              <p className="text-sm text-slate-300 mt-3 line-clamp-2 italic border-l-2 border-primary/30 pl-3">
                {record.insights}
              </p>
            )}
          </div>
          <div className="mt-4 md:mt-0 md:ml-6 flex items-center gap-4 text-slate-400 group-hover:text-white transition-colors">
            <span className="text-sm font-medium border border-slate-700 rounded-full px-3 py-1 bg-slate-800">
              Confidence: {Math.round((record.confidence_score || 0) * 100)}%
            </span>
            <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </div>
        </div>
      ))}
    </div>
  );
}
