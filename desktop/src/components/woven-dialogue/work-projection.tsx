import React from 'react';
import type { CoordinationWorkItem } from '../../lib/woven-dialogue/contracts';

export const WORK_PROJECTION_EMPTY_STATE = 'No structured plan recorded.';

type WorkProjectionProps = {
  items: readonly CoordinationWorkItem[];
};

function recordedValue(value: string | undefined): string {
  return value?.trim() || 'Not recorded';
}

export function WorkProjection({ items }: WorkProjectionProps): JSX.Element {
  return (
    <section aria-labelledby="woven-work-projection-heading" data-projection="work">
      <header>
        <h2 id="woven-work-projection-heading">Work</h2>
        <p>
          Evidence-only projection. Controlling status and authority remain with each
          recorded source.
        </p>
      </header>

      {items.length === 0 ? (
        <p role="status">{WORK_PROJECTION_EMPTY_STATE}</p>
      ) : (
        <ol aria-label="Recorded work items">
          {items.map((item) => (
            <li
              key={item.id}
              data-currency={item.currency}
              data-work-class={item.workClass}
            >
              <article>
                <h3>{item.title}</h3>
                <dl>
                  <div>
                    <dt>Work class</dt>
                    <dd>
                      <code>{item.workClass}</code>
                    </dd>
                  </div>
                  <div>
                    <dt>Source reference</dt>
                    <dd>
                      <code>{recordedValue(item.sourceReference)}</code>
                    </dd>
                  </div>
                  <div>
                    <dt>Status basis</dt>
                    <dd>{recordedValue(item.statusBasis)}</dd>
                  </div>
                  <div>
                    <dt>Currency</dt>
                    <dd>
                      <code>{item.currency}</code>
                    </dd>
                  </div>
                  <div>
                    <dt>Recorded status</dt>
                    <dd>{recordedValue(item.statusLabel)}</dd>
                  </div>
                  <div>
                    <dt>Responsible reference</dt>
                    <dd>{recordedValue(item.responsibleReference)}</dd>
                  </div>
                  <div>
                    <dt>Runtime status</dt>
                    <dd>{recordedValue(item.runtimeStatus)}</dd>
                  </div>
                  <div>
                    <dt>Project lifecycle status</dt>
                    <dd>{recordedValue(item.lifecycleStatus)}</dd>
                  </div>
                </dl>

                <section aria-label={`Related references for ${item.title}`}>
                  <h4>Related references</h4>
                  {item.relatedReferences.length === 0 ? (
                    <p>Not recorded</p>
                  ) : (
                    <ul>
                      {item.relatedReferences.map((reference) => (
                        <li key={reference}>
                          <code>{reference}</code>
                        </li>
                      ))}
                    </ul>
                  )}
                </section>
              </article>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
