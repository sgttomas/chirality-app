import { NextRequest, NextResponse } from "next/server";
import cfg from "@/config/selection.json";
import { selectForMirror } from "@/lib/graph/selector";

export async function POST(req: NextRequest) {
  // Gate behind feature flag
  if (process.env.FEATURE_GRAPH_ENABLED !== "true") {
    return NextResponse.json(
      { error: "Graph features are not enabled" },
      { status: 503 }
    );
  }
  const { bundle } = await req.json(); // supply a bundle (DS/SP/X/M + sections/raw)
  const sel = selectForMirror(bundle, cfg as any);
  return NextResponse.json({
    docs: sel.docs.map((d: any) => d.id),
    keepByDoc: sel.keepByDoc,
    components: sel.components.map((c: any) => ({ id: c.id, docId: c.docId }))
  });
}