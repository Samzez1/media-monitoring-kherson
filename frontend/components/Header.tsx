'use client';

import { useState } from 'react';
import { Search, Menu, X } from 'lucide-react';

interface HeaderProps {
  onSearch: (query: string) => void;
}

export const Header = ({ onSearch }: HeaderProps) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [menuOpen, setMenuOpen] = useState(false);

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch(searchQuery);
  };

  return (
    <header className="bg-gradient-to-r from-primary to-blue-600 text-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="text-2xl">📰</span>
            <div>
              <h1 className="text-2xl font-bold">Media Monitoring Kherson</h1>
              <p className="text-sm text-blue-100">Национальные проекты РФ</p>
            </div>
          </div>

          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="lg:hidden p-2 hover:bg-blue-500 rounded transition-colors"
          >
            {menuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Поисковая строка */}
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Поиск по заголовку и содержимому..."
            className="flex-1 px-4 py-2 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-yellow-400"
          />
          <button
            type="submit"
            className="px-6 py-2 bg-blue-700 hover:bg-blue-800 rounded-lg transition-colors flex items-center gap-2 font-medium"
          >
            <Search size={20} />
            <span className="hidden sm:inline">Найти</span>
          </button>
        </form>

        {/* Дополнительная информация */}
        <div className="mt-4 text-sm text-blue-100 flex flex-wrap gap-4">
          <span>🏢 Агрегация данных из федеральных и региональных источников</span>
          <span>🤖 NLP классификация по 12 Национальным проектам</span>
          <span>📍 Фильтрация по Херсонской области</span>
        </div>
      </div>
    </header>
  );
};
