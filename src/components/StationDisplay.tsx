'use client';

import { STATION_META } from '../domain/station';
import { ModalityChip } from './ModalityChip';

interface StationProps {
  station: string;
  label: string;
  modality: string;
  operation: string;
  duration: number;
  output: string;
  status: 'pending' | 'running' | 'completed';
}

interface StationDisplayProps {
  stations: StationProps[];
  currentStation?: string;
  status: 'running' | 'completed';
}

export function StationDisplay({ stations, currentStation, status }: StationDisplayProps) {
  // Create station list from STATION_META, merging with actual results
  const stationList = Object.values(STATION_META).map(meta => {
    const stationResult = stations.find(s => s.station === meta.station);
    
    return {
      ...meta,
      duration: stationResult?.duration || 0,
      output: stationResult?.output || '',
      status: stationResult?.status || (
        status === 'running' && currentStation === meta.station ? 'running' : 
        stationResult ? 'completed' : 'pending'
      ) as 'pending' | 'running' | 'completed'
    };
  });

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <h3 className="text-xl font-semibold">11-Station Semantic Valley Traversal</h3>
          <div className="text-sm text-gray-600">
            {status === 'running' ? 'In Progress...' : 'Completed'}
          </div>
        </div>
        <p className="text-gray-600 text-sm mt-1">
          Executed internally in 9 grouped stages following ontological progression
        </p>
      </div>

      <div className="p-6">
        <div className="space-y-4">
          {stationList.map((station, index) => (
            <div key={station.station} className="flex items-start space-x-4">
              {/* Station Number & Status */}
              <div className="flex-shrink-0 flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  station.status === 'completed' 
                    ? 'bg-green-100 text-green-700 border-2 border-green-300'
                    : station.status === 'running'
                    ? 'bg-blue-100 text-blue-700 border-2 border-blue-300 animate-pulse'
                    : 'bg-gray-100 text-gray-500 border-2 border-gray-200'
                }`}>
                  {station.status === 'completed' ? (
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  ) : station.status === 'running' ? (
                    <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  ) : (
                    station.station.slice(1)
                  )}
                </div>
                {index < stationList.length - 1 && (
                  <div className={`w-px h-12 ml-4 ${
                    station.status === 'completed' ? 'bg-green-300' : 'bg-gray-200'
                  }`} />
                )}
              </div>

              {/* Station Content */}
              <div className="flex-1 min-w-0 pb-8">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="font-medium text-gray-900">{station.label}</h4>
                      <ModalityChip modality={station.modality} />
                      <span className="text-xs text-gray-500 font-mono bg-gray-100 px-2 py-1 rounded">
                        {station.operation}
                      </span>
                      <span className="text-xs text-gray-500">
                        {station.group}
                      </span>
                    </div>
                    
                    {station.output && (
                      <div className="mt-3 p-3 bg-gray-50 rounded-md border-l-4 border-gray-300">
                        <p className="text-sm text-gray-700 whitespace-pre-wrap line-clamp-3">
                          {station.output.length > 200 
                            ? `${station.output.substring(0, 200)}...` 
                            : station.output
                          }
                        </p>
                        {station.output.length > 200 && (
                          <button className="text-xs text-blue-600 hover:text-blue-800 mt-1">
                            Show more
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                  
                  {station.duration > 0 && (
                    <div className="text-xs text-gray-500 ml-4">
                      {station.duration}ms
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}