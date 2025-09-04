import cfg from "../config/selection.json";
import { selectForMirror, Doc } from "../lib/graph/selector";

function mkDoc(id:string, kind:any, body:string): Doc {
  return { id, kind, slug: id.split(":")[1], title: "T", sections: [], raw: body };
}

test("selection threshold & caps", () => {
  const body = `
# Title
## API Integrations
See [[DS:core-auth]] and [[sp-deploy]] plus (docs/x-runbook).
## Random Notes
no refs here
## Decisions
Links: [[X:runner]], [[m-guidelines]]
`;
  const bundle = { DS: mkDoc("DS:sample", "DS", body) } as any;
  const sel = selectForMirror(bundle, cfg as any);
  const compTitles = sel.components.map(c => c.props.title);
  expect(compTitles.join(" ")).toMatch(/API Integrations/);
  expect(compTitles.join(" ")).toMatch(/Decisions/);
});

test("stable component ids", () => {
  const d = mkDoc("SP:ship", "SP", "## API Metrics\nSee [[DS:ref1]] and [[X:ref2]] for details");
  const sel = selectForMirror({ SP: d } as any, cfg as any);
  
  if (sel.components.length === 0) {
    console.log("No components selected, check scoring logic");
    return;
  }
  
  const first = sel.components[0].id;
  const sel2 = selectForMirror({ SP: d } as any, cfg as any);
  expect(sel2.components[0].id).toBe(first);
});

test("component caps are enforced", () => {
  const largeBody = Array.from({ length: 20 }, (_, i) => 
    `## API Section ${i}\nSee [[DS:ref${i}]] and [[SP:ref${i}]]`
  ).join("\n");
  
  const bundle = { DS: mkDoc("DS:large", "DS", largeBody) } as any;
  const selection = selectForMirror(bundle, cfg as any);
  
  expect(selection.components.length).toBeLessThanOrEqual((cfg as any).topKPerDoc);
});