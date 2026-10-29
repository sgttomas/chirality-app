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
    static SingleRead ARead;
    static readonly string CloseFile="P02-A-close.txt";
    const string ASetup="post-managed-start-stdout/v1";
    const uint FILE_TYPE_PIPE=3;

    // A alone: one synchronous read on the actual stdout reader. No Poll or
    // CloseHandle may touch this handle until Thread.Join proves completion.
    sealed class SingleRead {
        public IntPtr Handle;
        public Thread Worker;
        public bool Started,Ok;
        public uint Count;
        public int Error;
        public long Qpc,CompletedMs;
        public string Failure;
        public SingleRead(IntPtr handle) { Handle=handle; }
        public void Start() {
            Worker=new Thread(delegate() {
                try {
                    byte[] b=new byte[1];
                    Ok=ReadFile(Handle,b,1,out Count,IntPtr.Zero);
                    Error=Marshal.GetLastWin32Error(); // immediately; meaningful only if !Ok
                    Qpc=Stopwatch.GetTimestamp(); CompletedMs=Clock.ElapsedMilliseconds;
                } catch(Exception e) { Failure=e.GetType().Name; }
            });
            Worker.IsBackground=true; Worker.Start(); Started=true;
        }
        public bool Join(int ms) { return !Started || Worker.Join(ms); }
        public bool Eof { get { return Started && Failure==null && !Ok && Error==109 && Count==0; } }
        public string Result() {
            return "ok="+Ok+";bytes="+Count+";error="+Error+";qpc="+Qpc+
                ";completedMs="+CompletedMs+";workerStarted="+Started+";workerJoined=True;failure="+(Failure??"none");
        }
    }

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
    [DllImport("kernel32.dll", SetLastError=true)] static extern bool SetStdHandle(int kind,IntPtr handle);
    [DllImport("kernel32.dll", SetLastError=true)] static extern uint GetFileType(IntPtr handle);
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
    static long Number(string value) {
        long n;
        Require(Int64.TryParse(value,System.Globalization.NumberStyles.None,
            System.Globalization.CultureInfo.InvariantCulture,out n) && n.ToString()==value,"invalid diagnostic number");
        return n;
    }
    static bool Boolean(string value) {
        Require(value=="True" || value=="False","invalid diagnostic boolean"); return value=="True";
    }
    static string[] AFields(string detail,string keys) {
        string[] parts=detail.Split(';'),names=keys.Split(' '),values=new string[parts.Length];
        Require(parts.Length==names.Length,"A field count");
        for(int i=0;i<parts.Length;i++) {
            Require(parts[i].StartsWith(names[i]+"=",StringComparison.Ordinal),"A field name/order");
            values[i]=parts[i].Substring(names[i].Length+1);
        }
        return values;
    }
    static Reader CurrentStdoutA(Child c,long until,out string[] entry) {
        string[] control=Event(c.Output,until);
        Require(control[0]=="A_PIPE","A expected startup control frame");
        string[] p=AFields(control[4],"setup sourceRead sourceWrite startupStdin startupStdout startupStderr readNoninherit writeNoninherit pipeType");
        Require(p[0]==ASetup && p[6]=="True" && p[7]=="True" && Number(p[8])==FILE_TYPE_PIPE,"A pipe setup/version");
        long read=Number(p[1]),write=Number(p[2]);
        Require(read>0 && write>0 && read!=write,"A pipe pair");
        for(int i=3;i<=5;i++) Require(Number(p[i])>0 && p[i]!=p[1] && p[i]!=p[2],"A pipe was startup stdio");
        Require(c.Output.Pending.Length==0 && !c.Output.Eof,"A extra startup control bytes");
        IntPtr copy;
        // The retained original leader is the source authority, never a PID.
        Check(DuplicateHandle(c.Pi.process,new IntPtr(read),GetCurrentProcess(),out copy,0,false,2),"A DuplicateHandle reader SAME_ACCESS");
        IO.Add(copy); NoInherit(copy); uint readerType=GetFileType(copy);
        Require(readerType==FILE_TYPE_PIPE,"A duplicated reader not PIPE");
        Log("A_PIPE_READER","setup="+ASetup+";sourceLeaderHandle="+c.Pi.process+";sourceRead="+read+
            ";sourceWrite="+write+";handle="+copy+";noninherit=True;pipeType="+readerType+";sameAccess=True");
        long ackSentQpc=Stopwatch.GetTimestamp();
        Log("A_PIPE_ACK","sourceLeaderHandle="+c.Pi.process+";reader="+copy+";ownershipEstablished=True");
        Command(c,"STDOUT-OWNED");
        // Keep c.Output and its original startup HANDLE owned, with no further
        // reads. Only the transferred reader may supply the current-stdout ENTRY.
        Reader output=new Reader(copy); entry=Event(output,until);
        Require(entry[0]=="ENTRY","A current stdout ENTRY");
        string[] bound=AFields(entry[4],"setup stdout sourceRead ackQpc readCloseQpc bindQpc setOk getMatch pipeType startupStdout startupStderr");
        Require(bound[0]==ASetup && bound[1]==p[2] && bound[2]==p[1] && bound[6]=="True" &&
            bound[7]=="True" && Number(bound[8])==FILE_TYPE_PIPE && bound[9]==p[4] && bound[10]==p[5],"A actual stdout binding mismatch");
        Require(Number(control[3])<=ackSentQpc && ackSentQpc<=Number(bound[3]) && Number(bound[3])<=Number(bound[4]) &&
            Number(bound[4])<=Number(bound[5]) && Number(bound[5])<=Number(entry[3]) &&
            Number(entry[3])<=Stopwatch.GetTimestamp(),"A source binding time order");
        return output;
    }
    static bool CloseConfirmation(string[] entry,out long attemptQpc) {
        attemptQpc=0;
        string raw;
        try {
            // Writer used CreateNew/FileShare.None. This succeeds only after its
            // bounded write/flush/close; never accept a concurrently partial file.
            using(FileStream f=new FileStream(Path.Combine(Root,CloseFile),FileMode.Open,FileAccess.Read,FileShare.None)) {
                Require(f.Length>0 && f.Length<=512,"A close metadata size");
                byte[] bytes=new byte[(int)f.Length]; int offset=0,n;
                while(offset<bytes.Length && (n=f.Read(bytes,offset,bytes.Length-offset))>0) offset+=n;
                Require(offset==bytes.Length && f.ReadByte()==-1,"A close metadata incomplete");
                foreach(byte b in bytes) Require(b<128,"A close metadata non-ASCII");
                raw=Encoding.ASCII.GetString(bytes);
            }
        } catch(FileNotFoundException) { return false; }
        catch(IOException e) {
            if((e.HResult&0xffff)==32) return false; // exclusive writer still owns file
            throw;
        }
        Require(raw.EndsWith("|COMPLETE\n",StringComparison.Ordinal),"A close metadata unfinished");
        string[] p=raw.Substring(0,raw.Length-1).Split('|');
        Require(p.Length==13 && p[0]=="CLOSE" && p[1]==Nonce && p[2]=="P02-A" && p[4]==ASetup && p[12]=="COMPLETE","A close metadata fields/generation");
        long qpc=Number(p[3]),output=Number(p[5]),sourceRead=Number(p[6]),bindQpc=Number(p[7]),entryQpc=Number(p[8]);
        attemptQpc=Number(p[9]); bool outputOk=Boolean(p[10]); long outputError=Number(p[11]);
        string[] bound=AFields(entry[4],"setup stdout sourceRead ackQpc readCloseQpc bindQpc setOk getMatch pipeType startupStdout startupStderr");
        Require(output>0 && sourceRead>0 && outputError<=Int32.MaxValue,"A close metadata handle/error");
        Require(p[5]==bound[1] && p[6]==bound[2] && p[7]==bound[5] && p[8]==entry[3],"A close metadata binding mismatch");
        Require(entryQpc<=attemptQpc && attemptQpc<=qpc && qpc<=Stopwatch.GetTimestamp(),"A post-close time invalid");
        Log("A_CLOSE_CONFIRMATION","qpc="+qpc+";setup="+ASetup+";stdout="+output+";sourceRead="+sourceRead+
            ";bindQpc="+bindQpc+";entryQpc="+entryQpc+";attemptQpc="+attemptQpc+";stdoutOk="+outputOk+";stdoutError="+outputError+";writeComplete=True");
        Require(outputOk,"A helper output close failed");
        return true;
    }
    static void ObserveA(Child c,Reader output,string[] entry,long until,long untilQpc) {
        Require(output.Pending.Length==0,"A pending partial/extra bytes after ENTRY");
        Require(!output.Eof,"A EOF before direct read");
        ARead=new SingleRead(output.Handle);
        Log("A_READ_START","handle="+output.Handle+";leaderHandle="+c.Pi.process+
            ";untilMs="+until+";untilQpc="+untilQpc+";pendingBytes=0;length=1");
        ARead.Start();
        bool closed=false,joined=false; long closeAttemptQpc=0;
        while(Clock.ElapsedMilliseconds<until && Stopwatch.GetTimestamp()<untilQpc) {
            if(!closed) closed=CloseConfirmation(entry,out closeAttemptQpc);
            joined=ARead.Join(0);
            if(joined) {
                Log("A_READ_RESULT",ARead.Result());
                Require(ARead.Eof,"A direct read not FALSE/109: "+ARead.Result());
                if(closed) break;
                // Log the result only once, after joining; await metadata below.
                while(!closed && Clock.ElapsedMilliseconds<until && Stopwatch.GetTimestamp()<untilQpc) {
                    closed=CloseConfirmation(entry,out closeAttemptQpc); if(!closed) Thread.Sleep(5);
                }
                break;
            }
            Thread.Sleep(5);
        }
        if(!joined) Log("A_READ_PENDING","atOriginalDeadline=True;joined=False");
        bool eof=closed && joined && ARead.Eof && ARead.Qpc>=closeAttemptQpc && ARead.CompletedMs<until && ARead.Qpc<untilQpc;
        bool signaled=Signaled(c.Pi.process); uint code=Code(c.Pi.process);
        long observed=Stopwatch.GetTimestamp();
        Log("A_READ_PROOF","closeConfirmed="+closed+";workerJoined="+joined+";beforeDeadline="+
            (Clock.ElapsedMilliseconds<until && observed<untilQpc)+";originalLeaderHandle="+c.Pi.process);
        Log("OBSERVATION","leaderSignaled="+signaled+";exit="+code+";eof="+eof);
        Require(closed && eof && !signaled && code==259 && Clock.ElapsedMilliseconds<until && observed<untilQpc,
            "A live EOF/post-close proof not established by original deadline");
    }
    static void P02(string variant) {
        Case="P02-"+variant; long startQpc=Stopwatch.GetTimestamp(),until=Clock.ElapsedMilliseconds+8000;
        long untilQpc=startQpc+8*Stopwatch.Frequency; // additional strict bound; never extends original until
        if(variant=="A") {
            Log("A_DEADLINE","startQpc="+startQpc+";untilQpc="+untilQpc+";startMs="+(until-8000)+
                ";untilMs="+until+";frequency="+Stopwatch.Frequency);
            Require(!File.Exists(Path.Combine(Root,CloseFile)) && !Directory.Exists(Path.Combine(Root,CloseFile)),"A stale close metadata");
        }
        IntPtr inner=Job(false); Child c=Leader(variant,true); Bind(inner,c); Resume(c);
        IntPtr d=IntPtr.Zero;
        if(variant=="B") {
            d=Descendant(c,until); Require(Member(d,inner)&&Member(d,Safety),"B membership");
            Command(c,"EXIT"); WaitExit(c.Pi.process,until);
            string line=c.Output.Poll(); Require(line==null && !c.Output.Eof,"B pipe already EOF or unexpected event");
            Require(!Signaled(d),"B descendant no longer live");
            Log("OBSERVATION","leaderSignaled=true;exit="+Code(c.Pi.process)+";eof=false;descendantLive=true");
        } else if(variant=="A") {
            string[] entry; Reader output=CurrentStdoutA(c,until,out entry);
            ObserveA(c,output,entry,until,untilQpc);
        } else {
            string[] entry=Event(c.Output,until); Require(entry[0]=="ENTRY","P02 entry");
            WaitExit(c.Pi.process,until); uint code=Code(c.Pi.process);
            Log("OBSERVATION","leaderSignaled=true;exit="+code+";exit259IsExit=true");
            Require(code==259,"C real exit259 not established");
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
            IntPtr startupInput=GetStdHandle(-10),startupOutput=GetStdHandle(-11),startupError=GetStdHandle(-12);
            SA sa=new SA(); sa.size=Marshal.SizeOf(typeof(SA)); // inherit=0, after managed startup
            IntPtr read,output;
            Check(CreatePipe(out read,out output,ref sa,4096),"A fresh CreatePipe");
            NoInherit(read); NoInherit(output);
            uint readType=GetFileType(read),writeType=GetFileType(output);
            Require(readType==FILE_TYPE_PIPE && writeType==FILE_TYPE_PIPE,"A fresh pair not PIPE");
            foreach(IntPtr old in new IntPtr[]{startupInput,startupOutput,startupError})
                Require(read!=old && output!=old,"A fresh pipe aliases startup stdio");
            Emit("A_PIPE","setup="+ASetup+";sourceRead="+read+";sourceWrite="+output+
                ";startupStdin="+startupInput+";startupStdout="+startupOutput+";startupStderr="+startupError+
                ";readNoninherit=True;writeNoninherit=True;pipeType="+writeType);
            Ack(new Reader(startupInput),"STDOUT-OWNED"); long ackQpc=Stopwatch.GetTimestamp();
            Check(CloseHandle(read),"A close handed-off source reader"); long readCloseQpc=Stopwatch.GetTimestamp();
            Check(SetStdHandle(-11,output),"A SetStdHandle stdout");
            IntPtr boundOutput=GetStdHandle(-11); uint boundType=GetFileType(boundOutput);
            Require(boundOutput==output && boundType==FILE_TYPE_PIPE,"A actual stdout slot mismatch");
            long bindQpc=Stopwatch.GetTimestamp(),entryQpc=Stopwatch.GetTimestamp();
            // Raw WriteFile through a newly queried actual Win32 stdout. This
            // deliberately makes no claim about Console.Out's cached old stream.
            Send(GetStdHandle(-11),"ENTRY|"+Nonce+"|"+Case+"|"+entryQpc+"|setup="+ASetup+
                ";stdout="+output+";sourceRead="+read+";ackQpc="+ackQpc+";readCloseQpc="+readCloseQpc+
                ";bindQpc="+bindQpc+";setOk=True;getMatch=True;pipeType="+boundType+";startupStdout="+startupOutput+";startupStderr="+startupError);
            // The only new writer is closed exactly once. Startup stdout/stderr
            // remain control references until helper death; no old-pipe EOF claim.
            long attemptQpc=Stopwatch.GetTimestamp();
            bool outputOk=CloseHandle(output); int outputError=Marshal.GetLastWin32Error();
            if(outputOk) outputError=0; // Win32 last error is undefined on success
            long qpc=Stopwatch.GetTimestamp();
            try {
                string record="CLOSE|"+Nonce+"|"+Case+"|"+qpc+"|"+ASetup+"|"+output+"|"+read+"|"+
                    bindQpc+"|"+entryQpc+"|"+attemptQpc+"|"+outputOk+"|"+outputError+"|COMPLETE\n";
                byte[] bytes=Encoding.ASCII.GetBytes(record); Require(bytes.Length<=512,"A close metadata bound");
                using(FileStream f=new FileStream(Path.Combine(Root,CloseFile),FileMode.CreateNew,FileAccess.Write,FileShare.None)) {
                    f.Write(bytes,0,bytes.Length); f.Flush();
                }
            } catch { ExitProcess(93); return; } // never try logging through closed stdout
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
                    Require(Active(Safety)==0,"safety Job not observed empty");
                    long deathProofQpc=Stopwatch.GetTimestamp();
                    Log("SAFETY_CLEANUP","allRetainedHandlesSignaled=true;active=0");
                    if(ARead!=null) {
                        int remaining=(int)Math.Max(0,Math.Min(2000,until-Clock.ElapsedMilliseconds));
                        Require(ARead.Join(remaining),"A read worker completion UNKNOWN after owned-writer death; handle retained");
                        Log("A_READ_CLEANUP",ARead.Result()+";deathProofQpc="+deathProofQpc+
                            ";eofAfterDeathProof="+(ARead.Eof && ARead.Qpc>=deathProofQpc)+
                            ";liveEofOutcomeUnchanged=True");
                    }
                    CleanupObserved=true;
                } catch(Exception e) { Log("CLEANUP_UNKNOWN",e.GetType().Name+":"+e.Message); }
                // Unknown process/I/O teardown: exit this controller, retaining
                // pending read HANDLEs until process death. No concurrent close,
                // cancellation, cold thread lookup or arbitrary PID operation.
                if(!CleanupObserved) { TerminateJobObject(Safety,73); ExitProcess(3); }
                // Dispose watchdog only after cleanup attempt; crash/last-close still kills contained helpers.
                if(Deadline!=null) Deadline.Dispose();
                foreach(IntPtr h in IO) CloseHandle(h);
                foreach(IntPtr h in Processes) CloseHandle(h);
                foreach(IntPtr h in Jobs) CloseHandle(h);
            }
        }
    }
}
