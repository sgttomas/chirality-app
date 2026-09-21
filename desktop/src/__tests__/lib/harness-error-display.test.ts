import { describe, expect, it } from 'vitest';
import { HarnessApiClientError } from '../../lib/harness/client';
import { toHarnessUiError } from '../../lib/harness/error-display';

describe('harness ui error mapping', () => {
  it('keeps instruction adoption pending distinct from a failed boot or a new chat', () => {
    const mapped = toHarnessUiError(new HarnessApiClientError(503, 'INSTRUCTION_ADOPTION_PENDING', 'raw thread details'));
    expect(mapped.title).toBe('Instruction update pending');
    expect(mapped.code).toBe('INSTRUCTION_ADOPTION_PENDING');
    expect(mapped.message).toContain('next turn has not started');
    expect(mapped.message).not.toContain('raw thread details');
    expect(mapped.nextStep).toContain('retry in this chat');
  });

  it('maps known typed errors to actionable copy', () => {
    const input = new HarnessApiClientError(
      404,
      'WORKING_ROOT_INACCESSIBLE',
      'projectRoot is not accessible'
    );

    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Working Root Unavailable');
    expect(mapped.code).toBe('WORKING_ROOT_INACCESSIBLE');
    expect(mapped.nextStep).toContain('Re-select');
  });

  it('maps TURN_IN_PROGRESS to retry guidance', () => {
    const input = new HarnessApiClientError(409, 'TURN_IN_PROGRESS', 'A turn is already active');
    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Turn Already In Progress');
    expect(mapped.code).toBe('TURN_IN_PROGRESS');
    expect(mapped.nextStep).toContain('Wait for the current turn');
  });

  it('maps MISSING_API_KEY to provisioning guidance', () => {
    const input = new HarnessApiClientError(
      503,
      'MISSING_API_KEY',
      'Anthropic API key is not configured'
    );
    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('API Key Not Configured');
    expect(mapped.code).toBe('MISSING_API_KEY');
    expect(mapped.nextStep).toContain('ANTHROPIC_API_KEY');
  });

  it('includes attachment failure detail preview when server provides rejection details', () => {
    const input = new HarnessApiClientError(
      400,
      'ATTACHMENT_FAILURE',
      'Turn requires text content or at least one valid attachment',
      {
        category: 'ALL_ATTACHMENTS_FAILED_NO_TEXT',
        rejectedAttachmentCount: 3,
        attachmentErrors: [
          {
            path: '/tmp/alpha.txt',
            reason: 'Attachment file not found: /tmp/alpha.txt'
          },
          {
            path: '/tmp/beta.md',
            reason: 'Attachment file is not readable: /tmp/beta.md'
          },
          {
            path: '/tmp/gamma.csv',
            reason: 'Attachment exceeds per-file size limit (10485760 bytes)'
          }
        ]
      }
    );

    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Attachment Validation Failed');
    expect(mapped.message).toContain('Rejections:');
    expect(mapped.message).toContain('alpha.txt: Attachment file not found');
    expect(mapped.message).toContain('beta.md: Attachment file is not readable');
    expect(mapped.message).toContain('(+1 more)');
  });

  it('falls back to base attachment copy when rejection details are malformed', () => {
    const input = new HarnessApiClientError(400, 'ATTACHMENT_FAILURE', 'Attachment failure', {
      attachmentErrors: [{ bad: 'shape' }]
    });

    const mapped = toHarnessUiError(input);
    expect(mapped.message).toBe('No executable attachment content was available for this turn.');
  });

  it('falls back to generic copy for unknown codes', () => {
    const input = new HarnessApiClientError(500, 'SOMETHING_NEW', 'Unexpected backend path');
    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Harness Request Failed');
    expect(mapped.message).toContain('SOMETHING_NEW');
  });

  it('maps instruction-root failures to recovery guidance', () => {
    const input = new HarnessApiClientError(
      500,
      'INSTRUCTION_ROOT_INVALID',
      'Instruction root is missing required resources'
    );

    const mapped = toHarnessUiError(input);
    expect(mapped.title).toBe('Instruction Root Invalid');
    expect(mapped.code).toBe('INSTRUCTION_ROOT_INVALID');
    expect(mapped.nextStep).toContain('Reinstall');
  });

  it('returns unexpected copy for non-client errors', () => {
    const mapped = toHarnessUiError(new Error('boom'));
    expect(mapped.title).toBe('Unexpected Harness Failure');
    expect(mapped.message).toContain('boom');
  });

  it('distinguishes MODEL_NOT_IN_CATALOG at session creation from an existing session', () => {
    const details = { reason: 'MODEL_NOT_IN_CATALOG', model: 'gpt-alt', available: ['gpt-default'] };
    const created = toHarnessUiError(new HarnessApiClientError(400, 'INVALID_REQUEST', 'not in catalog', details), { origin: 'session-create' });
    expect(created.title).toBe('Model No Longer Offered');
    expect(created.message).toBe('Model gpt-alt is no longer offered by your Codex account. Refresh your account status and choose again.');
    expect(created.nextStep).toContain('Refresh your account status');

    const booted = toHarnessUiError(new HarnessApiClientError(503, 'ENGINE_UNAVAILABLE', 'not in catalog', details), { origin: 'session' });
    expect(booted.message).toBe('This chat used gpt-alt, which your Codex account no longer offers. Start a new chat.');
    // The default origin is the existing-session wording; the turn stream omits the model and the session names it.
    const streamed = toHarnessUiError(new HarnessApiClientError(503, 'ENGINE_UNAVAILABLE', 'not in catalog', { reason: 'MODEL_NOT_IN_CATALOG' }), { sessionModel: 'gpt-old' });
    expect(streamed.message).toBe('This chat used gpt-old, which your Codex account no longer offers. Start a new chat.');
    const unnamed = toHarnessUiError(new HarnessApiClientError(400, 'INVALID_REQUEST', 'not in catalog', { reason: 'MODEL_NOT_IN_CATALOG' }), { origin: 'session-create' });
    expect(unnamed.message).toBe('The chosen model is no longer offered by your Codex account. Refresh your account status and choose again.');
  });
});


it('uses safe initialization timeout copy and retained-session guidance', () => {
  const error = new HarnessApiClientError(504, 'ENGINE_UNAVAILABLE', 'secret socket details', { operation: 'boot', transportReason: 'timeout', sessionId: 'session-fixture' });
  const display = toHarnessUiError(error, { bootBeforePrompt: true });
  expect(display.title).toBe('Chat took too long to start');
  expect(display.message).toBe('Your message is saved.');
  expect(display.message).not.toContain('session-fixture');
  expect(display.message).not.toContain('secret');
  expect(display.message).not.toContain('daemon is unavailable');
  expect(display.nextStep).toContain('check this chat');
});


it.each([['BOOT_TIMEOUT', 'Chat took too long to start'], ['BOOT_CANCELLED', 'Chat could not start']])('renders %s as initialization state without raw causes', (reason, title) => {
  const display = toHarnessUiError(new HarnessApiClientError(503, 'ENGINE_UNAVAILABLE', 'raw sensitive cause', { reason, operation: 'boot', sessionId: '/private/socket?token=secret' }));
  expect(display.title).toBe(title);
  expect(display.message).not.toContain('sensitive');
  expect(display.message).not.toContain('private');
  expect(display.message).not.toContain('secret');
});
