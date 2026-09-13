# Chirality App

**Plan your work. Iterate.**

Meet Help Human, the assistant inside Chirality App. Bring a complex task, work through it together, and turn a useful plan into a workflow you can reuse and adapt.

**[Download Chirality App](https://github.com/sgttomas/chirality-app/releases/latest)** · [Website](https://chirality.ai/app) · [Report an issue](https://github.com/sgttomas/chirality-app/issues/new/choose)

## Get started

Version **3.0.0** is available for **Apple Silicon Macs running macOS 15 or newer**. It uses Codex through your ChatGPT account. Local-model support is planned for a later release.

1. Download the `.dmg` from the [latest release](https://github.com/sgttomas/chirality-app/releases/latest).
2. Open it and drag Chirality to Applications. The release is signed and notarized.
3. Open Chirality, sign in with your ChatGPT account, and choose a working folder.
4. Tell Help Human what you want to accomplish.

A conversation is enough to begin. Use Plan Mode when planning helps, select a workflow from the library, or ask Help Human to turn your plan into one. Come back to the conversation to continue, reuse, and refine your work.

## Your work

Prepare a monthly update, organize references, investigate a question, or review a document. You direct the work and decide when the result is ready.

Saved plans, workflows, references, and outputs are ordinary files in your folders. Plans stay in conversation history unless you choose to save them to a file. You can use them outside Chirality. Model processing sends the content needed for the task to OpenAI using your account; Chirality AI Ltd does not proxy or retain that content. Read more about [installation and data handling](https://chirality.ai/deployment).

## Updates and support

The App checks for updates automatically and shows when a newer release is available. Downloading and installing the update remains your choice. You can also check manually in the App.

Use **Report issue** in the App or [open a GitHub issue](https://github.com/sgttomas/chirality-app/issues/new/choose). Include the App version, what you expected, and what happened. Share only information you are comfortable making public.

## Source and development

This repository is the curated Chirality desktop release projection, hosting public installers, release notes, and user issue reports. The desktop application source is not currently included here. Current application and instruction development takes place in **[sgttomas/chirality](https://github.com/sgttomas/chirality)**. Retained folders such as `runtime/` are source snapshots, separate from the versioned installers; use the main repository for current source and build instructions.

- [App source and development setup](https://github.com/sgttomas/chirality#develop-and-contribute)
- [Roles and instructions](https://github.com/sgttomas/chirality/tree/main/agents)
- [Workflow library](https://github.com/sgttomas/chirality/tree/main/workflows)
- [Release notes](https://github.com/sgttomas/chirality-app/releases)

## License

Chirality App is free and open source under the [MIT License](https://github.com/sgttomas/chirality/blob/main/LICENSE.md). Bundled dependencies and older source snapshots retain their own licence notices. Copyright © 2026 Ryan Tufts.
