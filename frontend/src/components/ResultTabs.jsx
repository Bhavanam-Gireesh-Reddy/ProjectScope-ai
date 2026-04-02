import React, { useState } from 'react';
import { Code, BookText, Lightbulb, Map } from 'lucide-react';
import RepoCard from './RepoCard';
import PaperCard from './PaperCard';
import DatasetCard from './DatasetCard';
import { Database } from 'lucide-react';

export default function ResultTabs({ data }) {
  const [activeTab, setActiveTab] = useState('repos');

  const tabs = [
    { id: 'repos', label: 'Repositories', icon: Code, count: data.repositories.length },
    { id: 'papers', label: 'Research Papers', icon: BookText, count: data.papers.length },
    { id: 'datasets', label: 'Datasets', icon: Database, count: data.datasets?.length || 0 },
    { id: 'insights', label: 'Insights', icon: Lightbulb },
    { id: 'roadmap', label: 'Roadmap', icon: Map }
  ];

  return (
    <div className="w-full">
      <div className="flex overflow-x-auto border-b border-slate-700 mb-6 pb-px">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
              activeTab === tab.id 
                ? 'border-primary text-primary' 
                : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-600'
            }`}
          >
            <tab.icon className="h-4 w-4" />
            {tab.label}
            {tab.count !== undefined && (
              <span className={`ml-2 px-2 py-0.5 rounded-full text-xs ${
                activeTab === tab.id ? 'bg-primary/10' : 'bg-slate-800'
              }`}>
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </div>

      <div className="mt-6">
        {activeTab === 'repos' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
            {data.repositories.map(repo => <RepoCard key={repo.id} repo={repo} />)}
            {data.repositories.length === 0 && (
              <p className="text-slate-400 col-span-full text-center py-10">No repositories found.</p>
            )}
          </div>
        )}

        {activeTab === 'papers' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
            {data.papers.map(paper => <PaperCard key={paper.id} paper={paper} />)}
            {data.papers.length === 0 && (
              <p className="text-slate-400 col-span-full text-center py-10">No research papers found.</p>
            )}
          </div>
        )}

        {activeTab === 'datasets' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
            {(data.datasets || []).map(dataset => <DatasetCard key={dataset.id} dataset={dataset} />)}
            {(!data.datasets || data.datasets.length === 0) && (
              <p className="text-slate-400 col-span-full text-center py-10">No datasets found.</p>
            )}
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-2xl p-8">
            <h3 className="text-xl font-semibold mb-6 flex items-center gap-3 text-secondary">
              <Lightbulb className="h-6 w-6" />
              AI Architect Insights
            </h3>
            <div className="prose prose-invert prose-lg max-w-none text-slate-300">
              <p className="leading-relaxed">{data.insights}</p>
            </div>
            
            <div className="mt-8 pt-6 border-t border-slate-700">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 font-medium">Feasibility Confidence</span>
                <span className="text-primary font-bold text-xl">{Math.round(data.confidence_score * 100)}%</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-3 mt-3 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-secondary to-primary h-3 rounded-full transition-all duration-1000" 
                  style={{ width: `${data.confidence_score * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'roadmap' && (
          <div className="bg-slate-800/50 border border-slate-700 rounded-2xl p-4 sm:p-8">
            <h3 className="text-xl font-semibold mb-8 flex items-center gap-3 text-primary">
              <Map className="h-6 w-6" />
              Suggested Execution Roadmap
            </h3>
            
            {/* Roadmap Timeline / List */}
            <div className="relative space-y-8 before:absolute before:inset-0 before:ml-4 sm:before:ml-6 md:before:mx-auto before:-translate-x-px before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-700 before:to-transparent">
              {data.roadmap.map((step, idx) => (
                <div key={idx} className="relative flex items-start md:items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                  {/* Step Number Dot */}
                  <div className="flex items-center justify-center w-8 h-8 sm:w-10 sm:h-10 rounded-full border-4 border-slate-800 bg-primary text-slate-900 font-bold text-sm sm:text-base shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 transition-transform group-hover:scale-110">
                    {idx + 1}
                  </div>
                  
                  {/* Step Content Card */}
                  <div className="ml-6 sm:ml-10 md:ml-0 w-full md:w-[calc(50%-2.5rem)] bg-slate-900/80 backdrop-blur-sm p-4 sm:p-6 rounded-xl border border-slate-700/50 shadow-sm relative group-hover:border-primary/50 transition-all">
                    <p className="text-sm sm:text-base text-slate-300 leading-relaxed font-medium">{step}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
