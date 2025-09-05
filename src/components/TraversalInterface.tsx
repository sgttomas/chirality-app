'use client';

import { useState } from 'react';
import { ProblemForm } from './ProblemForm';
import { StationDisplay } from './StationDisplay';
import { ResultsDisplay } from './ResultsDisplay';

export interface TraversalState {
  status: 'idle' | 'running' | 'completed' | 'error';
  currentStation?: string;
  runId?: string;
  stations?: Array<{
    station: string;
    label: string;
    modality: string;
    operation: string;
    duration: number;
    output: string;
    status: 'pending' | 'running' | 'completed';
  }>;
  resolution?: string;
  error?: string;
  metadata?: {
    durations: Record<string, number>;
    totalDuration: number;
    totalTokens: number;
  };
}

export function TraversalInterface() {
  const [traversalState, setTraversalState] = useState<TraversalState>({
    status: 'idle'
  });

  const handleStartTraversal = async (
    problem: { title: string; statement: string }, 
    mode: 'full' | 'foundation',
    initialVector?: {
      matrixC: string[];
      matrixD: string[];
      matrixX: string[];
      matrixE: string[];
    }
  ) => {
    setTraversalState({
      status: 'running',
      stations: [],
      currentStation: undefined
    });

    try {
      const response = await fetch('/api/pipeline/traverse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          problem: {
            ...problem,
            initialVector
          },
          options: { mode }
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Traversal failed');
      }

      setTraversalState({
        status: 'completed',
        runId: data.traversalId,
        stations: data.stations.map((station: any) => ({
          ...station,
          status: 'completed' as const
        })),
        resolution: data.resolution,
        metadata: data.metadata
      });

    } catch (error) {
      setTraversalState({
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      });
    }
  };

  const handleReset = () => {
    setTraversalState({ status: 'idle' });
  };

  return (
    <div className="space-y-8">
      {traversalState.status === 'idle' && (
        <ProblemForm onSubmit={handleStartTraversal} />
      )}
      
      {(traversalState.status === 'running' || traversalState.status === 'completed') && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Semantic Valley Traversal</h2>
            <button
              onClick={handleReset}
              className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-md"
            >
              Start New Traversal
            </button>
          </div>
          
          <StationDisplay 
            stations={traversalState.stations || []}
            currentStation={traversalState.currentStation}
            status={traversalState.status}
          />
          
          {traversalState.status === 'completed' && traversalState.resolution && (
            <ResultsDisplay 
              resolution={traversalState.resolution}
              runId={traversalState.runId}
              metadata={traversalState.metadata}
            />
          )}
        </div>
      )}
      
      {traversalState.status === 'error' && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-semibold text-red-800 mb-2">Traversal Failed</h3>
              <p className="text-red-600">{traversalState.error}</p>
            </div>
            <button
              onClick={handleReset}
              className="px-4 py-2 text-sm bg-red-100 hover:bg-red-200 text-red-800 rounded-md"
            >
              Try Again
            </button>
          </div>
        </div>
      )}
    </div>
  );
}