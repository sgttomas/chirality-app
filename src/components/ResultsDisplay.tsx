'use client';

interface ResultsDisplayProps {
  resolution: string;
  runId?: string;
  metadata?: {
    durations: Record<string, number>;
    totalDuration: number;
    totalTokens: number;
  };
}

export function ResultsDisplay({ resolution, runId, metadata }: ResultsDisplayProps) {
  const handleExportRun = async () => {
    if (!runId) return;
    
    try {
      const response = await fetch(`/api/export/run?runId=${runId}`);
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'Export failed');
      }
      
      // Show export information
      alert(`Run exported successfully!\n\nFiles:\n- ${data.files.runJson}\n- ${data.files.packetsJsonl}\n\nTotal size: ${Math.round(data.size.total / 1024)} KB`);
    } catch (error) {
      alert(`Export failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Resolution */}
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-xl font-semibold text-green-800">Final Resolution</h3>
          <p className="text-gray-600 text-sm mt-1">
            Synthesized solution from 11-station semantic valley traversal
          </p>
        </div>
        
        <div className="p-6">
          <div className="prose max-w-none">
            <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded-md">
              <div className="whitespace-pre-wrap text-gray-800">
                {resolution}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Metadata & Export */}
      {metadata && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold">Traversal Metadata</h3>
              {runId && (
                <button
                  onClick={handleExportRun}
                  className="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-md"
                >
                  Export Run Files
                </button>
              )}
            </div>
          </div>
          
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Summary Stats */}
              <div className="space-y-3">
                <h4 className="font-medium text-gray-900">Summary</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Duration:</span>
                    <span className="font-medium">{(metadata.totalDuration / 1000).toFixed(2)}s</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Tokens:</span>
                    <span className="font-medium">{metadata.totalTokens.toLocaleString()}</span>
                  </div>
              {runId && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Run ID:</span>
                  <span className="font-mono text-xs bg-gray-100 px-2 py-1 rounded">{runId}</span>
                </div>
              )}
              {runId && (
                <div className="pt-3 border-t border-gray-100 flex gap-2">
                  <a
                    className="inline-flex items-center px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700 text-xs"
                    href={`/api/export/file?runId=${runId}&name=run.json`}
                  >
                    Download run.json
                  </a>
                  <a
                    className="inline-flex items-center px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700 text-xs"
                    href={`/api/export/file?runId=${runId}&name=packets.jsonl`}
                  >
                    Download packets.jsonl
                  </a>
                </div>
              )}
            </div>
          </div>

              {/* Station Durations */}
              <div className="md:col-span-2 space-y-3">
                <h4 className="font-medium text-gray-900">Station Performance</h4>
                <div className="space-y-1">
                  {Object.entries(metadata.durations)
                    .sort(([a], [b]) => a.localeCompare(b, undefined, { numeric: true }))
                    .map(([station, duration]) => (
                    <div key={station} className="flex items-center space-x-3">
                      <span className="text-sm font-mono w-8 text-gray-600">{station}:</span>
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                          style={{ 
                            width: `${Math.max(5, (duration / metadata.totalDuration) * 100)}%` 
                          }}
                        />
                      </div>
                      <span className="text-sm text-gray-600 w-16 text-right">{duration}ms</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
