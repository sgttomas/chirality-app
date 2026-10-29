// Synthetic mechanism probe only; no App adapter, supplier, or adopted policy.
using System;
using System.IO;
using System.Text;
using System.Threading;
using System.Diagnostics;
using System.ComponentModel;
using System.Collections.Generic;
using System.Runtime.InteropServices;

public static class P03Fixture {
    const uint SUSPENDED=4, EXTENDED=0x80000, WAIT_TIMEOUT=258;
    const int HANDLE_LIST=0x20002, JOB_LIST=0x2000D;
    static string Nonce, Root, Exe, Scenario;
    static long ExperimentEnd, CleanupEnd;
    static readonly List<IntPtr> Handles=new List<IntPtr>();
    static readonly List<IntPtr> Processes=new List<IntPtr>();
    static readonly List<IntPtr> Jobs=new List<IntPtr>();
    static Timer Watchdog;

    [StructLayout(LayoutKind.Sequential)] struct SA { public int size; public IntPtr sd; public int inherit; }
    [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] struct SI {
        public int cb; public string reserved,desktop,title;
        public uint x,y,xs,ys,xc,yc,fill,flags; public short show,cb2;
        public IntPtr reserved2,input,output,error;
    }
    [StructLayout(LayoutKind.Sequential)] struct SX { public SI si; public IntPtr attrs; }
    [StructLayout(LayoutKind.Sequential)] struct PI { public IntPtr process,thread; public uint pid,tid; }
    [StructLayout(LayoutKind.Sequential)] struct BASIC {
        public long processTime,jobTime; public uint flags; public UIntPtr min,max;
        public uint active; public UIntPtr affinity; public uint priority,scheduling;
    }
    [StructLayout(LayoutKind.Sequential)] struct COUNTERS { public ulong a,b,c,d,e,f; }
    [StructLayout(LayoutKind.Sequential)] struct LIMITS {
        public BASIC basic; public COUNTERS io; public UIntPtr process,job,peakProcess,peakJob;
    }
    [StructLayout(LayoutKind.Sequential)] struct ACCOUNTING {
        public long a,b,c,d; public uint faults,total,active,terminated;
    }
    [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr CreateJobObjectW(IntPtr sa,IntPtr name);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool SetInformationJobObject(IntPtr job,int cls,ref LIMITS info,int size);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool QueryInformationJobObject(IntPtr job,int cls,out ACCOUNTING info,int size,IntPtr returned);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool IsProcessInJob(IntPtr process,IntPtr job,out bool member);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool AssignProcessToJobObject(IntPtr job,IntPtr process);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool TerminateJobObject(IntPtr job,uint code);
    [DllImport("kernel32.dll",SetLastError=true)] static extern uint WaitForSingleObject(IntPtr handle,uint ms);
    [DllImport("kernel32.dll",SetLastError=true)] static extern uint ResumeThread(IntPtr handle);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool CloseHandle(IntPtr handle);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool GetHandleInformation(IntPtr handle,out uint flags);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool SetHandleInformation(IntPtr handle,uint mask,uint flags);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool CreatePipe(out IntPtr read,out IntPtr write,ref SA sa,uint size);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool PeekNamedPipe(IntPtr handle,IntPtr buffer,uint size,IntPtr read,out uint available,IntPtr left);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool ReadFile(IntPtr handle,byte[] buffer,uint size,out uint read,IntPtr ov);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool WriteFile(IntPtr handle,byte[] buffer,uint size,out uint written,IntPtr ov);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool DuplicateHandle(IntPtr source,IntPtr handle,IntPtr target,out IntPtr copy,uint access,bool inherit,uint options);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool InitializeProcThreadAttributeList(IntPtr list,int count,uint flags,ref IntPtr size);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool UpdateProcThreadAttribute(IntPtr list,uint flags,IntPtr attr,IntPtr value,IntPtr size,IntPtr previous,IntPtr returned);
    [DllImport("kernel32.dll")] static extern void DeleteProcThreadAttributeList(IntPtr list);
    [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern bool CreateProcessW(string app,StringBuilder command,IntPtr psa,IntPtr tsa,bool inherit,uint flags,IntPtr env,string cwd,ref SX startup,out PI pi);
    [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
    [DllImport("kernel32.dll")] static extern IntPtr GetStdHandle(int kind);
    [DllImport("kernel32.dll")] static extern void ExitProcess(uint code);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool GetExitCodeProcess(IntPtr process,out uint code);
    [DllImport("kernel32.dll",SetLastError=true)] static extern bool IsWow64Process2(IntPtr process,out ushort machine,out ushort native);

    static void Require(bool ok,string reason) { if(!ok) throw new InvalidOperationException(reason); }
    static void Check(bool ok,string api) { if(!ok) throw new Win32Exception(Marshal.GetLastWin32Error(),api); }
    static long Now { get { return Stopwatch.GetTimestamp(); } }
    static long After(int ms) { return Now+Stopwatch.Frequency*ms/1000; }
    static void Log(string kind,string detail) { Console.WriteLine(Now+"\t"+Nonce+"\t"+kind+"\t"+detail); Console.Out.Flush(); }
    static void Close(IntPtr h) { Check(CloseHandle(h),"CloseHandle"); Handles.Remove(h); }
    static void Noninherit(IntPtr h) { uint f; Check(GetHandleInformation(h,out f),"GetHandleInformation"); Require((f&1)==0,"inheritable custody"); }
    static bool Signaled(IntPtr h) { uint w=WaitForSingleObject(h,0); Require(w==0||w==WAIT_TIMEOUT,"wait UNKNOWN"); return w==0; }
    static bool Member(IntPtr p,IntPtr j) { bool b; Check(IsProcessInJob(p,j,out b),"IsProcessInJob"); return b; }
    static uint Active(IntPtr job) { ACCOUNTING a; Check(QueryInformationJobObject(job,1,out a,Marshal.SizeOf(typeof(ACCOUNTING)),IntPtr.Zero),"Job accounting UNKNOWN"); return a.active; }
    static IntPtr Job(bool safety) {
        IntPtr j=CreateJobObjectW(IntPtr.Zero,IntPtr.Zero); Check(j!=IntPtr.Zero,"CreateJobObjectW");
        Jobs.Add(j); Noninherit(j); LIMITS l=new LIMITS();
        // Small fixture-only containment: 128 MiB per process, 384 MiB per Job,
        // at most four contained processes; only external safety uses last-close.
        l.basic.flags=0x100u|0x200u|8u|(safety?0x2000u:0u); l.basic.active=4;
        l.process=new UIntPtr(128u*1024*1024); l.job=new UIntPtr(384u*1024*1024);
        Check(SetInformationJobObject(j,9,ref l,Marshal.SizeOf(typeof(LIMITS))),"SetInformationJobObject"); return j;
    }
    sealed class Reader {
        public IntPtr Handle; public string Pending=""; public bool Eof;
        public Reader(IntPtr h) { Handle=h; }
        public string Poll() {
            int i=Pending.IndexOf('\n');
            if(i>=0) { string line=Pending.Substring(0,i); Pending=Pending.Substring(i+1); return line; }
            if(Eof) return null;
            uint n; if(!PeekNamedPipe(Handle,IntPtr.Zero,0,IntPtr.Zero,out n,IntPtr.Zero)) {
                int e=Marshal.GetLastWin32Error(); if(e==109) { Eof=true; return null; } throw new Win32Exception(e,"PeekNamedPipe");
            }
            Require(n<=4096 && Pending.Length<=4096,"private channel bound"); if(n==0) return null;
            byte[] b=new byte[Math.Min(n,1024)]; uint read; Check(ReadFile(Handle,b,(uint)b.Length,out read,IntPtr.Zero),"ReadFile");
            Pending+=Encoding.ASCII.GetString(b,0,(int)read); return Poll();
        }
        public string Until(long end) {
            while(Now<end) { string s=Poll(); if(s!=null) return s; Require(!Eof,"unexpected EOF"); Thread.Sleep(5); }
            throw new TimeoutException("original absolute deadline");
        }
    }
    sealed class Child { public PI Pi; public IntPtr Input; public Reader Output; }
    static void Pipe(out IntPtr r,out IntPtr w) { SA sa=new SA(); sa.size=Marshal.SizeOf(typeof(SA)); sa.inherit=1; Check(CreatePipe(out r,out w,ref sa,4096),"CreatePipe"); Handles.Add(r); Handles.Add(w); }
    static PI Spawn(string mode,IntPtr input,IntPtr output,IntPtr creationJob) {
        int count=creationJob==IntPtr.Zero?1:2; IntPtr size=IntPtr.Zero;
        InitializeProcThreadAttributeList(IntPtr.Zero,count,0,ref size); Require(size!=IntPtr.Zero,"attribute size");
        IntPtr list=Marshal.AllocHGlobal(size),hs=IntPtr.Zero,js=IntPtr.Zero; bool init=false;
        try {
            Check(InitializeProcThreadAttributeList(list,count,0,ref size),"attribute init"); init=true;
            hs=Marshal.AllocHGlobal(IntPtr.Size*2); Marshal.WriteIntPtr(hs,0,input); Marshal.WriteIntPtr(hs,IntPtr.Size,output);
            Check(UpdateProcThreadAttribute(list,0,new IntPtr(HANDLE_LIST),hs,new IntPtr(IntPtr.Size*2),IntPtr.Zero,IntPtr.Zero),"HANDLE_LIST");
            if(creationJob!=IntPtr.Zero) {
                js=Marshal.AllocHGlobal(IntPtr.Size); Marshal.WriteIntPtr(js,creationJob);
                Check(UpdateProcThreadAttribute(list,0,new IntPtr(JOB_LIST),js,new IntPtr(IntPtr.Size),IntPtr.Zero,IntPtr.Zero),"JOB_LIST");
            }
            SX sx=new SX(); sx.si.cb=Marshal.SizeOf(typeof(SX)); sx.si.flags=0x100; sx.si.input=input; sx.si.output=output; sx.si.error=output; sx.attrs=list;
            string cmd="\""+Exe+"\" "+mode+" "+Nonce+" "+Scenario+" \""+Root+"\" "+ExperimentEnd+" "+CleanupEnd;
            PI p; Check(CreateProcessW(Exe,new StringBuilder(cmd),IntPtr.Zero,IntPtr.Zero,true,EXTENDED|SUSPENDED,IntPtr.Zero,Root,ref sx,out p),"CreateProcessW");
            Processes.Add(p.process); Handles.Add(p.thread); Noninherit(p.process); Noninherit(p.thread); return p;
        } finally { if(init) DeleteProcThreadAttributeList(list); Marshal.FreeHGlobal(list); if(hs!=IntPtr.Zero) Marshal.FreeHGlobal(hs); if(js!=IntPtr.Zero) Marshal.FreeHGlobal(js); }
    }
    static Child Create(string mode,IntPtr job) {
        IntPtr ir,iw,or,ow; Pipe(out ir,out iw); Pipe(out or,out ow);
        Check(SetHandleInformation(iw,1,0),"stdin parent"); Check(SetHandleInformation(or,1,0),"stdout parent");
        PI p=Spawn(mode,ir,ow,job); Close(ir); Close(ow);
        Require(Member(p.process,job),"creation Job membership");
        return new Child { Pi=p,Input=iw,Output=new Reader(or) };
    }
    static Child ContainedActor(string mode,IntPtr inner) {
        // Inherit the controller's external safety Job at creation. No breakaway
        // flag exists. Assign the inner generation Job while still suspended.
        Child c=Create(mode,IntPtr.Zero);
        Check(AssignProcessToJobObject(inner,c.Pi.process),"suspended inner assignment");
        Require(Member(c.Pi.process,inner),"inner membership"); return c;
    }
    static void Resume(PI p) { Require(ResumeThread(p.thread)==1,"ResumeThread"); }
    static void Emit(string kind,string detail) {
        byte[] b=Encoding.ASCII.GetBytes(kind+"|"+Nonce+"|"+detail+"\n"); uint n;
        Require(b.Length<512,"event bound"); Check(WriteFile(GetStdHandle(-11),b,(uint)b.Length,out n,IntPtr.Zero),"helper event"); Require(n==b.Length,"short event");
    }
    static string Event(Reader r,string kind) { string[] p=r.Until(ExperimentEnd).Split('|'); Require(p.Length==3&&p[0]==kind&&p[1]==Nonce,"private source event"); return p[2]; }
    static void WaitAll(IntPtr job,long end) {
        while(Now<end) {
            bool all=true; foreach(IntPtr p in Processes) all &= Signaled(p);
            if(all && Active(job)==0) return; Thread.Sleep(5);
        }
        throw new TimeoutException("cleanup UNKNOWN");
    }
    sealed class Generation {
        public readonly string Session,Home; public readonly int Counter;
        public Generation(string s,string h,int c) { Session=s; Home=h; Counter=c; }
        public bool Same(Generation g) { return g!=null&&Session==g.Session&&Home==g.Home&&Counter==g.Counter; }
        public override string ToString() { return "appSession="+Session+";home="+Home+";spawnCounter="+Counter; }
    }
    // Constructors and handles stay private in this synthetic executable. No
    // deserializer or PID/name acquisition path exists; integers are diagnostics.
    sealed class Custody {
        public readonly IntPtr Job,Process; public readonly Child Child;
        public Generation Generation { get; private set; }
        public Custody(IntPtr j,Child c) { Job=j; Process=c.Pi.process; Child=c; }
        public bool Bind(Generation g) { if(Generation!=null) return false; Generation=g; return true; }
    }
    sealed class Stop {
        public readonly Custody Original; public readonly Generation Generation;
        public Stop(Custody c) { Original=c; Generation=c.Generation; }
    }
    static Stop Begin(Custody slot,Generation expected) {
        if(!slot.Generation.Same(expected)) return null;
        Log("STOP_CAUSE","cause=explicit-fixture-stop;"+expected);
        Stop pending=new Stop(slot); // Lease/captured target precedes any wait.
        Close(slot.Child.Input);
        Log("STDIN_CLOSED",expected.ToString()); return pending;
    }
    static bool CanRetire(bool terminateOk,bool leaderSignaled,bool authoritativeZero) {
        // terminateOk deliberately supplies no exit evidence.
        return leaderSignaled && authoritativeZero;
    }
    static void Refused(bool rejected,string kind) { Require(rejected,"negative admission unexpectedly accepted: "+kind); Log("REFUSED",kind); }
    static bool FreshCustody(object evidence) { return evidence is Custody; }
    static void Controller() {
        long start=Now;
        IntPtr j=Job(false); Child c=ContainedActor("leader",j);
        Custody g=new Custody(j,c); Require(g.Bind(new Generation(Nonce,"fixture-home",1)),"first bind");
        Log("BOUND",g.Generation.ToString()); Resume(c.Pi);
        string raw=Event(c.Output,"DESCENDANT"); long handle;
        Require(Int64.TryParse(raw,out handle)&&handle>0,"source handle syntax");
        IntPtr d; Check(DuplicateHandle(c.Pi.process,new IntPtr(handle),GetCurrentProcess(),out d,0x100000|0x1000,false,0),"original leader DuplicateHandle");
        Processes.Add(d); Noninherit(d); Require(Member(d,j)&&!Signaled(d),"original descendant membership/live");
        Log("DESCENDANT","originalLeaderHandle=true;originalJobMember=true;live=true");
        Refused(!g.Bind(new Generation(Nonce,"fixture-home",2)),"second-bind");
        Refused(!FreshCustody((object)(long)c.Pi.pid),"numeric-pid");
        Refused(!FreshCustody("{pid:"+c.Pi.pid+",generation:1}"),"serialized-pid");
        Refused(Begin(g,new Generation("other-session","fixture-home",1))==null,"stale-session");
        Refused(Begin(g,new Generation(Nonce,"other-home",1))==null,"stale-home");
        Refused(Begin(g,new Generation(Nonce,"fixture-home",2))==null,"stale-counter");
        Stop pending=Begin(g,g.Generation); Require(pending!=null,"start original Stop");
        Event(c.Output,"EOF");
        long graceEnd=After(150); Require(graceEnd<ExperimentEnd,"no grace budget");
        while(Now<graceEnd) Thread.Sleep(5);
        Require(Signaled(g.Process)&&!Signaled(d)&&Active(j)==1,"EOF/grace survival not established");
        Log("GRACE","testMilliseconds=150;leaderSignaled=true;descendantLive=true;originalActive=1");
        Log("PENDING_CAPTURE",pending.Generation.ToString());
        IntPtr nextJob=Job(false); Child next=ContainedActor("leaf",nextJob);
        Custody successor=new Custody(nextJob,next);
        Require(successor.Bind(new Generation(Nonce,"fixture-home",2)),"successor bind"); Resume(next.Pi); Event(next.Output,"LIVE");
        Custody slot=successor; Log("SLOT_REPLACED",slot.Generation.ToString());
        Refused(Begin(slot,g.Generation)==null,"stale-generation-start");
        Require(!Signaled(next.Pi.process)&&Active(slot.Job)==1,"successor pre-stop live");
        Log("PRE_TERMINATE","originalDescendantLive="+(!Signaled(d))+";successorLive="+(!Signaled(next.Pi.process)));
        IntPtr target=Scenario=="wrong-slot"?slot.Job:pending.Original.Job;
        Log("TERMINATE_ATTEMPT",Scenario=="wrong-slot"?"target=current-slot-negative":"target=captured-original");
        bool ok=TerminateJobObject(target,71); int error=ok?0:Marshal.GetLastWin32Error();
        Log("TERMINATE_RESULT","ok="+ok+";error="+error+";confirmed=false"); Check(ok,"TerminateJobObject original");
        Require(!CanRetire(true,false,false)&&!CanRetire(true,true,false)&&!CanRetire(true,false,true),"retirement negative control");
        Log("REFUSED","success-alone;leader-only;zero-only");
        bool confirmed=false;
        if(Scenario=="missing-observation") {
            Log("OBSERVATION_UNKNOWN","injected-authoritative-job-query-unavailable;custody-retained=true");
        } else {
            while(Now<ExperimentEnd) {
                bool leader=Signaled(g.Process),zero=Active(g.Job)==0;
                if(CanRetire(ok,leader,zero)&&Signaled(d)) { confirmed=true; break; }
                if(Scenario=="wrong-slot"&&Signaled(next.Pi.process)&&Active(slot.Job)==0) break;
                Thread.Sleep(5);
            }
            Log("OBSERVATION","originalLeaderSignaled="+Signaled(g.Process)+";originalDescendantSignaled="+Signaled(d)+";originalActive="+Active(g.Job)+";successorSignaled="+Signaled(next.Pi.process)+";successorActive="+Active(slot.Job));
        }
        Log("RETIREMENT",confirmed?"CONFIRMED":"UNKNOWN");
        if(Scenario=="positive") Require(confirmed&&Signaled(d)&&!Signaled(next.Pi.process)&&Active(slot.Job)==1,"generation isolation failure");
        else if(Scenario=="wrong-slot") Require(!confirmed&&!Signaled(d)&&Signaled(next.Pi.process)&&Active(g.Job)==1,"wrong-slot control not falsifiable");
        else Require(!confirmed,"partial failure was promoted");
        Log("CASE_DONE",Scenario+";elapsedTicks="+(Now-start));
    }
    static void Helper(string mode) {
        if(mode=="leaf") { Emit("LIVE","bounded-leaf"); while(Now<ExperimentEnd) Thread.Sleep(10); return; }
        PI d=Spawn("descendant",GetStdHandle(-10),GetStdHandle(-11),IntPtr.Zero); Resume(d);
        Emit("DESCENDANT",d.process.ToInt64().ToString());
        Reader input=new Reader(GetStdHandle(-10));
        while(Now<ExperimentEnd) { Require(input.Poll()==null,"unexpected stdin data"); if(input.Eof) { Emit("EOF","leader-observed-stdin-eof"); return; } Thread.Sleep(5); }
        throw new TimeoutException("leader EOF deadline");
    }
    static int Supervisor() {
        IntPtr safety=Job(true); bool clean=false; int result=2;
        // Outer watchdog reports no pass; last-close disposes only this fixture.
        Watchdog=new Timer(delegate { TerminateJobObject(safety,92); ExitProcess(92); },null,25000,Timeout.Infinite);
        try {
            Child controller=Create("controller",safety); Resume(controller.Pi);
            bool eof=false;
            while(Now<CleanupEnd) {
                string line=controller.Output.Poll(); if(line!=null) { Console.Write(line+"\n"); Console.Out.Flush(); }
                if(Signaled(controller.Pi.process)&&controller.Output.Eof) { eof=true; break; }
                Thread.Sleep(5);
            }
            Require(eof,"controller exit/capture deadline"); uint code; Check(GetExitCodeProcess(controller.Pi.process,out code),"controller exit code");
            Require(code==0,"controller failed"); result=0;
        } finally {
            try {
                Log("SAFETY_TERMINATE","fixture-cleanup-only"); Check(TerminateJobObject(safety,72),"safety termination");
                WaitAll(safety,CleanupEnd); Log("SAFETY_CLEANUP","retainedControllerSignaled=true;active=0"); clean=true;
            } catch(Exception e) { Log("CLEANUP_UNKNOWN",e.GetType().Name); }
            if(!clean) ExitProcess(3);
            Watchdog.Dispose();
        }
        return result;
    }
    public static int Main(string[] args) {
        try {
            Require(args.Length==6,"mode nonce scenario root experimentEnd cleanupEnd");
            Nonce=args[1]; Scenario=args[2]; Root=Path.GetFullPath(args[3]); Exe=typeof(P03Fixture).Assembly.Location;
            Require(System.Text.RegularExpressions.Regex.IsMatch(Nonce,"^[a-f0-9]{32}$"),"nonce");
            Require(Scenario=="positive"||Scenario=="wrong-slot"||Scenario=="missing-observation","scenario");
            Require(Root.IndexOf('"')<0&&Exe.IndexOf('"')<0&&Path.GetDirectoryName(Exe)==Root,"owned executable root");
            Require(Path.GetFileName(Root)=="chirality-app-p03-"+Nonce&&File.ReadAllText(Path.Combine(Root,"OWNER"))==Nonce,"owned scratch");
            foreach(string n in new string[]{"TEMP","TMP","CODEX_HOME"}) Require(Environment.GetEnvironmentVariable(n)==Path.Combine(Root,n),"scratch environment");
            ushort machine,native; Check(IsWow64Process2(GetCurrentProcess(),out machine,out native),"native identity");
            Require(machine==0&&native==0x8664&&IntPtr.Size==8,"native AMD64 required");
            if(args[0]=="supervisor") {
                Require(args[4]=="0"&&args[5]=="0","supervisor deadline input"); ExperimentEnd=After(12000); CleanupEnd=After(18000);
                Log("IDENTITY","processMachine=0;nativeMachine=34404;pointerBytes=8;frequency="+Stopwatch.Frequency+";experimentEnd="+ExperimentEnd+";cleanupEnd="+CleanupEnd); return Supervisor();
            }
            Require(Int64.TryParse(args[4],out ExperimentEnd)&&Int64.TryParse(args[5],out CleanupEnd)&&Now<ExperimentEnd&&ExperimentEnd<CleanupEnd&&CleanupEnd<=After(18000),"original deadlines");
            if(args[0]=="controller") {
                bool completed=false;
                try { Controller(); completed=true; }
                finally {
                    foreach(IntPtr j in Jobs) Check(TerminateJobObject(j,73),"controller cleanup");
                    // Reserve the final three seconds for the external safety
                    // owner, including an actor whose inner assignment failed.
                    foreach(IntPtr j in Jobs) WaitAll(j,CleanupEnd-3*Stopwatch.Frequency);
                    Log("CONTROLLER_CLEANUP","allRetainedActorsSignaled=true;allOriginalJobsActive=0;caseCompleted="+completed);
                }
            } else if(args[0]=="descendant") { while(Now<ExperimentEnd) Thread.Sleep(10); }
            else { Require(args[0]=="leader"||args[0]=="leaf","mode"); Helper(args[0]); }
            return 0;
        } catch(Exception e) { Log("FAILURE",e.GetType().Name+":"+e.Message.Replace('\t',' ').Replace('\n',' ').Replace('\r',' ')); return 2; }
        finally {
            // Ownership lasts through observation; no later numeric reuse.
            foreach(IntPtr h in Handles) CloseHandle(h);
            foreach(IntPtr p in Processes) CloseHandle(p);
            foreach(IntPtr j in Jobs) CloseHandle(j);
        }
    }
}
