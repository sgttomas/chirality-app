"""CC-REC-ATTACHMENT-PROJECT-CONTEXT scripted source controls only.
No native capability/private Root proof is established by these Python values.
"""
import copy
import json

NIR_OWNER = "DEL-01-04"
EXPLICIT_SOURCES = {"configured App directory", "opened App directory"}


def explicit_project(reference, source):
    if source not in EXPLICIT_SOURCES or not isinstance(reference, str) or not reference:
        raise ValueError("Root explicit App directory reference required; no inferred/default project")
    reference.encode("utf-8", "strict")
    return reference


def encode_context(submission, project):
    if not isinstance(submission, str) or not submission.startswith("submission:") or len(submission)==len("submission:"):
        raise ValueError("owning App submission token required")
    if project is not None and (not isinstance(project, str) or not project):
        raise ValueError("explicit nonempty App reference or absence only")
    value=json.dumps([submission,project], ensure_ascii=False,separators=(",", ":"))
    value.encode("utf-8","strict")
    return value


def decode_context(owner, value):
    if owner!=NIR_OWNER:
        raise ValueError("not NIR's context tag")
    pair=json.loads(value)
    if not isinstance(pair,list) or len(pair)!=2 or encode_context(*pair)!=value:
        raise ValueError("not the exact compact context codec")
    return tuple(pair)


def resolve_context(tags, submission):
    """Only owning recognized values count; unknown tags are preserved by REC."""
    bindings=[]
    for tag in tags:
        try:
            token,project=decode_context(tag["owner"],tag["value"])
        except (ValueError,TypeError,KeyError,json.JSONDecodeError):
            continue
        if token==submission:
            bindings.append(project)
    if not bindings:
        return {"status":"not recorded","project":None}
    if any(project!=bindings[0] for project in bindings):
        return {"status":"ambiguous","project":None,"claims":bindings}
    return {"status":"bound recorded context","project":bindings[0]}


def bind_context(index, submission, current_project, memory_tags=()):
    """Known index stays P. Caller supplies hot tags when unknown index has no row.
    Neither resolution nor these scripted values hydrate a Root/native capability.
    """
    value=encode_context(submission,current_project)
    historical=index.get("project") if index else None
    if historical is not None and (not isinstance(historical,str) or not historical):
        raise ValueError("0.2 index must have its actual nonempty known project")
    # REC4.1 failed persistence can leave hot tags beside a known durable index.
    # Both sources constrain the same immutable submission; neither is a fallback.
    tags=list(index["tags"]) if index else []
    for hot in memory_tags:
        if hot not in tags:
            tags.append(hot)
    prior=resolve_context(tags,submission)
    if prior["status"]=="ambiguous" or (prior["status"]=="bound recorded context" and prior["project"]!=current_project):
        raise ValueError("immutable submission context conflicts; no retag/transfer")
    relation="unbound" if historical is None or current_project is None else ("same" if historical==current_project else "different; no transfer")
    tag={"owner":NIR_OWNER,"value":value,"seq":max((t["seq"] for t in tags),default=0)+1}
    output=copy.deepcopy(index) if historical else None
    if prior["status"]=="bound recorded context":
        tag=next(copy.deepcopy(t) for t in tags if t["owner"]==NIR_OWNER and t["value"]==value)
    elif output is not None:
        output["tags"].append(tag)
    limit=None if output is not None else "project index absent: no row, context tag memory-only; cold lookup unavailable"
    if output is not None and prior["status"]=="bound recorded context" and not any(t["owner"]==NIR_OWNER and t["value"]==value for t in output["tags"]):
        limit="known project index lacks this hot binding: tag memory-only; cold lookup unavailable"
    return {"historicalProject":historical,"currentSubmissionProject":current_project,
            "relation":relation,"indexSnapshot":output,"tag":tag,
            "idempotent":prior["status"]=="bound recorded context","limit":limit}
