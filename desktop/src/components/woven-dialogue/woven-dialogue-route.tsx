'use client';

import React, { type ReactNode } from 'react';
import type { WovenSurface } from './navigator';
import { WovenDialogueShell } from './woven-dialogue-shell';

type WovenDialogueRouteProps = {
  defaultSurface: WovenSurface;
  legacy: ReactNode;
};

export function WovenDialogueRoute({
  defaultSurface,
  legacy
}: WovenDialogueRouteProps): JSX.Element {
  // Keep the legacy element in the route contract while old callers migrate,
  // but every route now enters the same continuing conversation surface.
  void legacy;
  return <WovenDialogueShell defaultSurface={defaultSurface} />;
}
