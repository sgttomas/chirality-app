'use client';

import { useState } from 'react';

interface ProblemFormProps {
  onSubmit: (problem: { title: string; statement: string }, mode: 'full' | 'foundation') => void;
}

export function ProblemForm({ onSubmit }: ProblemFormProps) {
  const [title, setTitle] = useState('');
  const [statement, setStatement] = useState('');
  const [mode, setMode] = useState<'full' | 'foundation'>('foundation');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim() || !statement.trim()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit({ title: title.trim(), statement: statement.trim() }, mode);
    } finally {
      setIsSubmitting(false);
    }
  };

  const isValid = title.trim().length > 0 && statement.trim().length > 0;

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold">Problem Definition</h2>
        <p className="text-gray-600 text-sm mt-1">
          Define your problem to begin the 11-station semantic valley traversal
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="p-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Traversal Mode
          </label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                name="mode"
                value="foundation"
                checked={mode === 'foundation'}
                onChange={(e) => setMode(e.target.value as 'foundation')}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                disabled={isSubmitting}
              />
              <span className="ml-2 text-sm text-gray-700">
                <strong>Foundation</strong> - S1-S5 + S11 (6 stations, ~2-3 min)
              </span>
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="mode"
                value="full"
                checked={mode === 'full'}
                onChange={(e) => setMode(e.target.value as 'full')}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                disabled={isSubmitting}
              />
              <span className="ml-2 text-sm text-gray-700">
                <strong>Full</strong> - S1-S11 (11 stations, ~5-6 min)
              </span>
            </label>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Foundation mode generates the 4 core documents + resolution. Full mode includes iterative refinement cycles.
          </p>
        </div>

        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
            Problem Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Brief title describing your problem"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isSubmitting}
            required
          />
        </div>

        <div>
          <label htmlFor="statement" className="block text-sm font-medium text-gray-700 mb-2">
            Problem Statement *
          </label>
          <textarea
            id="statement"
            value={statement}
            onChange={(e) => setStatement(e.target.value)}
            placeholder="Detailed description of the problem you want to solve..."
            rows={6}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
            disabled={isSubmitting}
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            Be as specific as possible. This will be analyzed through systematic, process, epistemic, and alethic modalities.
          </p>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={!isValid || isSubmitting}
            className={`px-6 py-3 font-medium rounded-md transition-colors ${
              isValid && !isSubmitting
                ? 'bg-blue-600 hover:bg-blue-700 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {isSubmitting ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Starting Traversal...
              </span>
            ) : (
              'Begin Semantic Valley Traversal'
            )}
          </button>
        </div>
      </form>
    </div>
  );
}