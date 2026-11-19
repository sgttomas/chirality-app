# Front-end preview with a stand-in host

Development tooling for looking at the App's views without running the App: Vite serves the real
`app/src` and `preview.js` answers the web view's host commands from one constructed state. No App,
candidate bundle or Codex binary runs, and nothing here is in the product build (`app/index.html`
is the build's only entry).

From `app/`, with dependencies installed offline (`app/README.md`, Offline build and checks):

```sh
npx --offline vite --config examination/visual_preview/vite.config.mjs
```

then open `http://127.0.0.1:14207/examination/visual_preview/index.html?state=<name>`. Each state is
a file `states/<name>.state.js`; `window.__PREVIEW__.unanswered` lists commands the page issued that
the state does not answer.

A picture from here shows the form of a view, not the App working: the states are constructed from
the host's types and the front-end tests, not captured from a run. It is not evidence for any
criterion.
