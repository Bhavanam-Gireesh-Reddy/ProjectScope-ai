import React from 'react';
import { BookOpen, Users, Calendar, Quote } from 'lucide-react';

export default function PaperCard({ paper }) {
  return (
    <a 
      href={paper.url} 
      target="_blank" 
      rel="noopener noreferrer"
      className="block group bg-slate-800/50 hover:bg-slate-800 border border-slate-700 rounded-xl p-5 transition-all hover:-translate-y-1 hover:shadow-xl flex flex-col h-full"
    >
      <div className="flex items-start gap-3 mb-3">
        <div className="bg-secondary/20 p-2 rounded-lg text-secondary">
          <BookOpen className="h-5 w-5" />
        </div>
        <h3 className="text-white font-semibold flex-1 leading-tight group-hover:text-secondary transition-colors">
          {paper.title}
        </h3>
      </div>
      
      <p className="text-slate-400 text-sm mb-4 flex-1 line-clamp-3 italic">
        {paper.abstract}
      </p>
      
      <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 pt-3 border-t border-slate-700">
        <div className="flex items-center gap-1">
          <Users className="h-3 w-3" />
          <span className="truncate max-w-[150px]">
            {paper.authors.join(', ')}
          </span>
        </div>
        <div className="flex items-center gap-1">
          <Calendar className="h-3 w-3" />
          <span>{paper.year}</span>
        </div>
        <div className="flex items-center gap-1 ml-auto">
          <Quote className="h-3 w-3" />
          <span>{paper.citations} citations</span>
        </div>
      </div>
    </a>
  );
}
