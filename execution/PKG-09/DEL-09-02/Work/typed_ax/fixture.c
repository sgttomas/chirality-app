#include <ApplicationServices/ApplicationServices.h>
#include "reader.h"
#include "fixture_api.h"
#include <stdlib.h>
static CFMutableDictionaryRef application,window,foreign;
static int mode,foreign_role_reads,timeout_calls,copy_calls;
static CFMutableDictionaryRef element(int pid,CFStringRef role) {
 CFMutableDictionaryRef d=CFDictionaryCreateMutable(NULL,0,&kCFTypeDictionaryKeyCallBacks,&kCFTypeDictionaryValueCallBacks);
 CFNumberRef number=CFNumberCreate(NULL,kCFNumberIntType,&pid);
 CFDictionarySetValue(d,CFSTR("owner"),number);CFRelease(number);
 CFDictionarySetValue(d,kAXRoleAttribute,role);return d;
}
CFTypeRef fixture_start(int selected) {
 mode=selected;foreign_role_reads=timeout_calls=copy_calls=0;
 application=element(123,CFSTR("AXApplication"));window=element(123,CFSTR("AXWindow"));foreign=element(456,CFSTR("SECRET_FOREIGN_ROLE"));
 const void *items[]={application,window,window,foreign};
 CFArrayRef children=CFArrayCreate(NULL,items,4,&kCFTypeArrayCallBacks);
 CFDictionarySetValue(application,kAXWindowsAttribute,children);
 CFDictionarySetValue(application,kAXChildrenAttribute,children);CFRelease(children);
 CFDictionarySetValue(application,kAXMainWindowAttribute,window);CFDictionarySetValue(application,kAXFocusedWindowAttribute,window);
 return application;
}
void fixture_finish(void) {
 CFDictionaryRemoveAllValues(application);CFRelease(application);CFRelease(window);CFRelease(foreign);
 application=window=foreign=NULL;
}
int fixture_foreign_role_reads(void) {return foreign_role_reads;}
int fixture_timeout_calls(void) {return timeout_calls;}
int fixture_copy_calls(void) {return copy_calls;}
long fixture_app_retain_count(void) {return CFGetRetainCount(application);}
CFTypeID fixture_AXUIElementGetTypeID(void) {return CFDictionaryGetTypeID();}
AXError fixture_AXUIElementGetPid(AXUIElementRef ax,pid_t *pid) {
 CFNumberRef owner=CFDictionaryGetValue((CFDictionaryRef)ax,CFSTR("owner"));
 if(!owner) return kAXErrorInvalidUIElement;
 int value=0;CFNumberGetValue(owner,kCFNumberIntType,&value);*pid=value;return kAXErrorSuccess;
}
AXError fixture_AXUIElementSetMessagingTimeout(AXUIElementRef ax,float timeout) {
 timeout_calls++;if(timeout!=0.5f) abort();
 if(mode==4 && (CFTypeRef)ax==(CFTypeRef)window) return kAXErrorCannotComplete;
 return kAXErrorSuccess;
}
AXError fixture_AXUIElementCopyAttributeValue(AXUIElementRef ax,CFStringRef attr,CFTypeRef *out) {
 copy_calls++;*out=NULL;
 if((CFTypeRef)ax==(CFTypeRef)foreign && CFEqual(attr,kAXRoleAttribute)) foreign_role_reads++;
 if(mode==1) return kAXErrorCannotComplete;
 if(mode==2 && !CFEqual(attr,kAXRoleAttribute)) {*out=CFRetain(CFSTR("wrong value type"));return 0;}
 if(mode==3 && CFEqual(attr,kAXWindowsAttribute)) {
  const void *items[65];for(int i=0;i<65;i++)items[i]=window;
  *out=CFArrayCreate(NULL,items,65,&kCFTypeArrayCallBacks);return 0;
 }
 CFTypeRef value=CFDictionaryGetValue((CFDictionaryRef)ax,attr);
 if(!value) return kAXErrorAttributeUnsupported;
 *out=CFRetain(value);return kAXErrorSuccess;
}
