'use client';

import React, { type ReactNode } from 'react';

/** The primary controller has one stable, always-visible mount. */
export function DialogueViewport({ primaryDialogue }: { primaryDialogue: ReactNode }): JSX.Element {
  return (
    <div className="woven-primary-dialogue" data-primary-dialogue-mounted="true">
      {primaryDialogue}
    </div>
  );
}
