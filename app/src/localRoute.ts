// DEL-01-05 "For 4.0.0" (LIM-015): this version of the App does not offer a
// local model server or a local provider. The route's views and code are kept
// for a later update; every place that would offer it is gated on this, and
// the host refuses each of its commands with the same words
// (lib.rs LOCAL_ROUTE_NOT_OFFERED).
export const LOCAL_ROUTE_OFFERED: boolean = false;
export const LOCAL_ROUTE_NOT_OFFERED = "This version of the App does not offer a local model server or a local provider. Use your ChatGPT account: sign in under Connection and access.";
