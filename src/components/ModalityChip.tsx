'use client';

interface ModalityChipProps {
  modality: string;
}

export function ModalityChip({ modality }: ModalityChipProps) {
  const getModalityStyles = (modality: string) => {
    switch (modality.toLowerCase()) {
      case 'problem':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'systematic':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'process':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'epistemic':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'alethic':
        return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'resolution':
        return 'bg-indigo-100 text-indigo-800 border-indigo-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <span className={`
      inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border
      ${getModalityStyles(modality)}
    `}>
      {modality.charAt(0).toUpperCase() + modality.slice(1)}
    </span>
  );
}