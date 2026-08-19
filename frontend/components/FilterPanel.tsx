'use client';

import { useState, useEffect } from 'react';
import { NationalProject, Source } from '@/lib/types';
import { projectAPI, sourceAPI } from '@/lib/api';
import { ChevronDown } from 'lucide-react';

interface FilterPanelProps {
  onProjectSelect: (projectId: number | null) => void;
  onSourceSelect: (sourceId: number | null) => void;
}

export const FilterPanel = ({ onProjectSelect, onSourceSelect }: FilterPanelProps) => {
  const [projects, setProjects] = useState<NationalProject[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [selectedProject, setSelectedProject] = useState<number | null>(null);
  const [selectedSource, setSelectedSource] = useState<number | null>(null);
  const [expandProjects, setExpandProjects] = useState(true);
  const [expandSources, setExpandSources] = useState(true);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFilters = async () => {
      try {
        const [projectsRes, sourcesRes] = await Promise.all([
          projectAPI.listProjects({ active_only: true }),
          sourceAPI.listSources({ active_only: true }),
        ]);

        setProjects(projectsRes.data);
        setSources(sourcesRes.data);
      } catch (error) {
        console.error('Error loading filters:', error);
      } finally {
        setLoading(false);
      }
    };

    loadFilters();
  }, []);

  const handleProjectSelect = (projectId: number | null) => {
    setSelectedProject(projectId);
    onProjectSelect(projectId);
  };

  const handleSourceSelect = (sourceId: number | null) => {
    setSelectedSource(sourceId);
    onSourceSelect(sourceId);
  };

  if (loading) {
    return <div className="animate-pulse bg-gray-200 h-64 rounded-lg"></div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Фильтры</h2>

      {/* Национальные проекты */}
      <div className="mb-6">
        <button
          onClick={() => setExpandProjects(!expandProjects)}
          className="flex items-center justify-between w-full font-semibold text-gray-900 mb-3 hover:text-primary transition-colors"
        >
          <span>🎯 Национальные проекты ({projects.length})</span>
          <ChevronDown size={20} className={expandProjects ? 'rotate-180' : ''} />
        </button>

        {expandProjects && (
          <div className="space-y-2 pl-2">
            <button
              onClick={() => handleProjectSelect(null)}
              className={`block w-full text-left px-3 py-2 rounded transition-colors ${
                selectedProject === null
                  ? 'bg-primary text-white font-medium'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              Все проекты
            </button>

            {projects.map((project) => (
              <button
                key={project.id}
                onClick={() => handleProjectSelect(project.id)}
                className={`block w-full text-left px-3 py-2 rounded transition-colors ${
                  selectedProject === project.id
                    ? 'bg-primary text-white font-medium'
                    : 'hover:bg-gray-100 text-gray-700'
                }`}
              >
                <span
                  className="inline-block w-3 h-3 rounded-full mr-2"
                  style={{ backgroundColor: project.color_badge }}
                ></span>
                {project.name}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Источники */}
      <div className="mb-6">
        <button
          onClick={() => setExpandSources(!expandSources)}
          className="flex items-center justify-between w-full font-semibold text-gray-900 mb-3 hover:text-primary transition-colors"
        >
          <span>📰 Источники ({sources.length})</span>
          <ChevronDown size={20} className={expandSources ? 'rotate-180' : ''} />
        </button>

        {expandSources && (
          <div className="space-y-2 pl-2">
            <button
              onClick={() => handleSourceSelect(null)}
              className={`block w-full text-left px-3 py-2 rounded transition-colors ${
                selectedSource === null
                  ? 'bg-primary text-white font-medium'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              Все источники
            </button>

            {sources.map((source) => (
              <button
                key={source.id}
                onClick={() => handleSourceSelect(source.id)}
                className={`block w-full text-left px-3 py-2 rounded transition-colors text-sm ${
                  selectedSource === source.id
                    ? 'bg-primary text-white font-medium'
                    : 'hover:bg-gray-100 text-gray-700'
                }`}
              >
                {source.name}
                <span className="text-xs ml-2 opacity-75">({source.source_type})</span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Кнопка сброса */}
      <button
        onClick={() => {
          handleProjectSelect(null);
          handleSourceSelect(null);
        }}
        className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors font-medium"
      >
        Очистить фильтры
      </button>
    </div>
  );
};
