// The Chirality App over what the real engine emitted from recorded Codex sessions.
import { act, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";

import { createEngineClient, describeError, Store } from "@chirality/engine-ui";
import { engineData, mount, ReplayTransport, settle, testHost } from "@chirality/engine-ui/testing";
import { render } from "@testing-library/react";

import { App, Root } from "./App";

const signedIn = (name: string) => new ReplayTransport(engineData(name), (s) => ({ ...s, account: { state: "signedIn", email: "person@example.com", plan: null } }));

/** Mounts the app over a recording and follows its first thread from its start. */
async function open(name: string) {
  const engine = signedIn(name);
  const mounted = await mount(engine.client, <App />);
  const first = await act(async () => engine.play((e) => e.type === "thread"));
  if (first?.type !== "thread") throw new Error("no thread");
  await act(() => mounted.store.selectThread(first.thread.id));
  await settle();
  return { engine, ...mounted };
}

beforeEach(() => localStorage.clear());

describe("the Chirality App", () => {
  it("starts with first use while signed out", async () => {
    await mount(new ReplayTransport(engineData("text_turn")).client, <App />);
    expect(screen.getByRole("heading", { name: "Chirality" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Sign in" })).toBeInTheDocument();
  });

  it("shows the navigator, the conversation and the side panel with the thread's change", async () => {
    const { engine } = await open("file_change");
    await act(async () => void engine.play((e) => e.type === "pending"));
    await settle();
    await userEvent.click(within(screen.getByRole("dialog", { name: "Make these changes?" })).getByRole("button", { name: "Allow" }));
    await act(async () => void engine.play());
    await settle();
    expect(screen.getByRole("navigation", { name: "Projects" })).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: /hello\.txt/ }));
    const panel = screen.getByRole("complementary", { name: "Side panel" });
    expect(within(panel).getAllByRole("tab").map((t) => t.textContent)).toEqual(["Changes1", "Workflow", "Preview"]);
    await userEvent.click(within(panel).getByRole("tab", { name: "Preview" }));
    await settle();
    expect(within(panel).getByText("hello")).toBeInTheDocument();
  });

  it("shows the workflow a message carried", async () => {
    const { engine } = await open("workflow_turn");
    await act(async () => void engine.play());
    await settle();
    expect(screen.getByText("estimate")).toBeInTheDocument();
  });

  it("shows why it could not start, when the engine could not", async () => {
    const refused = { kind: "codexUnavailable", message: "No such file or directory (os error 2)" };
    const client = createEngineClient({ invoke: () => Promise.reject(refused), listen: async () => () => {} });
    const store = new Store(client, testHost);
    render(<Root store={store} started={store.start().then(() => null, describeError)} />);
    await settle();
    const alert = screen.getByRole("alert");
    expect(within(alert).getByRole("heading", { name: "Chirality couldn't start" })).toBeInTheDocument();
    expect(alert).toHaveTextContent("Codex isn't running: No such file or directory (os error 2)");
  });
});
