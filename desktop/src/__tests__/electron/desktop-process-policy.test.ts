import { describe, expect, it } from 'vitest';
import { resolveUserDataOverride } from '../../../electron/desktop-process-policy';

describe('resolveUserDataOverride', () => {
  it('reports absent when the variable is unset or blank', () => {
    expect(resolveUserDataOverride({})).toEqual({ kind: 'absent' });
    expect(resolveUserDataOverride({ CHIRALITY_USER_DATA: '' })).toEqual({ kind: 'absent' });
    expect(resolveUserDataOverride({ CHIRALITY_USER_DATA: '   ' })).toEqual({
      kind: 'absent'
    });
  });

  it('applies an absolute directory', () => {
    expect(
      resolveUserDataOverride({
        CHIRALITY_USER_DATA: '/Users/tester/Library/Application Support/chirality-frontend'
      })
    ).toEqual({
      kind: 'apply',
      directory: '/Users/tester/Library/Application Support/chirality-frontend'
    });
  });

  it('trims surrounding whitespace before applying', () => {
    expect(resolveUserDataOverride({ CHIRALITY_USER_DATA: '  /tmp/isolated-user-data  ' })).toEqual(
      { kind: 'apply', directory: '/tmp/isolated-user-data' }
    );
  });

  it('normalises redundant separators without changing the target', () => {
    expect(resolveUserDataOverride({ CHIRALITY_USER_DATA: '/tmp//iso/./data' })).toEqual({
      kind: 'apply',
      directory: '/tmp/iso/data'
    });
  });

  it('rejects a relative value instead of resolving it against an unknown cwd', () => {
    // A Finder launch and a shell launch have different working directories,
    // so resolving a relative value would pick a different directory per path.
    expect(resolveUserDataOverride({ CHIRALITY_USER_DATA: 'relative/user-data' })).toEqual({
      kind: 'rejected',
      requested: 'relative/user-data',
      reason: 'not-absolute'
    });
    expect(resolveUserDataOverride({ CHIRALITY_USER_DATA: './data' })).toEqual({
      kind: 'rejected',
      requested: './data',
      reason: 'not-absolute'
    });
    expect(resolveUserDataOverride({ CHIRALITY_USER_DATA: '~/Library/Chirality' })).toEqual({
      kind: 'rejected',
      requested: '~/Library/Chirality',
      reason: 'not-absolute'
    });
  });
});
