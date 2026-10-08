/* Temporary synthetic examination only. No production implementation. */
#define _DARWIN_C_SOURCE 1
#include <errno.h>
#include <fcntl.h>
#include <poll.h>
#include <pthread.h>
#include <signal.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static double mono(void) {
    struct timespec t;
    if (clock_gettime(CLOCK_MONOTONIC, &t) != 0) _Exit(90);
    return (double)t.tv_sec + (double)t.tv_nsec / 1e9;
}
static void emit(const char *format, ...) {
    char body[1800], line[2048];
    va_list ap;
    va_start(ap, format);
    int n = vsnprintf(body, sizeof(body), format, ap);
    va_end(ap);
    if (n < 0 || (size_t)n >= sizeof(body)) _Exit(91);
    int k = snprintf(line, sizeof(line), "{\"mono\":%.9f,%s}\n", mono(), body);
    if (k < 0 || (size_t)k >= sizeof(line)) _Exit(91);
    /* One bounded record; stdout is a regular owned log, not an unbounded pipe. */
    if (write(STDOUT_FILENO, line, (size_t)k) != k) _Exit(92);
}
static bool dispositions(void) {
    struct sigaction a;
    memset(&a, 0, sizeof(a));
    sigemptyset(&a.sa_mask);
    a.sa_handler = SIG_DFL;
    if (sigaction(SIGALRM, &a, NULL) || sigaction(SIGCHLD, &a, NULL)) return false;
    /* A disappeared private pipe is an EPIPE fixture failure, not an accidental
       driver/helper termination before it can record custody. Isolated helper only. */
    a.sa_handler = SIG_IGN;
    if (sigaction(SIGPIPE, &a, NULL) != 0) return false;
    sigset_t unblock;
    sigemptyset(&unblock); sigaddset(&unblock, SIGALRM);
    return sigprocmask(SIG_UNBLOCK, &unblock, NULL) == 0;
}
static void nap(void) {
    struct timespec t = {0, 10000000};
    (void)nanosleep(&t, NULL); /* No retry loop on EINTR. */
}
static int wait_readable(int fd, int millis) {
    struct pollfd p = {fd, POLLIN, 0};
    return poll(&p, 1, millis); /* One bounded poll, HUP followed by read is EOF. */
}
static bool observe(pid_t child, const char *phase, siginfo_t *info) {
    memset(info, 0, sizeof(*info));
    errno = 0;
    int r = waitid(P_PID, (id_t)child, info, WEXITED | WNOHANG | WNOWAIT);
    int e = errno;
    emit("\"event\":\"waitid\",\"phase\":\"%s\",\"target\":%ld,\"return\":%d,\"errno\":%d,\"siPid\":%ld,\"siCode\":%d,\"siStatus\":%d",
         phase, (long)child, r, e, (long)info->si_pid, info->si_code, info->si_status);
    return r == 0;
}
static void fixture(int ready, int release) {
    if (!dispositions()) { emit("\"event\":\"timerSetupFailure\",\"role\":\"fixture\",\"pid\":%ld", (long)getpid()); _Exit(40); }
    alarm(5);
    unsigned char marker = setpgid(0, 0) == 0 ? 1 : 2;
    if (write(ready, &marker, 1) != 1) _Exit(41);
    close(ready);
    if (marker != 1) _Exit(42);
    if (wait_readable(release, 2000) <= 0) _Exit(43);
    unsigned char b = 0;
    ssize_t n = read(release, &b, 1);
    close(release);
    if (n == 0 || (n == 1 && b == 7)) _Exit(37);
    _Exit(44);
}
static bool cleanup(pid_t child) {
    double end = mono() + 2.0;
    for (unsigned k = 0; k < 200 && mono() < end; ++k) {
        int status = 0;
        errno = 0;
        pid_t r = waitpid(child, &status, WNOHANG);
        int e = errno;
        emit("\"event\":\"cleanupWait\",\"target\":%ld,\"return\":%ld,\"errno\":%d,\"rawStatus\":%d", (long)child, (long)r, e, status);
        if (r == child) return true;
        if (r < 0) return false; /* ECHILD here is unknown, not manufactured reap. */
        nap();
    }
    return false;
}
static int native_observation(void) {
    if (!dispositions()) { emit("\"event\":\"timerSetupFailure\",\"role\":\"native-helper\""); return 10; }
    alarm(15);
    emit("\"event\":\"helperStart\",\"mode\":\"native\",\"pid\":%ld,\"alarmSeconds\":15,\"sigchld\":\"default-no-NOCLDWAIT\",\"sigpipe\":\"ignored-in-isolated-helper\"", (long)getpid());
    int ready[2], release[2];
    if (pipe(ready)) return 11;
    if (pipe(release)) { close(ready[0]); close(ready[1]); return 11; }
    pid_t child = fork();
    if (child < 0) { close(ready[0]); close(ready[1]); close(release[0]); close(release[1]); return 12; }
    if (child == 0) {
        close(ready[0]); close(release[1]);
        fixture(ready[1], release[0]);
    }
    close(ready[1]); close(release[0]);
    emit("\"event\":\"childCreated\",\"pid\":%ld,\"parent\":%ld,\"role\":\"one-direct-fixture-no-descendants\",\"alarmSeconds\":5", (long)child, (long)getpid());
    bool ok = false, reaped = false;
    const char *failure = "ready";
    unsigned char marker = 0;
    if (wait_readable(ready[0], 1000) <= 0 || read(ready[0], &marker, 1) != 1 || marker != 1) goto done;
    close(ready[0]); ready[0] = -1;
    siginfo_t first, second;
    failure = "live-observation";
    if (!observe(child, "live-held-at-release", &first) || first.si_pid != 0) goto done;
    errno = 0;
    pid_t pg = getpgid(child);
    emit("\"event\":\"getpgid\",\"phase\":\"live\",\"target\":%ld,\"return\":%ld,\"errno\":%d", (long)child, (long)pg, errno);
    failure = "group-setup";
    if (pg != child) goto done;
    unsigned char go = 7;
    failure = "release-write";
    errno = 0;
    ssize_t written = write(release[1], &go, 1);
    int write_error = errno;
    emit("\"event\":\"releaseWrite\",\"return\":%ld,\"errno\":%d", (long)written, write_error);
    if (written != 1) goto done;
    close(release[1]); release[1] = -1;
    emit("\"event\":\"releaseClosed\",\"target\":%ld", (long)child);
    failure = "terminal-observation";
    double end = mono() + 2.0;
    bool terminal = false;
    for (unsigned k = 0; k < 200 && mono() < end; ++k) {
        if (!observe(child, "terminal-first", &first)) goto done;
        if (first.si_pid != 0) { terminal = true; break; }
        nap();
    }
    if (!terminal || first.si_pid != child || first.si_code != CLD_EXITED || first.si_status != 37) goto done;
    failure = "terminal-repeat";
    if (!observe(child, "terminal-repeat", &second) || second.si_pid != child || second.si_code != first.si_code || second.si_status != first.si_status) goto done;
    errno = 0;
    pg = getpgid(child);
    emit("\"event\":\"getpgid\",\"phase\":\"unreaped-observation-only\",\"target\":%ld,\"return\":%ld,\"errno\":%d", (long)child, (long)pg, errno);
    emit("\"event\":\"signalsRevoked\",\"target\":%ld,\"realSignalCalls\":0", (long)child);
    int status = 0;
    errno = 0;
    pid_t r = waitpid(child, &status, WNOHANG);
    int e = errno;
    emit("\"event\":\"consume\",\"target\":%ld,\"return\":%ld,\"errno\":%d,\"rawStatus\":%d", (long)child, (long)r, e, status);
    reaped = r == child;
    failure = "consume";
    if (!reaped || !WIFEXITED(status) || WEXITSTATUS(status) != 37) goto done;
    errno = 0;
    r = waitpid(child, &status, WNOHANG); e = errno;
    emit("\"event\":\"afterConsume\",\"target\":%ld,\"return\":%ld,\"errno\":%d", (long)child, (long)r, e);
    failure = "after-consume";
    ok = r == -1 && e == ECHILD;
done:
    if (ready[0] >= 0) close(ready[0]);
    if (release[1] >= 0) { close(release[1]); emit("\"event\":\"releaseClosedOnFailure\",\"target\":%ld", (long)child); }
    if (!reaped) reaped = cleanup(child);
    emit("\"event\":\"nativeResult\",\"pass\":%s,\"failurePhase\":\"%s\",\"child\":%ld,\"exactChildReaped\":%s,\"realSignalCalls\":0", ok ? "true" : "false", ok ? "none" : failure, (long)child, reaped ? "true" : "false");
    return ok && reaped ? 0 : 13;
}

/* Inert model only: number 700 is never supplied to any OS process API. */
typedef struct {
    pthread_mutex_t owner, barrier;
    pthread_cond_t cv;
    int stage, done, identity, signals, wrong;
    bool reaped, revoked, broken;
} Model;
static void fatal_model(const char *reason) {
    emit("\"event\":\"modelFailure\",\"reason\":\"%s\"", reason);
    _Exit(60); /* No potentially unbounded join on a failed barrier. */
}
static void lock(pthread_mutex_t *m) { if (pthread_mutex_lock(m)) fatal_model("mutex-lock"); }
static void unlock(pthread_mutex_t *m) { if (pthread_mutex_unlock(m)) fatal_model("mutex-unlock"); }
static void await(Model *m, int stage, int done) {
    struct timespec until;
    if (clock_gettime(CLOCK_REALTIME, &until)) fatal_model("clock");
    until.tv_sec += 1;
    lock(&m->barrier);
    while (m->stage < stage || m->done < done) {
        int r = pthread_cond_timedwait(&m->cv, &m->barrier, &until);
        if (r != 0) fatal_model("barrier-timeout-or-error");
    }
    unlock(&m->barrier);
}
static void advance(Model *m, int stage, bool done) {
    lock(&m->barrier);
    if (stage > m->stage) m->stage = stage;
    if (done) ++m->done;
    if (pthread_cond_broadcast(&m->cv)) fatal_model("broadcast");
    unlock(&m->barrier);
}
static void backend_signal(Model *m) {
    ++m->signals;
    if (m->identity != 1 || m->reaped) ++m->wrong;
    emit("\"event\":\"inertSignal\",\"inventedNumber\":700,\"identity\":%d,\"wrongIdentity\":%s,\"brokenControl\":%s", m->identity, (m->identity != 1 || m->reaped) ? "true" : "false", m->broken ? "true" : "false");
}
static void *issuer(void *arg) {
    Model *m = arg;
    lock(&m->owner);
    if (m->revoked || m->reaped || m->identity != 1) fatal_model("initial-eligibility");
    if (m->broken) unlock(&m->owner);
    advance(m, 1, false);
    await(m, 2, 0);
    if (m->broken) lock(&m->owner); /* Deliberately fails to revalidate. */
    backend_signal(m);
    unlock(&m->owner);
    advance(m, 3, true);
    return NULL;
}
static void *reaper(void *arg) {
    Model *m = arg;
    await(m, 1, 0);
    int r = pthread_mutex_trylock(&m->owner);
    if (!m->broken) {
        if (r != EBUSY) fatal_model("owner-not-held-through-action");
        emit("\"event\":\"inertReaperBusy\"");
    } else {
        if (r != 0) fatal_model("broken-control-not-unlocked");
        m->revoked = true; m->reaped = true; m->identity = 2;
        unlock(&m->owner);
        emit("\"event\":\"inertReapAndReuse\",\"inventedNumber\":700,\"newIdentity\":2");
    }
    advance(m, 2, true);
    return NULL;
}
static void schedule(bool broken) {
    Model m;
    memset(&m, 0, sizeof(m)); m.identity = 1; m.broken = broken;
    if (pthread_mutex_init(&m.owner, NULL) || pthread_mutex_init(&m.barrier, NULL) || pthread_cond_init(&m.cv, NULL)) fatal_model("init");
    pthread_t a, b;
    if (pthread_create(&a, NULL, issuer, &m) || pthread_create(&b, NULL, reaper, &m)) fatal_model("thread-create");
    await(&m, 3, 2);
    if (pthread_join(a, NULL) || pthread_join(b, NULL)) fatal_model("join");
    lock(&m.owner);
    bool pass = broken ? (m.signals == 1 && m.wrong == 1) : (m.signals == 1 && m.wrong == 0);
    if (!broken) {
        m.revoked = true; m.reaped = true; m.identity = 2;
        /* Reverse ordering: an old owner must refuse before backend invocation. */
        int before = m.signals;
        bool denied = m.revoked || m.reaped || m.identity != 1;
        if (!denied) backend_signal(&m);
        pass = pass && denied && m.signals == before;
        emit("\"event\":\"inertReapFirstRefusal\",\"denied\":%s,\"additionalSignals\":%d", denied ? "true" : "false", m.signals - before);
    }
    unlock(&m.owner);
    emit("\"event\":\"modelScheduleResult\",\"schedule\":\"%s\",\"pass\":%s,\"inertSignals\":%d,\"wrongIdentitySignals\":%d,\"realSignalCalls\":0", broken ? "deliberately-broken-red-control" : "guarded-signal-first-and-reap-first", pass ? "true" : "false", m.signals, m.wrong);
    if (!pass) fatal_model("assertion");
    if (pthread_cond_destroy(&m.cv) || pthread_mutex_destroy(&m.barrier) || pthread_mutex_destroy(&m.owner)) fatal_model("destroy");
}
static int model(void) {
    if (!dispositions()) { emit("\"event\":\"timerSetupFailure\",\"role\":\"model-helper\""); return 50; }
    alarm(10);
    emit("\"event\":\"helperStart\",\"mode\":\"inert-model\",\"pid\":%ld,\"alarmSeconds\":10", (long)getpid());
    schedule(false); schedule(true);
    emit("\"event\":\"modelResult\",\"pass\":true,\"realSignalCalls\":0");
    return 0;
}
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (strcmp(argv[1], "native") == 0) return native_observation();
    if (strcmp(argv[1], "model") == 0) return model();
    return 2;
}
