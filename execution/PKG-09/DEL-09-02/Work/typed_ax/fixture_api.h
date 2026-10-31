#ifndef CHIRALITY_TYPED_AX_FIXTURE_API
#define CHIRALITY_TYPED_AX_FIXTURE_API
/* Test build only: no real AX calls. Production reader uses SDK functions. */
CFTypeID fixture_AXUIElementGetTypeID(void);
AXError fixture_AXUIElementGetPid(AXUIElementRef, pid_t *);
AXError fixture_AXUIElementSetMessagingTimeout(AXUIElementRef, float);
AXError fixture_AXUIElementCopyAttributeValue(AXUIElementRef, CFStringRef, CFTypeRef *);
#define AXUIElementGetTypeID fixture_AXUIElementGetTypeID
#define AXUIElementGetPid fixture_AXUIElementGetPid
#define AXUIElementSetMessagingTimeout fixture_AXUIElementSetMessagingTimeout
#define AXUIElementCopyAttributeValue fixture_AXUIElementCopyAttributeValue
#endif
