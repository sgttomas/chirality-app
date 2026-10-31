# Offline AX representation audit after the owned-window diagnostic

Scope: retained ctypes reader sources and the actual raw observations from
[the am98hzma attempt](NATIVE_B_DIAGNOSTIC_20261031.md). No App or AX service was
queried for this audit, no permission changed, and no runtime source was edited.
The App candidate remains fdcf608f; source tests are not actual GUI qualification.

## ABI, conversion and references

The local macOS SDK declares AXUIElementCopyAttributeValue as returning AXError
with a retained CFTypeRef output pointer; AXError/pid_t are32-bit, CFIndex is
signed long and CFTypeID unsigned long on this arm64 host. The diagnostic uses
c_int, POINTER(c_void_p), c_long, c_ulong and c_void_p accordingly. CFArray count
and index access use CFIndex and return const void*. AX timeout takes float;
the corrected diagnostic sets it on every element before remote reads, since
the header says a timeout applies only to that object, not other equal objects.
CFEqual is explicitly supported for AXUIElementRefs. Boolean and pointer widths
match the actual arm64 API; no concrete truncation/out-pointer mismatch was found.

Both readers use dynamically queried CF type IDs rather than assuming that
75 always means AXUIElement. The raw diagnostic observed array19, AXUIElement75
and string7, with success0 from the relevant calls. It retained raw type/result
information, then read role from the owned returned reference. The self-reference
is therefore not merely a title heuristic or a traversal-cycle side effect.
The new reader does not recursively traverse AXChildren; the older wrapper's
pruning happens after it observes the returned object's role and CFEqual result.

The original controller's attribute copies are never CFReleased during the
walk: this leaks copies for its bounded process lifetime, but does not expose
an early-release explanation. Array elements are borrowed from the still-owned
copied array. The diagnostic instead tracks every Create/Copy reference in
`held`, uses borrowed children only while their parent array is retained, and
releases owned copies after the capture. No returned pointer is decoded after
that close. Neither reader converts an AX reference through a32-bit integer.
The actual capture does not retain raw pointer addresses, so it cannot say
whether equal remote references shared the same local address. CFEqual plus
the observed AXRole is the supported claim.

## Harmless concrete conversion fixture

A tiny compiled C/CoreFoundation fixture returned known distinct application-
label/window-label/menu-label CFString objects through a CFTypeRef output
pointer and a retained CFArray, including a duplicate window reference. The
Python test used the diagnostic's actual `attribute`, `array`, `scalar`, `equal`
and `close` methods, while bypassing NativeBackend construction and AX-element
checks because these were CFString objects, not real AX objects. Only
CoreFoundation and that fixture library were loaded; no ApplicationServices,
WindowServer, permission query, actual App or supplier was involved.

All six checks passed: retained out-pointer/array decoding, distinct/duplicate
references, UTF8 scalar conversion, raw failure/null output, borrowed children
remaining valid after the C creator released its own store while the copied
array stayed retained, and release of the five owned copies. Pointer, CFIndex
and CFTypeID widths were8 bytes. Sources, result and build record are in the
archive's `offline-abi/`; original fixture root is
`/Users/ryan/dev/chirality-t3/scratch/app-ax-cf-abi-nz19_vld`.
This tests the concrete general libffi/CF conversion/lifetime hypothesis, not
AX remote-object identity or the real application's accessibility implementation.

## Attribution and minimal remaining route

The retained Tauri configuration and overlays request the expected main window;
WindowServer observed it on-screen. A passed native A used the same candidate
and network-denied profile. The retained Tao0.35.2 macOS window construction
uses native NSWindow, while the bounded search of its macOS implementation and
Wry0.55.1 wkwebview source found no explicit override explaining this exact
Application-as-window result. That search is not proof of framework correctness,
and neither the source audit nor the fixture establishes a WebKit/Tauri bug,
sandbox cause or permission failure. No speculative App repair is justified.

The remaining client-specific hypothesis is whether the Python/libffi path and
a directly SDK-typed AX call disagree for the **same live owned reference**.
A minimal discriminating route would be a tiny independently implemented C
function loaded into the existing keeper, with PID supplied only from its live
original-Child binding. It would call only AXUIElementCreateApplication,
CopyAttributeValue for AXWindows/MainWindow/FocusedWindow and AXRole,
GetPid/CFGetTypeID/CFEqual, with retained copies, per-object timeout and finite
reference counts. Return typed result codes/roles/equality, no actions, images,
foreign objects, WindowServer enumeration, input variants or permission request.
The keeper would preserve its before/after birth/path/hash/reservation checks.
No separate process-control interface or generic accessibility framework is needed.

If the typed C path returns the same owned Application references, the general
ctypes conversion explanation becomes substantially less plausible; the result
still would not identify which upstream native accessibility layer is responsible.
If it returns distinct Window references while Python does not, compare those
exact call signatures/reference handling before changing the App. This proposed
observation boundary has **not** been implemented or run. It needs bounded
fixture tests and independent Claude Opus5.5/high scrutiny before inclusion in
any separately authorized future live profile. Existing window-existence facts
need not be re-probed. Current retained state would require its own freshly
reviewed admission; no reset, rebuild, supplier/model/auth/network activity or
new launch follows from this audit.
