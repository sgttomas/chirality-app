// The controls guard reads literal App vocabulary in RequestCards.tsx. Keep
// that projection generated from the same maintained table the host reads.
import { readFileSync, writeFileSync } from 'node:fs';
const source = new URL('../src/requestAnswerWords.json', import.meta.url);
const target = new URL('../src/RequestCards.tsx', import.meta.url);
const table = JSON.parse(readFileSync(source, 'utf8'));
const start = '// BEGIN GENERATED REQUEST ANSWER WORDS';
const end = '// END GENERATED REQUEST ANSWER WORDS';
const generated = `${start}\nexport const DECISION_WORDS = ${JSON.stringify(table.decisions, null, 2)} as const;\nexport const QUESTION_CHOICE_WORDS = ${JSON.stringify(table.questionChoices, null, 2)} as const;\n${end}`;
const previous = readFileSync(target, 'utf8');
const from = previous.indexOf(start), to = previous.indexOf(end);
if (from < 0 || to < from) throw new Error('Request-answer word projection markers are missing');
const next = previous.slice(0, from) + generated + previous.slice(to + end.length);
if (process.argv.includes('--check')) {
  if (next !== previous) throw new Error('Run node tools/generate-request-answer-words.mjs from app/');
} else if (next !== previous) writeFileSync(target, next);
