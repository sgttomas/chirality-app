#!/usr/bin/env python3
"""
extract_agent_output.py
Extracts the final assistant text message from a Claude agent output file.

Agent output files are JSONL (one JSON object per line) containing the full
conversation. This script extracts the last assistant text block — which is
the agent's final report — and writes it to stdout or a file.

Usage:
    python3 extract_agent_output.py <agent_output_file> [output_file]

If output_file is omitted, writes to stdout.
"""

import json
import sys

def extract_last_assistant_text(input_path):
    texts = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if obj.get('type') == 'assistant':
                    msg = obj.get('message', {})
                    for block in msg.get('content', []):
                        if block.get('type') == 'text':
                            texts.append(block['text'])
            except (json.JSONDecodeError, KeyError):
                pass
    return texts[-1] if texts else ''

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <agent_output_file> [output_file]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    result = extract_last_assistant_text(input_path)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        with open(output_path, 'w') as f:
            f.write(result)
            f.write('\n')
    else:
        print(result)
