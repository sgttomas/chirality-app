# Troubleshooting Guide

Complete solutions for common issues in Chirality AI App.

## Quick Diagnosis

### System Health Check
```bash
curl http://localhost:3001/api/healthz     # Basic health
curl http://localhost:3001/api/readyz      # Dependency check
curl http://localhost:3001/api/chat/debug  # System status
curl http://localhost:3001/api/core/state  # Current state
```

### Common Issue Patterns
- **Document Generation Fails**: OpenAI API key or connectivity issues
- **Chat Not Streaming**: Browser SSE support or network problems
- **State Not Persisting**: File permissions or disk space issues  
- **UI Not Loading**: Development server or port conflicts

## Installation & Setup Issues

### OpenAI API Key Problems
**Symptoms**: Authentication errors, generation failures, "API key required" messages

**Solutions**:
1. **Verify API Key Format**:
   ```bash
   # Correct format starts with sk-proj-
   echo $OPENAI_API_KEY
   cat .env.local  # Should contain: OPENAI_API_KEY=sk-proj-...
   ```

2. **Test API Key**:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

3. **Common Issues**:
   - **Expired Key**: Generate new key in OpenAI dashboard
   - **Insufficient Credits**: Check OpenAI account billing  
   - **Rate Limits**: Wait or upgrade OpenAI plan
   - **Wrong Project**: Ensure key belongs to correct project

### Node.js & Dependencies
**Symptoms**: Installation failures, version compatibility errors, module not found

**Solutions**:
1. **Check Node.js Version**:
   ```bash
   node --version  # Should be 18.0.0 or higher
   ```

2. **Clean Installation**:
   ```bash
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install
   ```

3. **Version Manager**:
   ```bash
   # Using nvm
   nvm install 18
   nvm use 18
   npm install
   ```

### Port & Network Issues
**Symptoms**: Cannot connect to localhost, port conflicts, ERR_CONNECTION_REFUSED

**Solutions**:
1. **Check Port Usage**:
   ```bash
   lsof -i :3001  # Check what's using port 3001
   PORT=3002 npm run dev  # Use different port
   ```

2. **Network Configuration**:
   ```bash
   ping localhost
   curl http://127.0.0.1:3001/api/healthz  # Try IP instead of localhost
   ```

## Document Generation Issues

### Three-Pass Generation Failures

#### Incomplete Generation
**Symptoms**: Progress stops partway, missing documents, hangs indefinitely

**Diagnostic Steps**:
1. **Check Generation Logs**: Browser console or `/chat-admin` dashboard
2. **Test Single Documents**:
   ```bash
   curl -X POST http://localhost:3001/api/core/run \
     -H "Content-Type: application/json" \
     -d '{"kind": "DS"}'
   ```

**Solutions**:
1. **OpenAI Issues**: Check rate limits, billing status, model availability
2. **Content Issues**: Simplify problem statement, avoid special characters
3. **Resource Issues**: Ensure disk space, check memory usage, restart server

#### Document Quality Issues
**Symptoms**: Poor quality content, incomplete information, irrelevant responses

**Solutions**:
1. **Problem Statement Optimization**:
   ```bash
   # Set clear, specific problem
   curl -X POST http://localhost:3001/api/core/state \
     -H "Content-Type: application/json" \
     -d '{"problem": {"statement": "Clear, specific problem description"}}'
   ```

2. **Generation Parameters**:
   - Check OPENAI_MODEL environment variable
   - Verify DEFAULT_TEMPERATURE setting (should be 0.6)
   - Ensure MAX_OUTPUT_TOKENS is sufficient (800+)

#### Matrix Integration Issues
**Symptoms**: Matrix data not loading, framework run failures, ingestion errors

**Solutions**:
1. **Framework Run Validation**:
   ```bash
   # Check framework run exists
   ls -la fixtures/runs/sample_happy_001/
   # Verify manifest structure
   cat fixtures/runs/sample_happy_001/index.json
   ```

2. **Matrix File Format**:
   ```bash
   # Check JSONL format
   head -1 fixtures/runs/sample_happy_001/snapshots/C.jsonl
   # Should be valid JSON with required fields
   ```

### State Management Issues

#### State Corruption or Loss
**Symptoms**: Documents disappear, state resets, generation history lost

**Diagnostic Steps**:
1. **Check State File**:
   ```bash
   cat store/state.json          # View current state
   ls -la store/                 # Check permissions
   python -m json.tool store/state.json  # Validate JSON
   ```

**Solutions**:
1. **File Permissions**:
   ```bash
   chmod 755 store/
   chmod 644 store/state.json
   ```

2. **State Recovery**:
   ```bash
   # Backup and reset
   cp store/state.json store/state.json.backup
   curl -X DELETE http://localhost:3001/api/core/state
   ```

## Chat Interface Issues

### Streaming Response Problems

#### Chat Not Streaming
**Symptoms**: Messages appear all at once, "Connecting..." never resolves

**Solutions**:
1. **Browser Support**:
   ```javascript
   // Check in browser console
   console.log('EventSource' in window);  // Should return true
   ```

2. **Network Test**:
   ```bash
   # Test SSE endpoint directly
   curl -N -H "Accept: text/event-stream" \
     -X POST http://localhost:3001/api/chat/stream \
     -H "Content-Type: application/json" \
     -d '{"message": "test"}'
   ```

3. **Browser Debugging**:
   - Check Network tab for failed SSE connections
   - Disable ad blockers that might interfere
   - Try incognito/private mode

#### Context Injection Failures  
**Symptoms**: AI gives generic responses, no document references

**Solutions**:
1. **Verify Documents Exist**:
   ```bash
   curl http://localhost:3001/api/core/state
   # Should show finals with DS/SP/X/M documents
   ```

2. **Generate Documents First**: Chat requires documents for context
3. **Clear and Regenerate**: If documents corrupted, clear state and regenerate

### Command Recognition Issues
**Symptoms**: Commands treated as regular messages, no special processing

**Solutions**:
1. **Correct Command Format**:
   ```
   ✅ Correct: set problem: Implement user authentication
   ❌ Wrong: set problem Implement user authentication
   ❌ Wrong: setproblem: Implement user authentication
   ```

2. **Case Sensitivity**: Use lowercase `set problem:` and `generate DS`

## Performance Issues

### Slow Generation Times
**Expected Performance**:
- Single Document: 3-8 seconds
- Complete Three-Pass: 2-4 minutes
- Chat Response: <2 seconds first token

**If Slower**:
1. **Check OpenAI API Status**: Monitor response times
2. **Network Speed**: Verify internet connectivity 
3. **Problem Complexity**: Simplify for testing
4. **Resource Usage**: Monitor CPU/memory with `top`

### Memory Issues
**Symptoms**: Browser tabs unresponsive, server crashes, system slowdown

**Solutions**:
1. **Restart Development Server**:
   ```bash
   # Increase memory limit if needed
   NODE_OPTIONS="--max-old-space-size=4096" npm run dev
   ```

2. **Browser Resources**:
   - Close unnecessary tabs
   - Clear browser cache
   - Use browser task manager to check memory

3. **State Cleanup**:
   ```bash
   # Clear large state files
   curl -X DELETE http://localhost:3001/api/core/state
   ```

## Browser-Specific Issues

### Safari Problems
**Common Issues**: SSE limitations, localStorage differences, CSS inconsistencies

**Solutions**:
1. Enable "Develop" menu in Safari preferences
2. Test in Safari Technology Preview
3. Check console for specific error messages

### Firefox Problems
**Common Issues**: Privacy settings blocking requests

**Solutions**:
1. Check tracking protection settings
2. Verify localStorage is enabled
3. Test in private browsing to isolate extensions

## Advanced Debugging

### Debug Mode
```bash
# Enable verbose logging
DEBUG=* npm run dev

# OpenAI-specific debugging
DEBUG=openai:* npm run dev
```

### State Inspection
```bash
# Complete state dump
curl http://localhost:3001/api/core/state | python -m json.tool

# System status
curl http://localhost:3001/api/chat/debug | python -m json.tool
```

### Performance Monitoring
```bash
# Monitor API response times
curl -w "Total time: %{time_total}s\n" \
  http://localhost:3001/api/core/orchestrate
```

## Getting Help

### Information to Collect
1. **System Info**:
   ```bash
   node --version
   npm --version
   cat package.json | grep version
   echo $OPENAI_MODEL
   ```

2. **Error Details**:
   - Browser console errors
   - Network tab failures
   - Server terminal logs

3. **Reproduction Steps**:
   - Exact steps to reproduce
   - Problem statement used
   - Browser and OS details

### Support Resources
- **GitHub Issues**: Bug reports with complete information
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Development setup and debugging
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System design details
- **Admin Dashboard**: `/chat-admin` for real-time system state

### Reset Everything
Complete reset if all else fails:
```bash
# Stop server (Ctrl+C)
rm -rf node_modules package-lock.json .next
npm install
npm run dev
```

---

*This guide covers the most common issues. For additional help, check the GitHub repository or create an issue with detailed information.*