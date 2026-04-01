import React from 'react';
import { Database, Download, ExternalLink } from 'lucide-react';

export default function DatasetCard({ dataset }) {
  return (
    <a 
      href={dataset.url} 
      target="_blank" 
      rel="noopener noreferrer"
      className="block group bg-slate-800/40 hover:bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 transition-all hover:-translate-y-1 hover:shadow-xl"
    >
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-2 text-secondary font-semibold text-lg group-hover:underline line-clamp-1">
          <Database className="h-5 w-5" />
          {dataset.title}
        </div>
        <div className="flex items-center gap-1 text-slate-400 bg-slate-900/50 px-2.5 py-1 rounded-full text-xs font-medium border border-slate-700">
          <Download className="h-3 w-3" />
          {dataset.downloads?.toLocaleString() || 0}
        </div>
      </div>
      
      <p className="text-slate-400 text-sm mb-4 line-clamp-2 min-h-[40px]">
        {dataset.description || "No description provided for this dataset."}
      </p>
      
      <div className="flex items-center justify-between mt-auto pt-2 border-t border-slate-700/30">
        <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Kaggle Dataset</span>
        <ExternalLink className="h-3.5 w-3.5 text-slate-500 group-hover:text-primary transition-colors" />
      </div>
    </a>
  );
}
