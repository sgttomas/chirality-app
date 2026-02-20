"use client";

import React, { useState, useEffect, useCallback, useRef } from "react";

interface ResizerProps {
  onResize: (delta: number) => void;
}

export function Resizer({ onResize }: ResizerProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
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

  useEffect(() => {
    if (!isDragging) return;

    const previousCursor = document.body.style.cursor;
    const previousUserSelect = document.body.style.userSelect;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";

    return () => {
      document.body.style.cursor = previousCursor;
      document.body.style.userSelect = previousUserSelect;
    };
  }, [isDragging]);

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
      title="Drag to resize panels"
      className={`resizer-handle ui-focus-ring touch-none ${isDragging ? "active" : ""} ${isHovered ? "hovered" : ""}`}
      onPointerDown={startDragging}
      onKeyDown={handleKeyResize}
      onPointerEnter={() => setIsHovered(true)}
      onPointerLeave={() => setIsHovered(false)}
    >
      <div className="resizer-grip" aria-hidden>
        <span className="resizer-grip-dot" />
        <span className="resizer-grip-dot" />
        <span className="resizer-grip-dot" />
      </div>
      <span className="resizer-hint">DRAG</span>
    </div>
  );
}
