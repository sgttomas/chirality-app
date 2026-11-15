#!/usr/bin/env python3
"""Three separately gated, no-model observations for the 0.169.0 delegation rule.

No execution on import. The loopback provider returns fixed text and requests no
tool. Only its received tools declaration is retained, never the turn body or
header values. Supplier contacts are not observed; proxies are not isolation.
This is supplier evidence, not App behavior or candidate qualification.
"""
import argparse
import copy
import json
from pathlib import Path
import signal
import subprocess

import intake
import record_at_pin as capture
import recording_provider as provider
import same_basis

CASES = ("baseline", "agents-disabled", "catalog-disabled")
MODEL = "delegation-observation-model"
SECONDS = 180


def catalog(case):
    """Invented ModelInfo; required fields read at supplier d32063f9, not a real model."""
    model = {
        "slug": MODEL, "display_name": "Invented delegation observation",
        "description": "Fixed text loopback fixture", "supported_reasoning_levels": [],
        "shell_type": "unified_exec", "visibility": "list", "supported_in_api": True,
        "priority": 1, "support_verbosity": False,
        # ModelsResponse's custom deserializer requires a canonical template or
        # legacy base_instructions, although ModelInfo alone makes both optional.
        "model_messages": {"instructions_template": "Reply with invented observation text. Request no tool."},
        "truncation_policy": {"mode": "bytes", "limit": 10000},
        "experimental_supported_tools": [],
    }
    if case == "catalog-disabled":
        model["multi_agent_version"] = "disabled"
    return {"models": [model]}


def configuration(root, case, port):
    capture.require(case in CASES, "unknown observation case")
    text = (
        f'model_provider = "observation_stub"\nmodel = "{MODEL}"\n'
        f'model_catalog_json = {json.dumps(str(root / "catalog.json"))}\n'
        'approval_policy = "never"\nsandbox_mode = "read-only"\n'
        'allow_login_shell = false\n'
        f'[model_providers.observation_stub]\nname = "Invented loopback provider"\n'
        f'base_url = "http://127.0.0.1:{port}/v1"\nwire_api = "responses"\n'
        '[features]\nplugins = false\nshell_snapshot = false\n'
        '[analytics]\nenabled = false\n'
    )
    if case == "agents-disabled":
        text += '[agents]\nenabled = false\n'
    return text


def response_plan(declarations):
    def plan(index, body):
        capture.require(index == 1 and not declarations, "more than one provider turn request")
        capture.require(isinstance(body, dict) and isinstance(body.get("tools"), list),
                        "provider request has no tools declaration")
        declarations.append(copy.deepcopy(body["tools"]))
        return [provider.message("Invented observation complete.", "msg_observation")], 0, "fixed text; no tool requested"
    return plan


def retain_refusal(run, case, error):
    """Keep already-received frames privately; no new request or inspection."""
    def withheld(value):
        if isinstance(value, dict):
            return {key: ("<WITHHELD>" if key in {"userId", "accountId", "userAgent", "apiKey", "accessToken",
                         "refreshToken", "idToken", "loginId", "userCode", "authUrl", "verificationUrl"}
                         else withheld(item)) for key, item in value.items()}
        if isinstance(value, list):
            return [withheld(item) for item in value]
        return value
    with (run.root / "refusal.json").open("x") as handle:
        json.dump({"case": case, "refusal": str(error), "frames": withheld(run.frames),
                   "limits": "Already-received frames only; no completed observation or inferred cause."}, handle, indent=2)
        handle.write("\n")


def check_observation(case, reads, declarations):
    capture.require(len(declarations) == 1, "one tools declaration required")
    models = reads["model/list"]
    capture.require(models.get("nextCursor") is None, "partial model list")
    entries = [v for v in models["data"] if v.get("model") == MODEL]
    capture.require(len(entries) == 1, "invented model not uniquely listed")
    expected = "disabled" if case == "catalog-disabled" else None
    capture.require(entries[0].get("multiAgentVersion") == expected, "catalogue version differs")
    config = reads["config/read"]
    capture.require(isinstance(config.get("layers"), list), "configuration layers not returned")
    capture.require(isinstance(reads["configRequirements/read"], dict)
                    and "requirements" in reads["configRequirements/read"], "requirements not returned")
    requirements = reads["configRequirements/read"]["requirements"]
    capture.require(requirements is None or isinstance(requirements, dict), "requirements malformed")
    constraints = (requirements or {}).get("featureRequirements") or {}
    capture.require(isinstance(constraints, dict) and not constraints,
                    "managed feature requirement present; this route does not test one")
    for layer in config["layers"]:
        capture.require(isinstance(layer, dict) and isinstance(layer.get("config"), dict),
                        "configuration layer incomplete")
        features = layer["config"].get("features") or {}
        agents = layer["config"].get("agents") or {}
        capture.require(isinstance(features, dict) and isinstance(agents, dict), "configuration table malformed")
        capture.require("multi_agent" not in features and "multi_agent_v2" not in features,
                        "unexpected delegation feature in a configuration layer")
        capture.require("enabled" not in agents or (case == "agents-disabled" and agents["enabled"] is False),
                        "unexpected agents.enabled in a configuration layer")
    effective = config.get("config")
    capture.require(isinstance(effective, dict), "effective configuration not returned")
    agents = effective.get("agents") or {}
    features = effective.get("features") or {}
    capture.require(isinstance(agents, dict) and isinstance(features, dict), "effective tables malformed")
    capture.require(agents.get("enabled") is (False if case == "agents-disabled" else None),
                    "agents.enabled read differs from the supplied case")
    capture.require(features.get("multi_agent") is None and features.get("multi_agent_v2") is None,
                    "effective delegation feature differs from the supplied case")
    native = [name for _namespace, name in capture.names({"tools": declarations[0]})
              if name in {"spawn_agent", "send_input", "wait_agent", "resume_agent", "close_agent",
                          "send_message", "followup_task", "interrupt_agent", "list_agents"}]
    capture.require(("spawn_agent" in native) if case == "baseline" else not native,
                    "native tools differ from the proposed rule")
    return native


def observe(vendor, record, root, case, port):
    declarations = []
    # Run's constructor creates fresh homes, checks the vendor and outside config,
    # and binds a loopback listener. It does not execute the supplier.
    run = capture.Run(vendor, record, root, "nv04", port)
    try:
        run.provider.plan = response_plan(declarations)
        (run.root / "catalog.json").write_text(json.dumps(catalog(case)) + "\n")
        (run.root / "home/config.toml").write_text(configuration(run.root, case, port))
        pipe = capture.Pipe(run, 1)  # one app-server start; no version/help probe
        pipe.initialize()
        reads = {
            "config/read": pipe.request("config/read", {"cwd": str(run.work), "includeLayers": True}),
            "configRequirements/read": pipe.request("configRequirements/read", {}),
            "model/list": pipe.request("model/list", {"includeHidden": True}),
        }
        reads["thread/start"] = pipe.request("thread/start", {"cwd": str(run.work), "approvalPolicy": "never",
                                                            "sandbox": "read-only"})
        thread = reads["thread/start"]["thread"]["id"]
        turn = pipe.request("turn/start", {"threadId": thread, "input": [
            {"type": "text", "text": "Reply with the invented observation text. Request no tool."}]})["turn"]["id"]
        done = pipe.until(lambda: next((frame for frame in pipe.received
            if frame.get("method") == "turn/completed" and frame["params"].get("threadId") == thread
            and frame["params"]["turn"].get("id") == turn), None))
        capture.require(done["params"]["turn"].get("status") == "completed", "turn did not complete")
        capture.require(not any("method" in f and "id" in f for f in pipe.received),
                        "unexpected supplier request; no response supplied")
        pipe.end()
        native = check_observation(case, reads, declarations)
        # Private evidence only: reads include exclusively invented scratch paths.
        result = {"case": case, "pin": record["pin"], "binary_sha256": intake.sha256_file(run.binary),
                  "configuration_supplied": configuration(run.root, case, port), "catalog": catalog(case),
                  "reads": reads, "tools": declarations[0], "native_tool_names": native,
                  "provider_requests": run.provider_log,
                  "limits": ["No model, tool call, sign-in, account read or contact observation.",
                             "Proxy settings are not isolation; an ignoring binary could contact other hosts.",
                             "One root conversation per case; no descendant or override observation.",
                             "Not App behavior, capacity evidence or candidate qualification."]}
    except Exception as error:
        retain_refusal(run, case, error)
        raise
    finally:
        run.close()
    with (run.root / "observation.json").open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    return {"case": case, "native_tool_names": native,
            "sha256": intake.sha256_file(run.root / "observation.json")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vendor", required=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--case", choices=CASES, help="Run only this case when the route gate permits it")
    args = parser.parse_args()
    record = same_basis.admit_distribution("0.169.0", Path(args.record).read_bytes())
    root = Path(args.root)
    capture.require(root.is_absolute() and root.resolve() == root, "root must be a plain absolute path")
    root.mkdir(mode=0o700)  # never reuse any run root
    def deadline(_signum, _frame):
        raise capture.Refused("case exceeded 180 seconds")
    previous = signal.signal(signal.SIGALRM, deadline)
    try:
        for case in ((args.case,) if args.case else CASES):
            signal.alarm(SECONDS)
            try:
                result = observe(args.vendor, record, root / case, case, args.port)
            finally:
                signal.alarm(0)
            print(json.dumps(result), flush=True)
    finally:
        signal.signal(signal.SIGALRM, previous)


if __name__ == "__main__":
    try:
        main()
    except (capture.Refused, intake.Refused, same_basis.Refused, OSError, ValueError, KeyError,
            subprocess.TimeoutExpired) as error:
        raise SystemExit("delegation observation refused: " + str(error)) from None
