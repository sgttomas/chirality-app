#ifndef CHIRALITY_TYPED_AX_READER_H
#define CHIRALITY_TYPED_AX_READER_H
#include <CoreFoundation/CoreFoundation.h>
#include <stdint.h>
#define AX_COMPARE_ATTRIBUTES 4
#define AX_COMPARE_REFERENCES 64
/* Fixed POD ABI. No PID entrypoint, actions, global AX lookup, or image API. */
typedef struct {
    uint64_t type_id, role_type_id;
    int32_t owner_rc, role_rc, timeout_rc, status;
    uint32_t self_equal, duplicate;
    char role[128];
} AXCompareReference;
typedef struct {
    uint64_t type_id;
    int32_t value_rc, status;
    uint32_t reference_count, reserved;
    AXCompareReference references[AX_COMPARE_REFERENCES];
} AXCompareAttribute;
typedef struct {
    uint32_t abi_version, byte_size, attribute_count, completed;
    int32_t status, application_owner_rc, application_pid, application_timeout_rc;
    uint64_t application_type_id;
    AXCompareAttribute attributes[AX_COMPARE_ATTRIBUTES];
} AXCompareResult;
/* application must be the keeper's retained, already-bound AX reference.
 * This routine retains it for the call. The keeper checks original Child
 * identity/liveness immediately before and after. This is not custody. */
int chirality_ax_compare_v1(CFTypeRef application, AXCompareResult *result);
uint32_t chirality_ax_compare_size_v1(void);
#endif
