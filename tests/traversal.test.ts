import { createOrchestrator } from '../src/core/orchestrator';

describe('Semantic Valley Traversal', () => {
  it.skip('should complete S1-S11 traversal with placeholders', async () => {
    // This test requires an OpenAI API key
    // Run with: OPENAI_API_KEY=your_key npm test
    
    const orchestrator = await createOrchestrator();
    
    const problem = {
      title: 'Test Problem',
      statement: 'How can we improve team collaboration in remote work environments?'
    };

    const result = await orchestrator.runTraversal(problem);
    
    // Verify basic structure
    expect(result.runId).toMatch(/^run_\d+_[a-z0-9]+$/);
    expect(result.packets).toHaveLength(11);
    expect(result.resolution).toBeTruthy();
    expect(result.metadata.durations).toBeDefined();
    expect(result.metadata.totalDuration).toBeGreaterThan(0);

    // Verify all stations are present
    const stations = result.packets.map(p => p.station);
    expect(stations).toEqual(['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11']);

    // Verify document generation stations (S2-S5) have proper operations
    const s2Packet = result.packets.find(p => p.station === 'S2');
    const s3Packet = result.packets.find(p => p.station === 'S3');
    const s4Packet = result.packets.find(p => p.station === 'S4');
    const s5Packet = result.packets.find(p => p.station === 'S5');
    
    expect(s2Packet?.payload?.DS).toBeTruthy();
    expect(s3Packet?.payload?.SP).toBeTruthy();
    expect(s4Packet?.payload?.GD).toBeTruthy();
    expect(s5Packet?.payload?.EC).toBeTruthy();

    // Verify S11 has resolution
    const s11Packet = result.packets.find(p => p.station === 'S11');
    expect(s11Packet?.payload?.Final).toBeTruthy();

    console.log('Traversal completed successfully:', {
      runId: result.runId,
      totalDuration: result.metadata.totalDuration,
      stationCount: result.packets.length
    });
    
  }, 30000); // 30 second timeout for LLM calls
});