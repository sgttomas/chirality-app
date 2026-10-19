import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import React from 'react';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {RunOffer} = loadSrc('RunOffers');
const nodes = (container,tag) => container.querySelectorAll(node => node.localName === tag);
const labelled = (container,label) => container.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const startButton = container => nodes(container,'button').find(node => /^(Start |End .+ and start )/.test(node.textContent));
const expectedStart = (offer,generation) => ['workflow_start_proposed',{
  generation,message:offer.message,runRef:offer.proposal.runInForce?.run ?? null,personText:'',proposalContext:offer.proposal.context,
}];
function freeze(value) {
  if (value && typeof value === 'object') {Object.values(value).forEach(freeze);Object.freeze(value);}
  return value;
}
let packet;
function actualPacket() {
  if (packet) return packet;
  let output;
  if (process.env.CHIRALITY_PROPOSED_RUN_DISCLOSURE_DTO_LOG) output = readFileSync(process.env.CHIRALITY_PROPOSED_RUN_DISCLOSURE_DTO_LOG,'utf8');
  else {
    const producer = 'runtime_session::workflow_root_tests::proposal_disclosure_tests::proposed_run_actual_candidate_report_dto_before_choice';
    const result = spawnSync('cargo',['test','--offline','--locked','--lib',producer,'--','--exact','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:12*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);output = result.stdout;
  }
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) > 0 && Number(summary[3]) === 0,'actual offline Rust producer checks completed successfully');
  assert.match(output,/test runtime_session::workflow_root_tests::proposal_disclosure_tests::proposed_run_actual_candidate_report_dto_before_choice/);
  const marker = 'PROPOSED_RUN_DISCLOSURE_DTO:';
  const captured = output.split('\n').filter(line => line.includes(marker)).map(line => JSON.parse(line.slice(line.indexOf(marker)+marker.length)));
  assert.equal(captured.length,1,'one actual Rust disclosure packet');
  assert.ok(captured[0].cases.length >= 2);
  packet = freeze(captured[0]);
  return packet;
}
async function mount(offer,generation,extra = {}) {
  const calls = [],container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  const render = async (nextOffer = offer,nextGeneration = generation,state = {}) => React.act(() => root.render(React.createElement(RunOffer,{
    offer:nextOffer,generation:nextGeneration,ready:true,busy:false,act:async (...args) => {calls.push(args);},...extra,...state,
  })));
  await render();
  return {container,calls,render,close:async () => {await React.act(() => root.unmount());document.body.removeChild(container);}};
}
function assertDisclosureBeforeStart(container) {
  const disclosure = labelled(container,'Proposed workflow compatibility'),button = startButton(container);
  assert.ok(disclosure);assert.ok(button);
  const siblings = button.parentNode.childNodes;
  assert.ok(siblings.indexOf(disclosure) < siblings.indexOf(button),'B’s advisory precedes the existing start/join button');
  return {disclosure,button};
}

test('actual Rust production offer DTO discloses the proposed B role, tools and basis before the inert ordinary Start choice',async () => {
  const source = actualPacket();
  assert.equal(source.standing,'production host_status history/thread/workflow composition; disclosure is read-only','final connection evidence must include the actual host_status history/workflow caller boundary');
  assert.ok(source.cases.some(sample => sample.offer.proposal.compatibility.preparation?.role.standing === 'unknown'));
  assert.ok(source.cases.some(sample => sample.offer.proposal.compatibility.preparation?.check.result === 'unsupported'));
  for (const sample of source.cases) {
    const {offer,generation} = sample,report = offer.proposal.compatibility,p = report.preparation;
    // Production host_status history/thread/workflow output from registered-snapshot,
    // Host-role and evaluator fixtures; no live supplier or native act.
    assert.equal(report.advisory,true);assert.equal(report.publication.state,'not published');
    assert.deepEqual(sample.rootBefore,sample.rootAfter,'disclosure changes no selection or run state');
    assert.deepEqual(offer.proposal.context.workflow,offer.proposal.resolution.workflow);
    assert.equal(offer.proposal.context.roleSupplyRef,p.role.supply_ref ?? null);
    const before = JSON.stringify(offer),view = await mount(offer,generation);
    try {
      const {disclosure,button} = assertDisclosureBeforeStart(view.container),text = disclosure.textContent;
      assert.ok(text.includes('CK-1 offered candidate'));assert.ok(text.includes('requirement check'));
      assert.ok(text.includes(report.statement));
      assert.ok(text.includes('never decides whether the run starts'));
      assert.ok(text.includes('Role in force:'));
      if (p.role.standing === 'unknown') {
        assert.ok(text.includes(`not established (${p.role.reason})`));
        assert.ok(!text.includes('this conversation has'),'unknown original role is not a deliberate no-role or mismatch');
      } else {
        assert.ok(text.includes(p.role.role));assert.ok(text.includes('The check does not pass for the role.'));
        assert.ok(text.includes('You may still start or continue the run.'));
        assert.ok(text.includes('use Continue as on the conversation'));
      }
      for (const requirement of p.requirements) {
        assert.ok(text.includes(requirement.name));assert.ok(text.includes(requirement.reason));assert.ok(text.includes(requirement.purpose));
      }
      for (const field of ['surface','acting_pin','conversation','home']) assert.ok(text.includes(p.basis[field]),field);
      assert.ok(text.includes(JSON.stringify(p.basis.generation)));
      assert.ok(text.includes(p.evaluated_at));
      assert.ok(text.includes('catalog edition not supplied'));assert.ok(text.includes('environment observation not supplied'));
      assert.ok(text.includes(report.inventoryOrigin.source));
      for (const limit of report.publication.factsNotSupplied) assert.ok(text.includes(limit),limit);
      assert.ok(text.includes(report.r14));assert.ok(text.includes('Publication: not published'));
      assert.equal(!!props(button).disabled,false,'unknown/nonpassing compatibility remains advisory');
      assert.deepEqual(view.calls,[],'rendering neither evaluates again nor selects, starts, sends or records');
      await React.act(() => props(button).onClick());
      assert.deepEqual(view.calls,[expectedStart(offer,generation)]);
      assert.equal(view.calls[0][1].proposalContext,offer.proposal.context,'echo the exact supplied context object');
      assert.equal(view.calls[0][1].generation,generation);
      assert.equal(view.calls[0][1].message,offer.message);
      assert.equal(JSON.stringify(offer),before,'display and press never rewrite the report or context');
    } finally {await view.close();}
  }
});

test('End A/start B shows B’s advisory before the join; End A alone keeps its original finished-report command',async () => {
  // UI-only lifecycle variants of the real evaluator packet; backend joined
  // lifecycle/freshness checks have their own Rust owner and evidence.
  for (const endCause of ['completed','changed']) {
    const sample = actualPacket().cases[1],offer = structuredClone(sample.offer);
    offer.proposal.runInForce = {run:'run:synthetic-A',workflow:'synthetic-A',endCause};
    offer.proposal.context.runRef = 'run:synthetic-A';
    offer.finished = {run:'run:synthetic-A',statement:'Workflow finished: project:synthetic-A'};
    freeze(offer);
    const view = await mount(offer,sample.generation);
    try {
      const {button} = assertDisclosureBeforeStart(view.container);
      assert.ok(button.textContent.startsWith('End synthetic-A and start '));
      assert.ok(view.container.textContent.includes(`ends with cause “${endCause}”`));
      assert.equal(nodes(view.container,'button').length,2,'no second confirmation or report action');
      assert.deepEqual(view.calls,[]);
      const endOnly = nodes(view.container,'button').find(node => node.textContent === 'End run');
      await React.act(() => props(endOnly).onClick());
      assert.deepEqual(view.calls,[['workflow_end_run',{runRef:'run:synthetic-A',finishedReport:offer.message}]]);
      await React.act(() => props(button).onClick());
      assert.deepEqual(view.calls[1],expectedStart(offer,sample.generation));
      assert.equal(view.calls[1][1].proposalContext,offer.proposal.context);
    } finally {await view.close();}
  }
});

test('passing, unknown, unsupported and preparation-error disclosures add no start gate; only original busy/ready conditions disable Start',async () => {
  const sample = actualPacket().cases[0];
  const reports = ['compatible','not_established','unsupported'].map(result => {
    const report = structuredClone(sample.offer.proposal.compatibility);
    report.preparation.check.result = result;report.statement = `Synthetic ${result} evaluator statement`;
    report.preparation.requirements = [
      ['present','present'],['present_currently_unavailable','present, currently unavailable'],['missing','missing'],['version_mismatch','version differs'],
      ['not_exposed_on_this_surface','not exposed on this surface'],['channel_not_enabled','channel not enabled'],['not_established','not established'],
    ].map(([outcome,words]) => ({name:`synthetic-${outcome}`,purpose:`Purpose of ${words}`,reason:`Reason for ${words}`,fallback:'Synthetic fallback',outcome}));
    return report;
  });
  reports.push({occasionLabel:'CK-1 offered candidate',preparation:null,limit:'Synthetic preparation failed: declaration unavailable',advisory:true});
  reports.push(undefined);
  for (const report of reports) {
    const offer = freeze({...sample.offer,proposal:{...sample.offer.proposal,compatibility:report}}),view = await mount(offer,sample.generation);
    try {
      const {disclosure,button} = assertDisclosureBeforeStart(view.container);
      assert.equal(!!props(button).disabled,false);
      assert.ok(disclosure.textContent.includes('never decides whether the run starts'));
      if (!report?.preparation) {
        assert.ok(disclosure.textContent.includes('no evaluation'));assert.ok(disclosure.textContent.includes('Evaluation basis not supplied'));
        if (report?.limit) assert.ok(disclosure.textContent.includes(report.limit));
      } else {
        for (const row of report.preparation.requirements) for (const value of [row.name,row.purpose,row.reason,row.fallback]) assert.ok(disclosure.textContent.includes(value));
      }
      for (const [busy,ready] of [[true,true],[false,false],[true,false],[false,true]]) {
        await view.render(offer,sample.generation,{busy,ready});
        assert.equal(!!props(startButton(view.container)).disabled,busy || !ready);
      }
      assert.deepEqual(view.calls,[],'no report state automatically starts or changes anything');
      await React.act(() => props(startButton(view.container)).onClick());
      assert.deepEqual(view.calls,[expectedStart(offer,sample.generation)],'report error/absence retains the given proposal context and original command');
      const during = freeze({...offer,proposal:{...offer.proposal,runInForce:{run:'run:synthetic-A',workflow:'synthetic-A',endCause:'changed'},context:{...offer.proposal.context,runRef:'run:synthetic-A'}}});
      await view.render(during,sample.generation);
      assert.equal(!!props(assertDisclosureBeforeStart(view.container).button).disabled,false,'the same advisory state leaves End A/start B available');
      assert.equal(view.calls.length,1,'joining is never automatic');
      await view.render(during,sample.generation,{busy:true,ready:true});assert.equal(props(startButton(view.container)).disabled,true);
      await view.render(during,sample.generation,{busy:false,ready:false});assert.equal(props(startButton(view.container)).disabled,true);
      await view.render(during,sample.generation);
      await React.act(() => props(startButton(view.container)).onClick());
      assert.deepEqual(view.calls[1],expectedStart(during,sample.generation));
    } finally {await view.close();}
  }
});

test('a retained callback echoes its original source, full generation, message, tuple, holding library and fixed-role basis after replacement',async () => {
  const sample = actualPacket().cases[1],original = sample.offer;
  const view = await mount(original,sample.generation);
  try {
    const retained = props(startButton(view.container)).onClick;
    const replacement = structuredClone(original),generation = {...sample.generation,spawnCounter:sample.generation.spawnCounter + 1,appSession:'synthetic-other-session',home:'synthetic-other-home'};
    replacement.message = {threadId:'synthetic-other-thread',turnId:'synthetic-other-turn',itemId:'synthetic-other-message'};
    replacement.proposal.context = {...replacement.proposal.context,sourceRef:'synthetic-other-source',home:generation.home,generation,message:replacement.message,
      libraryRef:'synthetic-other-library',holdingLibrary:'synthetic-other-holding',roleSupplyRef:'synthetic-other-role-supply',
      workflow:{...replacement.proposal.context.workflow,source_root:'synthetic-other-root',revision:'synthetic-other-full-revision'}};
    replacement.proposal.resolution.workflow = replacement.proposal.context.workflow;
    freeze(replacement);
    await view.render(replacement,generation);
    assert.deepEqual(view.calls,[]);
    await React.act(() => retained());
    assert.deepEqual(view.calls,[expectedStart(original,sample.generation)],'a stale press is not retargeted to the replacement; the backend checks freshness');
    assert.equal(view.calls[0][1].proposalContext,original.proposal.context);
    await React.act(() => props(startButton(view.container)).onClick());
    assert.deepEqual(view.calls[1],expectedStart(replacement,generation));
    assert.equal(view.calls[1][1].proposalContext,replacement.proposal.context);
    const withoutContext = {...replacement,proposal:{...replacement.proposal,context:undefined}};
    await view.render(withoutContext,generation);
    assert.equal(!!props(startButton(view.container)).disabled,false,'context absence invents no UI gate');
    await React.act(() => props(startButton(view.container)).onClick());
    assert.equal(view.calls[2][1].proposalContext,undefined,'missing context is never manufactured from current selection or role');
  } finally {await view.close();}
});

test('an earlier evaluation stays labelled not current and missing basis remains unknown; finished-only and unresolved offers gain no B disclosure',async () => {
  const sample = actualPacket().cases[0],offer = structuredClone(sample.offer),report = offer.proposal.compatibility;
  report.notCurrent = true;report.preparation.basis.catalog_edition = 'synthetic-earlier-catalog';report.preparation.basis.environment_observation = 'synthetic-earlier-environment';
  report.preparation.requirements[0].purpose = '<script>do not execute</script>\nLiteral purpose';
  const view = await mount(freeze(offer),sample.generation);
  try {
    const disclosure = labelled(view.container,'Proposed workflow compatibility');
    assert.ok(disclosure.textContent.includes('evaluated on an earlier basis, so it is not current'));
    assert.ok(disclosure.textContent.includes('catalog edition synthetic-earlier-catalog'));
    assert.ok(disclosure.textContent.includes('environment observation synthetic-earlier-environment'));
    assert.ok(disclosure.textContent.includes(report.preparation.requirements[0].purpose));assert.equal(nodes(view.container,'script').length,0);
    assert.equal(!!props(startButton(view.container)).disabled,false);
    const unknownBasis = structuredClone(offer);delete unknownBasis.proposal.compatibility.preparation.basis;
    await view.render(unknownBasis,sample.generation);
    assert.ok(view.container.textContent.includes('surface not supplied; acting pin not supplied; catalog edition not supplied; environment observation not supplied'));
    await view.render({message:offer.message,finished:{run:'run:synthetic-A',statement:'Workflow finished: project:synthetic-A'}},sample.generation);
    assert.equal(labelled(view.container,'Proposed workflow compatibility'),undefined);
    assert.deepEqual(nodes(view.container,'button').map(node => node.textContent),['End run']);
    await view.render({...offer,proposal:{...offer.proposal,resolution:{workflow:null,notice:'Synthetic unresolved candidate'}}},sample.generation);
    assert.equal(labelled(view.container,'Proposed workflow compatibility'),undefined);
    assert.equal(nodes(view.container,'button').length,0);assert.ok(view.container.textContent.includes('Synthetic unresolved candidate'));
    assert.deepEqual(view.calls,[]);
  } finally {await view.close();}
});
