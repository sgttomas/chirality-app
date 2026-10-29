// Package-free fixture only. No production App policy or supplier execution.
using System;
using System.IO;
using System.Text;
using System.Diagnostics;
using System.Threading;
using System.Runtime.InteropServices;
using System.ComponentModel;
using System.Collections.Generic;

public static class ProcessFixture {
    const uint SUSPENDED=4, EXTENDED=0x80000, UNICODE_ENV=0x400;
    const uint SYNCHRONIZE=0x100000, QUERY=0x1000, TERMINATE=1;
    const uint WAIT_OBJECT_0=0, WAIT_TIMEOUT=258, INHERIT=1;
    const int HANDLE_LIST=0x20002, JOB_LIST=0x2000D;
    static readonly Stopwatch Clock=Stopwatch.StartNew();
    static string Nonce, Case, Root, Exe;
    static IntPtr Safety;
    static Timer Deadline;
    static List<IntPtr> Processes=new List<IntPtr>();
    static List<IntPtr> Jobs=new List<IntPtr>();
    static List<IntPtr> IO=new List<IntPtr>();
    static bool CleanupObserved;

    [StructLayout(LayoutKind.Sequential)] struct SA { public int size; public IntPtr sd; public int inherit; }
    [StructLayout(LayoutKind.Sequential, CharSet=CharSet.Unicode)] struct SI {
        public int cb; public string reserved,desktop,title;
        public uint x,y,xs,ys,xc,yc,fill,flags; public short show,cb2;
        public IntPtr reserved2,input,output,error;
    }
    [StructLayout(LayoutKind.Sequential)] struct SX { public SI si; public IntPtr attrs; }
    [StructLayout(LayoutKind.Sequential)] struct PI { public IntPtr process,thread; public uint pid,tid; }
    [StructLayout(LayoutKind.Sequential)] struct BASIC_LIMIT {
        public long perProcess,perJob; public uint flags;
        public UIntPtr min,max; public uint active; public UIntPtr affinity; public uint priority,scheduling;
    }
    [StructLayout(LayoutKind.Sequential)] struct IO_COUNTERS { public ulong a,b,c,d,e,f; }
    [StructLayout(LayoutKind.Sequential)] struct EXT_LIMIT {
        public BASIC_LIMIT basic; public IO_COUNTERS io; public UIntPtr process,job,peakProcess,peakJob;
    }
    [StructLayout(LayoutKind.Sequential)] struct ACCOUNTING {
        public long a,b,c,d; public uint faults,total,active,terminated;
    }
    [StructLayout(LayoutKind.Sequential)] struct SYSTEM_INFO {
        public ushort architecture,reserved; public uint page; public IntPtr min,max;
        public UIntPtr mask; public uint count,type,granularity; public ushort level,revision;
    }
    [DllImport("kernel32.dll", SetLastError=true)] static extern IntPtr CreateJobObjectW(IntPtr sa,IntPtr name);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool SetInformationJobObject(IntPtr job,int cls,ref EXT_LIMIT info,int size);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool QueryInformationJobObject(IntPtr job,int cls,out ACCOUNTING info,int size,IntPtr returned);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool AssignProcessToJobObject(IntPtr job,IntPtr process);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool IsProcessInJob(IntPtr process,IntPtr job,out bool result);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool TerminateJobObject(IntPtr job,uint code);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool TerminateProcess(IntPtr process,uint code);
    [DllImport("kernel32.dll", SetLastError=true)] static extern uint WaitForSingleObject(IntPtr h,uint ms);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool GetExitCodeProcess(IntPtr h,out uint code);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool CloseHandle(IntPtr h);
    [DllImport("kernel32.dll")] static extern IntPtr GetCurrentProcess();
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool IsWow64Process2(IntPtr p,out ushort process,out ushort native);
    [DllImport("kernel32.dll")] static extern void GetNativeSystemInfo(out SYSTEM_INFO info);
    [DllImport("kernel32.dll")] static extern void ExitProcess(uint code);
    [DllImport("kernel32.dll", SetLastError=true)] static extern uint ResumeThread(IntPtr h);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool SetHandleInformation(IntPtr h,uint mask,uint flags);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool GetHandleInformation(IntPtr h,out uint flags);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool CreatePipe(out IntPtr r,out IntPtr w,ref SA sa,uint size);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool PeekNamedPipe(IntPtr h,IntPtr buffer,uint size,IntPtr read,out uint available,IntPtr left);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool ReadFile(IntPtr h,byte[] buffer,uint size,out uint read,IntPtr ov);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool WriteFile(IntPtr h,byte[] buffer,uint size,out uint written,IntPtr ov);
    [DllImport("kernel32.dll")] static extern IntPtr GetStdHandle(int kind);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool DuplicateHandle(IntPtr source,IntPtr handle,IntPtr target,out IntPtr copy,uint access,bool inherit,uint options);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool InitializeProcThreadAttributeList(IntPtr list,int count,uint flags,ref IntPtr size);
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool UpdateProcThreadAttribute(IntPtr list,uint flags,IntPtr attr,IntPtr value,IntPtr size,IntPtr previous,IntPtr returned);
    [DllImport("kernel32.dll")] static extern void DeleteProcThreadAttributeList(IntPtr list);
    [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)] static extern bool CreateProcessW(string app,StringBuilder cmd,IntPtr psa,IntPtr tsa,bool inherit,uint flags,IntPtr env,string cwd,ref SX startup,out PI pi);

    static void Check(bool ok,string api) { if(!ok) throw new Win32Exception(Marshal.GetLastWin32Error(),api); }
    static void Require(bool ok,string reason) { if(!ok) throw new InvalidOperationException(reason); }
    static void Log(string kind,string detail) {
        Console.WriteLine(Stopwatch.GetTimestamp()+"\t"+Case+"\t"+Nonce+"\t"+kind+"\t"+detail);
        Console.Out.Flush();
    }
    static void Send(IntPtr h,string line) {
        byte[] b=Encoding.ASCII.GetBytes(line+"\n"); uint n;
        Check(WriteFile(h,b,(uint)b.Length,out n,IntPtr.Zero),"WriteFile");
        Require(n==b.Length,"short private pipe write");
    }
    static void Emit(string kind,string detail) {
        Send(GetStdHandle(-11),kind+"|"+Nonce+"|"+Case+"|"+Stopwatch.GetTimestamp()+"|"+detail);
    }
    sealed class Reader {
        public IntPtr Handle; public string Pending=""; public bool Eof;
        public Reader(IntPtr h) { Handle=h; }
        public string Poll() {
            int index=Pending.IndexOf('\n');
            if(index>=0) { string line=Pending.Substring(0,index); Pending=Pending.Substring(index+1); return line; }
            if(Eof) return null;
            uint available;
            if(!PeekNamedPipe(Handle,IntPtr.Zero,0,IntPtr.Zero,out available,IntPtr.Zero)) {
                int error=Marshal.GetLastWin32Error();
                if(error==109) { Eof=true; return null; }
                throw new Win32Exception(error,"PeekNamedPipe");
            }
            if(available==0) return null;
            Require(available<=8192 && Pending.Length<=8192,"private pipe bound");
            byte[] b=new byte[Math.Min(available,4096)]; uint n;
            Check(ReadFile(Handle,b,(uint)b.Length,out n,IntPtr.Zero),"ReadFile");
            Pending+=Encoding.ASCII.GetString(b,0,(int)n);
            return Poll();
        }
        public string Until(long deadline) {
            while(Clock.ElapsedMilliseconds<deadline) {
                string line=Poll(); if(line!=null) return line;
                Require(!Eof,"unexpected private EOF"); Thread.Sleep(5);
            }
            throw new TimeoutException("private pipe original deadline");
        }
    }
    static string[] Event(Reader r,long until) {
        string line=r.Until(until); string[] p=line.Split('|');
        Require(p.Length==5 && p[1]==Nonce && p[2]==Case,"private generation mismatch");
        long ticks; Require(Int64.TryParse(p[3],out ticks),"invalid event time");
        Log("HELPER_"+p[0],"qpc="+ticks+";"+p[4]); return p;
    }
    static void Ack(Reader input,string wanted) {
        Require(input.Until(Clock.ElapsedMilliseconds+7000)==wanted+"|"+Nonce+"|"+Case,"private ack mismatch");
    }
    static bool Member(IntPtr p,IntPtr job) { bool result; Check(IsProcessInJob(p,job,out result),"IsProcessInJob"); return result; }
    static void NoInherit(IntPtr h) { uint flags; Check(GetHandleInformation(h,out flags),"GetHandleInformation"); Require((flags&INHERIT)==0,"unexpected inheritable custody"); }
    static IntPtr Job(bool safety) {
        IntPtr h=CreateJobObjectW(IntPtr.Zero,IntPtr.Zero); Check(h!=IntPtr.Zero,"CreateJobObjectW");
        Jobs.Add(h); NoInherit(h);
        EXT_LIMIT limits=new EXT_LIMIT(); limits.basic.flags=safety?0x2000u:0u;
        Check(SetInformationJobObject(h,9,ref limits,Marshal.SizeOf(typeof(EXT_LIMIT))),"SetInformationJobObject");
        return h;
    }
    static PI Spawn(string mode,IntPtr input,IntPtr output,IntPtr safety,bool suspended) {
        // All command tokens except quoted executable/root are validated literals/nonce.
        Require(Root.IndexOf('"')<0 && Exe.IndexOf('"')<0,"unsafe executable/root");
        IntPtr size=IntPtr.Zero; InitializeProcThreadAttributeList(IntPtr.Zero,safety==IntPtr.Zero?1:2,0,ref size);
        Require(size!=IntPtr.Zero,"attribute size unavailable");
        IntPtr list=Marshal.AllocHGlobal(size), handles=IntPtr.Zero, jobs=IntPtr.Zero;
        bool initialized=false;
        try {
            Check(InitializeProcThreadAttributeList(list,safety==IntPtr.Zero?1:2,0,ref size),"InitializeProcThreadAttributeList"); initialized=true;
            handles=Marshal.AllocHGlobal(IntPtr.Size*2); Marshal.WriteIntPtr(handles,0,input); Marshal.WriteIntPtr(handles,IntPtr.Size,output);
            Check(UpdateProcThreadAttribute(list,0,new IntPtr(HANDLE_LIST),handles,new IntPtr(IntPtr.Size*2),IntPtr.Zero,IntPtr.Zero),"attribute HANDLE_LIST");
            if(safety!=IntPtr.Zero) {
                jobs=Marshal.AllocHGlobal(IntPtr.Size); Marshal.WriteIntPtr(jobs,safety);
                Check(UpdateProcThreadAttribute(list,0,new IntPtr(JOB_LIST),jobs,new IntPtr(IntPtr.Size),IntPtr.Zero,IntPtr.Zero),"attribute JOB_LIST");
            }
            SX sx=new SX(); sx.si.cb=Marshal.SizeOf(typeof(SX)); sx.si.flags=0x100;
            sx.si.input=input; sx.si.output=output; sx.si.error=output; sx.attrs=list;
            PI p;
            string command="\""+Exe+"\" "+mode+" "+Nonce+" "+Case+" \""+Root+"\"";
            Check(CreateProcessW(Exe,new StringBuilder(command),IntPtr.Zero,IntPtr.Zero,true,
                EXTENDED|UNICODE_ENV|(suspended?SUSPENDED:0),IntPtr.Zero,Root,ref sx,out p),"CreateProcessW "+mode);
            // Immediately retain actual creation handles; no PID reopening ever.
            Processes.Add(p.process); IO.Add(p.thread); NoInherit(p.process); NoInherit(p.thread);
            return p;
        } finally {
            if(initialized) DeleteProcThreadAttributeList(list);
            Marshal.FreeHGlobal(list); if(handles!=IntPtr.Zero) Marshal.FreeHGlobal(handles); if(jobs!=IntPtr.Zero) Marshal.FreeHGlobal(jobs);
        }
    }
    sealed class Child {
        public PI Pi; public IntPtr Input; public Reader Output;
    }
    static Child Leader(string mode,bool suspended) {
        SA sa=new SA(); sa.size=Marshal.SizeOf(typeof(SA)); sa.inherit=1;
        IntPtr ir,iw,or,ow;
        Check(CreatePipe(out ir,out iw,ref sa,4096),"CreatePipe stdin"); IO.Add(ir); IO.Add(iw);
        Check(CreatePipe(out or,out ow,ref sa,4096),"CreatePipe stdout"); IO.Add(or); IO.Add(ow);
        Check(SetHandleInformation(iw,INHERIT,0),"parent stdin noninherit");
        Check(SetHandleInformation(or,INHERIT,0),"parent stdout noninherit");
        PI p=Spawn(mode,ir,ow,Safety,suspended);
        CloseOwnedIO(ir); CloseOwnedIO(ow);
        Require(Member(p.process,Safety),"leader not in safety Job");
        Log("CREATED_LEADER","suspended="+suspended+";safety=true;handle="+p.process);
        return new Child { Pi=p,Input=iw,Output=new Reader(or) };
    }
    static void CloseOwnedIO(IntPtr h) { Check(CloseHandle(h),"CloseHandle IO"); IO.Remove(h); }
    static void Command(Child c,string value) { Send(c.Input,value+"|"+Nonce+"|"+Case); }
    static void Bind(IntPtr inner,Child c) {
        Log("ASSIGN_ATTEMPT","original_inner");
        Check(AssignProcessToJobObject(inner,c.Pi.process),"AssignProcessToJobObject");
        Log("ASSIGNED","original_inner");
        Require(Member(c.Pi.process,inner),"leader inner membership");
        Log("BOUND","appSession="+Nonce+";home=fixture-home;spawnCounter="+Case);
    }
    static void Resume(Child c) {
        Log("RESUME_ATTEMPT","original_thread");
        Require(ResumeThread(c.Pi.thread)==1,"ResumeThread unexpected/error="+Marshal.GetLastWin32Error());
        Log("RESUMED","original_thread");
    }
    static IntPtr Descendant(Child c,long until) {
        Require(Event(c.Output,until)[0]=="ENTRY","entry order");
        Require(Event(c.Output,until)[0]=="PRE","pre-creation order");
        Log("PRE_ACK","child creation permitted after private PRE"); Command(c,"CREATE");
        bool effect=false,created=false; IntPtr descendant=IntPtr.Zero;
        while(!effect || !created) {
            string[] p=Event(c.Output,until);
            if(p[0]=="EFFECT") { Require(!effect,"duplicate effect"); effect=true; }
            else if(p[0]=="CREATED") {
                Require(!created,"duplicate creation"); created=true;
                long value; Require(Int64.TryParse(p[4],out value) && value>0,"invalid source-bound handle");
                Check(DuplicateHandle(c.Pi.process,new IntPtr(value),GetCurrentProcess(),out descendant,
                    SYNCHRONIZE|QUERY|TERMINATE,false,0),"DuplicateHandle from original leader");
                Processes.Add(descendant); NoInherit(descendant);
                Log("DESCENDANT_HANDLE","noninherit=true;source=original_leader;handle="+descendant);
            } else throw new InvalidOperationException("unexpected descendant event "+p[0]);
        }
        Require(WaitForSingleObject(descendant,0)==WAIT_TIMEOUT,"descendant exited before membership");
        return descendant;
    }
    static void P01(bool negative) {
        Case=negative?"P01-negative":"P01-positive";
        long until=Clock.ElapsedMilliseconds+8000;
        IntPtr inner=Job(false); Child c=Leader("leader",true);
        if(!negative) Bind(inner,c);
        Resume(c);
        IntPtr d=Descendant(c,until);
        if(negative) Bind(inner,c); // Deliberately too late, despite final marker after this.
        bool inside=Member(d,inner),safe=Member(d,Safety);
        Log("MEMBERSHIP","inner="+inside+";safety="+safe+";live="+(WaitForSingleObject(d,0)==WAIT_TIMEOUT));
        Require(safe && inside==!negative,"membership does not establish intended control");
        Command(c,"FINAL"); Require(Event(c.Output,until)[0]=="FINAL","final marker order");
        Log("CONTAINMENT",negative?"REJECT":"PASS");
        CleanupCase(inner,c.Pi.process,d);
    }
    static bool Signaled(IntPtr p) {
        uint w=WaitForSingleObject(p,0);
        if(w==WAIT_OBJECT_0) return true;
        Require(w==WAIT_TIMEOUT,"wait unavailable/error="+Marshal.GetLastWin32Error()); return false;
    }
    static uint Code(IntPtr p) { uint code; Check(GetExitCodeProcess(p,out code),"GetExitCodeProcess"); return code; }
    static void WaitExit(IntPtr p,long until) {
        while(Clock.ElapsedMilliseconds<until) { if(Signaled(p)) return; Thread.Sleep(5); }
        throw new TimeoutException("original process exit observation unavailable");
    }
    static void P02(string variant) {
        Case="P02-"+variant; long until=Clock.ElapsedMilliseconds+8000;
        IntPtr inner=Job(false); Child c=Leader(variant,true); Bind(inner,c); Resume(c);
        IntPtr d=IntPtr.Zero;
        if(variant=="B") {
            d=Descendant(c,until); Require(Member(d,inner)&&Member(d,Safety),"B membership");
            Command(c,"EXIT"); WaitExit(c.Pi.process,until);
            string line=c.Output.Poll(); Require(line==null && !c.Output.Eof,"B pipe already EOF or unexpected event");
            Require(!Signaled(d),"B descendant no longer live");
            Log("OBSERVATION","leaderSignaled=true;exit="+Code(c.Pi.process)+";eof=false;descendantLive=true");
        } else {
            Require(Event(c.Output,until)[0]=="ENTRY","P02 entry");
            if(variant=="A") {
                while(!c.Output.Eof && Clock.ElapsedMilliseconds<until) { Require(c.Output.Poll()==null,"unexpected A event"); Thread.Sleep(5); }
                bool signaled=Signaled(c.Pi.process); uint code=Code(c.Pi.process);
                Log("OBSERVATION","leaderSignaled="+signaled+";exit="+code+";eof="+c.Output.Eof);
                Require(c.Output.Eof && !signaled,"A EOF versus exit not established");
            } else {
                WaitExit(c.Pi.process,until); uint code=Code(c.Pi.process);
                Log("OBSERVATION","leaderSignaled=true;exit="+code+";exit259IsExit=true");
                Require(code==259,"C real exit259 not established");
            }
        }
        Log("CASE","PASS"); CleanupCase(inner,c.Pi.process,d);
    }
    static uint Active(IntPtr job) {
        ACCOUNTING a; Check(QueryInformationJobObject(job,1,out a,Marshal.SizeOf(typeof(ACCOUNTING)),IntPtr.Zero),"Job accounting"); return a.active;
    }
    static void CleanupCase(IntPtr inner,IntPtr leader,IntPtr descendant) {
        Log("TERMINATE_ATTEMPT","original_inner");
        Check(TerminateJobObject(inner,70),"TerminateJobObject inner"); Log("TERMINATE_API","success;not_exit_proof");
        if(descendant!=IntPtr.Zero && !Member(descendant,inner)) {
            Log("TERMINATE_DESCENDANT_ATTEMPT","retained source-bound handle");
            Check(TerminateProcess(descendant,71),"TerminateProcess negative descendant");
        }
        long until=Clock.ElapsedMilliseconds+4000;
        WaitExit(leader,until); if(descendant!=IntPtr.Zero) WaitExit(descendant,until);
        while(Active(inner)!=0 && Clock.ElapsedMilliseconds<until) Thread.Sleep(5);
        Require(Active(inner)==0,"inner active count unknown/nonzero");
        Log("CASE_CLEANUP","leaderSignaled=true;descendantSignaled="+(descendant==IntPtr.Zero?"not_created":"true")+";innerActive=0");
    }
    static void Helper(string mode) {
        // Timer self-expiry is independent of private ack waits or host connection.
        Deadline=new Timer(delegate { ExitProcess(91); },null,12000,Timeout.Infinite);
        if(mode=="leaf") { Emit("EFFECT","invented-nonce-effect"); Thread.Sleep(11000); return; }
        if(mode=="A") {
            // Both standard outputs were assigned the same pipe. Close every
            // distinct helper-side reference before asking the parent for EOF.
            IntPtr output=GetStdHandle(-11),error=GetStdHandle(-12);
            Emit("ENTRY","helper-entry;stdout="+output+";stderr="+error);
            Check(CloseHandle(output),"close stdout");
            if(error!=output) Check(CloseHandle(error),"close stderr output alias");
            Thread.Sleep(11000); return;
        }
        Emit("ENTRY","helper-entry");
        if(mode=="C") { ExitProcess(259); return; }
        Reader input=new Reader(GetStdHandle(-10));
        Emit("PRE","before-actual-CreateProcessW"); Ack(input,"CREATE");
        PI child=Spawn("leaf",GetStdHandle(-10),GetStdHandle(-11),IntPtr.Zero,false);
        Emit("CREATED",child.process.ToInt64().ToString());
        if(mode=="B") { Ack(input,"EXIT"); ExitProcess(0); return; }
        Ack(input,"FINAL"); Emit("FINAL","late-marker"); Thread.Sleep(11000);
    }
    static void Identity() {
        ushort process,native; Check(IsWow64Process2(GetCurrentProcess(),out process,out native),"IsWow64Process2");
        SYSTEM_INFO si; GetNativeSystemInfo(out si);
        Log("IDENTITY","processMachine=0x"+process.ToString("x4")+";nativeMachine=0x"+native.ToString("x4")+
            ";nativeSystemArchitecture="+si.architecture+";pointerBytes="+IntPtr.Size+";runtime="+Environment.Version+
            ";os="+Environment.OSVersion+";stopwatchFrequency="+Stopwatch.Frequency+";launcherInJob="+Member(GetCurrentProcess(),IntPtr.Zero));
    }
    public static int Main(string[] args) {
        try {
            Require(args.Length==4,"expected mode nonce case root");
            Nonce=args[1]; Case=args[2]; Root=Path.GetFullPath(args[3]);
            Require(System.Text.RegularExpressions.Regex.IsMatch(Nonce,"^[a-f0-9]{32}$"),"nonce format");
            Require(System.Text.RegularExpressions.Regex.IsMatch(Case,"^[A-Za-z0-9-]{1,32}$"),"case format");
            Require(Path.GetFileName(Root)=="chirality-app-process-fixture-"+Nonce,"scratch leaf mismatch");
            Require(File.ReadAllText(Path.Combine(Root,"OWNER"))==Nonce,"ownership sentinel mismatch");
            Exe=typeof(ProcessFixture).Assembly.Location;
            Require(Path.GetDirectoryName(Exe)==Root,"executable outside owned root");
            foreach(string name in new string[]{"TEMP","TMP","CODEX_HOME"})
                Require(Environment.GetEnvironmentVariable(name)==Path.Combine(Root,name),"explicit scratch environment "+name);
            if(args[0]!="supervisor") { Require(args[0]=="leader"||args[0]=="leaf"||args[0]=="A"||args[0]=="B"||args[0]=="C","unknown helper"); Helper(args[0]); return 0; }
            Safety=Job(true);
            Deadline=new Timer(delegate { TerminateJobObject(Safety,92); ExitProcess(92); },null,80000,Timeout.Infinite);
            Identity();
            P01(false); P01(true); P02("A"); P02("B"); P02("C");
            Case="suite"; Log("SUITE","cases_complete"); return 0;
        } catch(Exception e) {
            if(Case==null) Case="startup";
            Log("REFUSAL",e.GetType().Name+":"+e.Message.Replace('\t',' ').Replace('\r',' ').Replace('\n',' ')); return 2;
        } finally {
            if(Safety!=IntPtr.Zero) {
                Case="suite";
                try {
                    Log("SAFETY_TERMINATE_ATTEMPT","original safety Job");
                    Check(TerminateJobObject(Safety,72),"TerminateJobObject safety");
                    long until=Clock.ElapsedMilliseconds+5000;
                    foreach(IntPtr p in Processes) WaitExit(p,until);
                    while(Active(Safety)!=0 && Clock.ElapsedMilliseconds<until) Thread.Sleep(5);
                    Require(Active(Safety)==0,"safety Job not observed empty"); CleanupObserved=true;
                    Log("SAFETY_CLEANUP","allRetainedHandlesSignaled=true;active=0");
                } catch(Exception e) { Log("CLEANUP_UNKNOWN",e.GetType().Name+":"+e.Message); }
                // Dispose watchdog only after cleanup attempt; crash/last-close still kills contained helpers.
                if(Deadline!=null) Deadline.Dispose();
                foreach(IntPtr h in IO) CloseHandle(h);
                foreach(IntPtr h in Processes) CloseHandle(h);
                foreach(IntPtr h in Jobs) CloseHandle(h);
                if(!CleanupObserved) ExitProcess(3);
            }
        }
    }
}
