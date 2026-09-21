export const PRODUCT_INSTRUCTIONS_CHANNEL = 'chirality:product-instructions';

export type ProductInstructionsState = {
  path: string;
  modified: boolean;
};

export type ProductInstructionsOperation = 'get' | 'open' | 'restore';
export type ProductInstructionsResult =
  | { ok: true; state: ProductInstructionsState; cancelled?: boolean }
  | { ok: false; error: string };
