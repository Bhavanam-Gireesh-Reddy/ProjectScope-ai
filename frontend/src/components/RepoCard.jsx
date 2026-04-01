import React from 'react';
import { Star, ExternalLink, Github } from 'lucide-react';

export default function RepoCard({ repo }) {
  return (
    <a 
      href={repo.url} 
      target="_blank" 
      rel="noopener noreferrer"
      className="block group bg-slate-800/50 hover:bg-slate-800 border border-slate-700 rounded-xl p-5 transition-all hover:-translate-y-1 hover:shadow-xl"
    >
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-2 text-primary font-semibold text-lg group-hover:underline">
          <Github className="h-5 w-5" />
          {repo.name}
        </div>
        <div className="flex items-center gap-1 text-yellow-500 bg-yellow-500/10 px-2.5 py-1 rounded-full text-sm font-medium">
          <Star className="h-4 w-4 fill-current" />
          {repo.stars.toLocaleString()}
        </div>
      </div>
      <p className="text-slate-300 text-sm mb-4 line-clamp-2">
        {repo.description || "No description provided."}
      </p>
      {repo.technologies && repo.technologies.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {repo.technologies.map((tech, idx) => (
            <span key={idx} className="px-2 py-1 bg-slate-700 text-slate-300 text-xs rounded-md">
              {tech}
            </span>
          ))}
        </div>
      )}
    </a>
  );
}
