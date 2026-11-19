// Every ./<name>.state.js is one state, found by name: export default { title, host, commands }.
//   host      the host_status snapshot, exactly as the host would send it;
//   commands  answers to the other commands the web view issues, each a value or a function of the arguments.
// Shapes follow the Rust host (app/src-tauri/src) and the front-end tests (app/tests); a state the
// App cannot reach misleads whoever looks at its picture.
const modules = import.meta.glob("./*.state.js", { eager: true });
export const states = Object.fromEntries(Object.entries(modules).map(([path, module]) => [path.slice(2, -".state.js".length), module.default]));
