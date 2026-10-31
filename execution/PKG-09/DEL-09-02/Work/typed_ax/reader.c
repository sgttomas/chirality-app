#include "reader.h"
#include <ApplicationServices/ApplicationServices.h>
#include <string.h>
#include <time.h>
#ifdef AX_COMPARE_TEST
#include "fixture_api.h"
#endif
/* Internal observation statuses, distinct from raw AX return codes. */
enum { OBS_OK=0, OBS_TYPE=1, OBS_OWNER=2, OBS_BOUND=3, OBS_TIMEOUT=4,
       OBS_TEXT=5, OBS_RAW_ERROR=6, OBS_ARGUMENT=7 };
static double seconds(void) {
#ifdef AX_COMPARE_TEST
    return fixture_seconds();
#else
    struct timespec t;
    if (clock_gettime(CLOCK_MONOTONIC, &t)) return -1;
    return (double)t.tv_sec + (double)t.tv_nsec / 1000000000.0;
#endif
}
static int expired(double deadline) { double t=seconds();return t<0 || t>=deadline; }
static int bounded(AXUIElementRef element, int32_t *rc) {
    *rc=AXUIElementSetMessagingTimeout(element,0.5f);
    return *rc==kAXErrorSuccess;
}
static void reference(CFTypeRef element, AXUIElementRef application, pid_t owner,
                      const CFTypeRef *seen, CFIndex count, double deadline,
                      AXCompareReference *out) {
    out->owner_rc=out->role_rc=out->timeout_rc=INT32_MIN;
    if (!element) {out->status=OBS_TYPE;return;}
    out->type_id=CFGetTypeID(element);
    if (out->type_id!=AXUIElementGetTypeID()) {out->status=OBS_TYPE;return;}
    if (expired(deadline)) {out->status=OBS_TIMEOUT;return;}
    AXUIElementRef ax=(AXUIElementRef)element;
    if (!bounded(ax,&out->timeout_rc)) {out->status=OBS_RAW_ERROR;return;}
    pid_t actual=0;out->owner_rc=AXUIElementGetPid(ax,&actual);
    if (out->owner_rc!=kAXErrorSuccess || actual!=owner) {out->status=OBS_OWNER;return;}
    /* Foreign role/content is never read, and foreign PID is never returned. */
    out->self_equal=CFEqual(element,application)?1:0;
    for (CFIndex i=0;i<count;i++) if (seen[i] && CFEqual(element,seen[i])) {out->duplicate=1;break;}
    if (out->duplicate) return;
    if (expired(deadline)) {out->status=OBS_TIMEOUT;return;}
    CFTypeRef role=NULL;
    out->role_rc=AXUIElementCopyAttributeValue(ax,kAXRoleAttribute,&role);
    if (out->role_rc!=kAXErrorSuccess) out->status=OBS_RAW_ERROR;
    else if (!role || (out->role_type_id=CFGetTypeID(role))!=CFStringGetTypeID()) out->status=OBS_TYPE;
    else if (!CFStringGetCString((CFStringRef)role,out->role,sizeof(out->role),kCFStringEncodingUTF8)) {out->role[0]=0;out->status=OBS_TEXT;}
    if (role) CFRelease(role);
}
uint32_t chirality_ax_compare_size_v1(void) {return (uint32_t)sizeof(AXCompareResult);}
int chirality_ax_compare_v1(CFTypeRef input, AXCompareResult *out) {
    if (!out) return OBS_ARGUMENT;
    memset(out,0,sizeof(*out));out->abi_version=1;out->byte_size=(uint32_t)sizeof(*out);
    out->application_owner_rc=out->application_timeout_rc=INT32_MIN;
    if (!input) return out->status=OBS_ARGUMENT;
    out->application_type_id=CFGetTypeID(input);
    if (out->application_type_id!=AXUIElementGetTypeID()) return out->status=OBS_TYPE;
    AXUIElementRef app=(AXUIElementRef)CFRetain(input);
    double start=seconds(),deadline=start+3.0;
    if (start<0) {CFRelease(app);return out->status=OBS_TIMEOUT;}
    if (!bounded(app,&out->application_timeout_rc)) {CFRelease(app);return out->status=OBS_RAW_ERROR;}
    pid_t owner=0;out->application_owner_rc=AXUIElementGetPid(app,&owner);
    if (out->application_owner_rc!=kAXErrorSuccess || owner<=0) {CFRelease(app);return out->status=OBS_OWNER;}
    out->application_pid=owner;
    const CFStringRef names[]={kAXWindowsAttribute,kAXMainWindowAttribute,kAXFocusedWindowAttribute,kAXChildrenAttribute};
    for (uint32_t n=0;n<AX_COMPARE_ATTRIBUTES;n++) {
        AXCompareAttribute *row=&out->attributes[n];row->value_rc=INT32_MIN;out->attribute_count=n+1;
        if (expired(deadline)) {row->status=OBS_TIMEOUT;out->status=OBS_TIMEOUT;break;}
        CFTypeRef value=NULL;row->value_rc=AXUIElementCopyAttributeValue(app,names[n],&value);
        if (row->value_rc!=kAXErrorSuccess) row->status=OBS_RAW_ERROR;
        else if (value) {
            row->type_id=CFGetTypeID(value);
            CFIndex count=1;int array=row->type_id==CFArrayGetTypeID();
            if (array) count=CFArrayGetCount((CFArrayRef)value);
            else if (row->type_id!=AXUIElementGetTypeID()) row->status=OBS_TYPE;
            if (count<0 || count>AX_COMPARE_REFERENCES) row->status=OBS_BOUND;
            if (!row->status) {
                CFTypeRef seen[AX_COMPARE_REFERENCES]={0};
                for (CFIndex i=0;i<count;i++) {
                    CFTypeRef element=array?CFArrayGetValueAtIndex((CFArrayRef)value,i):value;
                    row->reference_count=(uint32_t)i+1;
                    reference(element,app,owner,seen,i,deadline,&row->references[i]);
                    if (row->references[i].owner_rc==0 && row->references[i].status!=OBS_OWNER) seen[i]=element;
                    if (row->references[i].status==OBS_TIMEOUT) {row->status=OBS_TIMEOUT;out->status=OBS_TIMEOUT;break;}
                }
            }
        } else row->status=OBS_TYPE;
        /* Borrowed elements are never used beyond this owned value's lifetime. */
        if (value) CFRelease(value);
        if (out->status==OBS_TIMEOUT) break;
    }
    out->completed=out->attribute_count==AX_COMPARE_ATTRIBUTES && out->status!=OBS_TIMEOUT;
    CFRelease(app);return out->status;
}
