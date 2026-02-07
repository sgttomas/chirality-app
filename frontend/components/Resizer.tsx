"use client";

import React, { useState, useEffect, useCallback } from "react";

interface ResizerProps {
  onResize: (delta: number) => void;
}

export function Resizer({ onResize }: ResizerProps) {
  const [isDragging, setIsDragging] = useState(false);

  const startDragging = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  useEffect(() => {
    if (!isDragging) return;

    const handleMouseMove = (e: MouseEvent) => {
      onResize(e.movementX);
    };

    const stopDragging = () => {
      setIsDragging(false);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", stopDragging);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", stopDragging);
    };
  }, [isDragging, onResize]);

  return (
    <div 
      className={`resizer-handle ${isDragging ? "active" : ""}`} 
      onMouseDown={startDragging}
    >
        <div className={`w-[2px] h-full transition-colors ${isDragging ? 'bg-[var(--color-accent-orange)]' : 'bg-transparent group-hover:bg-[var(--color-accent-orange)]'}`}></div>
    </div>
  );
}
