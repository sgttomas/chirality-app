"use client";

import React, { useState, useEffect, useCallback, useRef } from "react";

interface ResizerProps {
  onResize: (delta: number) => void;
}

export function Resizer({ onResize }: ResizerProps) {
  const [isDragging, setIsDragging] = useState(false);
  const lastPointerX = useRef<number | null>(null);

  const startDragging = useCallback((e: React.PointerEvent<HTMLDivElement>) => {
    e.preventDefault();
    lastPointerX.current = e.clientX;
    setIsDragging(true);
    e.currentTarget.setPointerCapture(e.pointerId);
  }, []);

  useEffect(() => {
    if (!isDragging) return;

    const handlePointerMove = (e: PointerEvent) => {
      const previousX = lastPointerX.current;
      if (previousX === null) {
        lastPointerX.current = e.clientX;
        return;
      }
      const delta = e.clientX - previousX;
      lastPointerX.current = e.clientX;
      if (delta !== 0) {
        onResize(delta);
      }
    };

    const stopDragging = () => {
      lastPointerX.current = null;
      setIsDragging(false);
    };

    window.addEventListener("pointermove", handlePointerMove);
    window.addEventListener("pointerup", stopDragging);
    window.addEventListener("pointercancel", stopDragging);

    return () => {
      window.removeEventListener("pointermove", handlePointerMove);
      window.removeEventListener("pointerup", stopDragging);
      window.removeEventListener("pointercancel", stopDragging);
    };
  }, [isDragging, onResize]);

  const handleKeyResize = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      onResize(-24);
      return;
    }
    if (e.key === "ArrowRight") {
      e.preventDefault();
      onResize(24);
    }
  };

  return (
    <div
      role="separator"
      aria-orientation="vertical"
      aria-label="Resize panels"
      tabIndex={0}
      className={`resizer-handle ui-focus-ring touch-none ${isDragging ? "active" : ""}`}
      onPointerDown={startDragging}
      onKeyDown={handleKeyResize}
    >
      <div
        className={`h-full w-[2px] transition-colors ${
          isDragging ? "bg-[var(--color-accent-orange)]" : "bg-transparent"
        }`}
      />
    </div>
  );
}
