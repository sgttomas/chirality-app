# Source input for inline/EncodedCommand transport only; never load as a .ps1.
# No invocation is authorized by loading this source. Namespace admission is
# separate. The watchdog runs emitted IL on a dedicated managed thread, without
# a PowerShell runspace, and terminates only its original root process.

function Initialize-FixtureController {
    if ([IntPtr]::Size -ne 8) { throw 'Fixture controller requires a 64-bit process.' }
    if ($ExecutionContext.SessionState.LanguageMode -ne 'FullLanguage') {
        throw 'Fixture controller requires FullLanguage.'
    }
    if ($null -ne $script:FixtureControllerNative) { return }

    $assemblyName = New-Object System.Reflection.AssemblyName
    $assemblyName.Name = 'FixtureController_' + [Guid]::NewGuid().ToString('N')
    $assembly = [AppDomain]::CurrentDomain.DefineDynamicAssembly(
        $assemblyName, [System.Reflection.Emit.AssemblyBuilderAccess]::Run)
    $module = $assembly.DefineDynamicModule($assemblyName.Name)
    $structAttributes = [System.Reflection.TypeAttributes]::Public -bor
        [System.Reflection.TypeAttributes]::Sealed -bor
        [System.Reflection.TypeAttributes]::SequentialLayout -bor
        [System.Reflection.TypeAttributes]::AnsiClass

    function New-FixtureLayout($name, $fields, $expectedSize, $offsets) {
        $builder = $module.DefineType($name, $structAttributes, [ValueType])
        foreach ($field in $fields.GetEnumerator()) {
            [void]$builder.DefineField($field.Key, [Type]$field.Value,
                [System.Reflection.FieldAttributes]::Public)
        }
        $type = $builder.CreateType()
        $size = [System.Runtime.InteropServices.Marshal]::SizeOf($type)
        if ($size -ne $expectedSize) {
            throw "$name has size $size; expected $expectedSize."
        }
        foreach ($field in $offsets.GetEnumerator()) {
            $actual = [System.Runtime.InteropServices.Marshal]::OffsetOf($type, $field.Key).ToInt64()
            if ($actual -ne $field.Value) {
                throw "$name.$($field.Key) has offset $actual; expected $($field.Value)."
            }
        }
        return $type
    }

    # Windows SDK field order, natural alignment, and 64-bit offsets. Pointer
    # fields are represented by IntPtr/UIntPtr; the native structures contain
    # pointers, not managed strings or automatically marshalled arrays.
    $si = New-FixtureLayout 'FIXTURE_STARTUPINFOW' ([ordered]@{
        cb=[UInt32]; reserved=[IntPtr]; desktop=[IntPtr]; title=[IntPtr]
        x=[UInt32]; y=[UInt32]; xSize=[UInt32]; ySize=[UInt32]
        xCountChars=[UInt32]; yCountChars=[UInt32]; fillAttribute=[UInt32]
        flags=[UInt32]; showWindow=[UInt16]; reserved2Length=[UInt16]
        reserved2=[IntPtr]; stdInput=[IntPtr]; stdOutput=[IntPtr]; stdError=[IntPtr]
    }) 104 ([ordered]@{
        cb=0; reserved=8; desktop=16; title=24; x=32; y=36; xSize=40; ySize=44
        xCountChars=48; yCountChars=52; fillAttribute=56; flags=60
        showWindow=64; reserved2Length=66; reserved2=72; stdInput=80
        stdOutput=88; stdError=96
    })
    $sx = New-FixtureLayout 'FIXTURE_STARTUPINFOEXW' ([ordered]@{
        startupInfo=$si; attributeList=[IntPtr]
    }) 112 ([ordered]@{ startupInfo=0; attributeList=104 })
    $pi = New-FixtureLayout 'FIXTURE_PROCESS_INFORMATION' ([ordered]@{
        process=[IntPtr]; thread=[IntPtr]; processId=[UInt32]; threadId=[UInt32]
    }) 24 ([ordered]@{ process=0; thread=8; processId=16; threadId=20 })
    $basic = New-FixtureLayout 'FIXTURE_JOB_BASIC_LIMIT_INFORMATION' ([ordered]@{
        perProcessUserTimeLimit=[Int64]; perJobUserTimeLimit=[Int64]
        limitFlags=[UInt32]; minimumWorkingSetSize=[UIntPtr]; maximumWorkingSetSize=[UIntPtr]
        activeProcessLimit=[UInt32]; affinity=[UIntPtr]; priorityClass=[UInt32]; schedulingClass=[UInt32]
    }) 64 ([ordered]@{
        perProcessUserTimeLimit=0; perJobUserTimeLimit=8; limitFlags=16
        minimumWorkingSetSize=24; maximumWorkingSetSize=32; activeProcessLimit=40
        affinity=48; priorityClass=56; schedulingClass=60
    })
    $io = New-FixtureLayout 'FIXTURE_IO_COUNTERS' ([ordered]@{
        readOperationCount=[UInt64]; writeOperationCount=[UInt64]; otherOperationCount=[UInt64]
        readTransferCount=[UInt64]; writeTransferCount=[UInt64]; otherTransferCount=[UInt64]
    }) 48 ([ordered]@{
        readOperationCount=0; writeOperationCount=8; otherOperationCount=16
        readTransferCount=24; writeTransferCount=32; otherTransferCount=40
    })
    $extended = New-FixtureLayout 'FIXTURE_JOB_EXTENDED_LIMIT_INFORMATION' ([ordered]@{
        basicLimitInformation=$basic; ioInfo=$io; processMemoryLimit=[UIntPtr]
        jobMemoryLimit=[UIntPtr]; peakProcessMemoryUsed=[UIntPtr]; peakJobMemoryUsed=[UIntPtr]
    }) 144 ([ordered]@{
        basicLimitInformation=0; ioInfo=64; processMemoryLimit=112
        jobMemoryLimit=120; peakProcessMemoryUsed=128; peakJobMemoryUsed=136
    })
    $accounting = New-FixtureLayout 'FIXTURE_JOB_BASIC_ACCOUNTING_INFORMATION' ([ordered]@{
        totalUserTime=[Int64]; totalKernelTime=[Int64]; thisPeriodTotalUserTime=[Int64]
        thisPeriodTotalKernelTime=[Int64]; totalPageFaultCount=[UInt32]; totalProcesses=[UInt32]
        activeProcesses=[UInt32]; totalTerminatedProcesses=[UInt32]
    }) 48 ([ordered]@{
        totalUserTime=0; totalKernelTime=8; thisPeriodTotalUserTime=16
        thisPeriodTotalKernelTime=24; totalPageFaultCount=32; totalProcesses=36
        activeProcesses=40; totalTerminatedProcesses=44
    })

    $nativeAttributes = [System.Reflection.TypeAttributes]::Public -bor
        [System.Reflection.TypeAttributes]::Abstract -bor [System.Reflection.TypeAttributes]::Sealed
    $native = $module.DefineType('FixtureNative', $nativeAttributes)
    $methodAttributes = [System.Reflection.MethodAttributes]::Public -bor
        [System.Reflection.MethodAttributes]::Static -bor [System.Reflection.MethodAttributes]::PinvokeImpl
    function Add-FixtureImport($name, [Type]$result, [Type[]]$parameters) {
        $method = $native.DefinePInvokeMethod($name, 'kernel32.dll', $name, $methodAttributes,
            [System.Reflection.CallingConventions]::Standard, $result, $parameters,
            [System.Runtime.InteropServices.CallingConvention]::Winapi,
            [System.Runtime.InteropServices.CharSet]::Unicode)
        $attribute = New-Object System.Reflection.Emit.CustomAttributeBuilder(
            [Runtime.InteropServices.DllImportAttribute].GetConstructor([Type[]]@([string])),
            [object[]]@('kernel32.dll'),
            [Reflection.FieldInfo[]]@([Runtime.InteropServices.DllImportAttribute].GetField('SetLastError')),
            [object[]]@($true))
        $method.SetCustomAttribute($attribute)
        $method.SetImplementationFlags($method.GetMethodImplementationFlags() -bor
            [System.Reflection.MethodImplAttributes]::PreserveSig)
    }
    # All reference/out native parameters are explicit pointers. The future
    # caller must allocate and initialize their buffers and retain ownership.
    Add-FixtureImport 'CreateJobObjectW' ([IntPtr]) ([Type[]]@([IntPtr],[IntPtr]))
    Add-FixtureImport 'SetInformationJobObject' ([Int32]) ([Type[]]@([IntPtr],[Int32],[IntPtr],[UInt32]))
    Add-FixtureImport 'QueryInformationJobObject' ([Int32]) ([Type[]]@([IntPtr],[Int32],[IntPtr],[UInt32],[IntPtr]))
    Add-FixtureImport 'GetHandleInformation' ([Int32]) ([Type[]]@([IntPtr],[IntPtr]))
    Add-FixtureImport 'InitializeProcThreadAttributeList' ([Int32]) ([Type[]]@([IntPtr],[Int32],[UInt32],[IntPtr]))
    Add-FixtureImport 'UpdateProcThreadAttribute' ([Int32]) ([Type[]]@([IntPtr],[UInt32],[IntPtr],[IntPtr],[UIntPtr],[IntPtr],[IntPtr]))
    Add-FixtureImport 'DeleteProcThreadAttributeList' ([Void]) ([Type[]]@([IntPtr]))
    Add-FixtureImport 'CreateProcessW' ([Int32]) ([Type[]]@([IntPtr],[IntPtr],[IntPtr],[IntPtr],[Int32],[UInt32],[IntPtr],[IntPtr],[IntPtr],[IntPtr]))
    Add-FixtureImport 'IsProcessInJob' ([Int32]) ([Type[]]@([IntPtr],[IntPtr],[IntPtr]))
    Add-FixtureImport 'ResumeThread' ([UInt32]) ([Type[]]@([IntPtr]))
    Add-FixtureImport 'WaitForSingleObject' ([UInt32]) ([Type[]]@([IntPtr],[UInt32]))
    Add-FixtureImport 'GetExitCodeProcess' ([Int32]) ([Type[]]@([IntPtr],[IntPtr]))
    Add-FixtureImport 'TerminateJobObject' ([Int32]) ([Type[]]@([IntPtr],[UInt32]))
    Add-FixtureImport 'CloseHandle' ([Int32]) ([Type[]]@([IntPtr]))
    Add-FixtureImport 'IsWow64Process2' ([Int32]) ([Type[]]@([IntPtr],[IntPtr],[IntPtr]))
    Add-FixtureImport 'GetCurrentProcess' ([IntPtr]) ([Type[]]@())
    Add-FixtureImport 'TerminateProcess' ([Int32]) ([Type[]]@([IntPtr],[UInt32]))
    Add-FixtureImport 'ExitProcess' ([Void]) ([Type[]]@([UInt32]))
    $nativeType = $native.CreateType()

    # A dedicated thread avoids PowerShell callbacks and thread-pool dependence.
    # It never accesses a Job handle, so cancellation cannot race handle reuse.
    # Killing this root closes its only non-inherited containment handle, even
    # if CreateProcessW is still blocked. No other process is reopened by PID.
    $watch = $module.DefineType('FixtureDeadline', $nativeAttributes)
    $watchClock = $watch.DefineField('Clock', [Diagnostics.Stopwatch], 'Public,Static')
    $watchLimit = $watch.DefineField('Limit', [long], 'Public,Static')
    $watchStop = $watch.DefineField('Stop', [Threading.ManualResetEvent], 'Public,Static')
    $run = $watch.DefineMethod('Run', 'Public,Static', [void], [Type[]]@())
    $il = $run.GetILGenerator()
    $loop = $il.DefineLabel(); $done = $il.DefineLabel(); $expired = $il.DefineLabel()
    $stopRequested = $il.DeclareLocal([bool])
    $il.MarkLabel($loop)
    $il.Emit([Reflection.Emit.OpCodes]::Ldsfld, $watchStop)
    $il.Emit([Reflection.Emit.OpCodes]::Ldc_I4, 10)
    $il.Emit([Reflection.Emit.OpCodes]::Callvirt, [Threading.WaitHandle].GetMethod('WaitOne',[Type[]]@([int])))
    $il.Emit([Reflection.Emit.OpCodes]::Stloc, $stopRequested)
    # The watchdog, not the cancelling PowerShell thread, decides whether a
    # stop acknowledgment preceded the original deadline. Check time AFTER
    # every wake, including a stop signal, before accepting cancellation.
    $il.Emit([Reflection.Emit.OpCodes]::Ldsfld, $watchClock)
    $il.Emit([Reflection.Emit.OpCodes]::Callvirt, [Diagnostics.Stopwatch].GetProperty('ElapsedMilliseconds').GetGetMethod())
    $il.Emit([Reflection.Emit.OpCodes]::Ldsfld, $watchLimit)
    $il.Emit([Reflection.Emit.OpCodes]::Bge, $expired)
    $il.Emit([Reflection.Emit.OpCodes]::Ldloc, $stopRequested)
    $il.Emit([Reflection.Emit.OpCodes]::Brtrue, $done)
    $il.Emit([Reflection.Emit.OpCodes]::Br, $loop)
    $il.MarkLabel($expired)
    $il.Emit([Reflection.Emit.OpCodes]::Call, $nativeType.GetMethod('GetCurrentProcess'))
    $il.Emit([Reflection.Emit.OpCodes]::Ldc_I4, 92)
    $il.Emit([Reflection.Emit.OpCodes]::Call, $nativeType.GetMethod('TerminateProcess'))
    $il.Emit([Reflection.Emit.OpCodes]::Pop)
    $il.Emit([Reflection.Emit.OpCodes]::Ldc_I4, 93)
    $il.Emit([Reflection.Emit.OpCodes]::Call, $nativeType.GetMethod('ExitProcess'))
    $il.MarkLabel($done); $il.Emit([Reflection.Emit.OpCodes]::Ret)
    $watchType = $watch.CreateType()
    $script:FixtureControllerWatchdog = $watchType

    # Publish only after every layout check and import definition succeeds.
    $script:FixtureControllerLayouts = @{
        StartupInfo=$si; StartupInfoEx=$sx; ProcessInformation=$pi
        BasicLimit=$basic; IoCounters=$io; ExtendedLimit=$extended; Accounting=$accounting
    }
    $script:FixtureControllerNative = $nativeType
}

function Invoke-FixtureContainedProcess {
    param(
        [Parameter(Mandatory=$true)][string]$Application,
        [Parameter(Mandatory=$true)][string]$CommandLine,
        [Parameter(Mandatory=$true)][byte[]]$EnvironmentBlock,
        [Parameter(Mandatory=$true)][string]$WorkingDirectory,
        [Parameter(Mandatory=$true)][long]$DeadlineMilliseconds
    )
    # This function is deliberately unreachable from run_fixture.py until the
    # namespace contract can admit every compiler open. It creates no pipes;
    # stdout capture for a future suite integration remains a separate repair.
    Initialize-FixtureController
    if ($DeadlineMilliseconds -lt 1 -or $DeadlineMilliseconds -gt 80000) { throw 'Deadline bound.' }
    if ($EnvironmentBlock.Length -lt 4 -or $EnvironmentBlock.Length -gt 65536 -or
        $EnvironmentBlock.Length % 2 -ne 0 -or
        ($EnvironmentBlock[-1] -bor $EnvironmentBlock[-2] -bor $EnvironmentBlock[-3] -bor $EnvironmentBlock[-4]) -ne 0) {
        throw 'Expected bounded double-NUL UTF-16 environment.'
    }
    if ($script:FixtureControllerActive) { throw 'Only one controller actor is supported.' }
    $script:FixtureControllerActive = $true
    $n = $script:FixtureControllerNative
    $w = $script:FixtureControllerWatchdog
    $clock = [Diagnostics.Stopwatch]::StartNew()
    $stop = New-Object Threading.ManualResetEvent($false)
    $w::Clock=$clock; $w::Limit=$DeadlineMilliseconds; $w::Stop=$stop
    $callback=[Delegate]::CreateDelegate([Threading.ThreadStart],$w.GetMethod('Run'))
    $watchdog=New-Object Threading.Thread($callback)
    $watchdog.IsBackground=$true
    $job=[IntPtr]::Zero; $process=[IntPtr]::Zero; $thread=[IntPtr]::Zero
    $attributes=[IntPtr]::Zero; $initialized=$false; $cleanup=$false
    $buffers=New-Object 'System.Collections.Generic.List[IntPtr]'
    function Allocate-FixtureBuffer([int]$size) {
        $p=[Runtime.InteropServices.Marshal]::AllocHGlobal($size)
        $buffers.Add($p)
        [Runtime.InteropServices.Marshal]::Copy((New-Object byte[] $size),0,$p,$size)
        return $p
    }
    function Check-FixtureApi([int]$ok,[string]$api) {
        if ($ok -eq 0) { throw "$api failed: $([Runtime.InteropServices.Marshal]::GetLastWin32Error())" }
    }
    function Assert-FixtureDeadline {
        if ($clock.ElapsedMilliseconds -ge $DeadlineMilliseconds) { throw 'Original guest deadline expired.' }
    }
    $watchdog.Start()
    try {
        $job=$n::CreateJobObjectW([IntPtr]::Zero,[IntPtr]::Zero)
        if ($job -eq [IntPtr]::Zero) { throw 'CreateJobObjectW failed.' }
        $flags=Allocate-FixtureBuffer 4
        Check-FixtureApi ($n::GetHandleInformation($job,$flags)) 'GetHandleInformation'
        if (([Runtime.InteropServices.Marshal]::ReadInt32($flags) -band 1) -ne 0) { throw 'Inheritable safety Job.' }
        $limit=Allocate-FixtureBuffer 144
        [Runtime.InteropServices.Marshal]::WriteInt32($limit,16,0x2000)
        Check-FixtureApi ($n::SetInformationJobObject($job,9,$limit,144)) 'Kill-on-close Job limit'
        $size=Allocate-FixtureBuffer 8
        [void]$n::InitializeProcThreadAttributeList([IntPtr]::Zero,1,0,$size)
        $bytes=[Runtime.InteropServices.Marshal]::ReadInt64($size)
        if ($bytes -le 0 -or $bytes -gt 65536) { throw 'Attribute list size bound.' }
        $attributes=Allocate-FixtureBuffer ([int]$bytes)
        Check-FixtureApi ($n::InitializeProcThreadAttributeList($attributes,1,0,$size)) 'InitializeProcThreadAttributeList'
        $initialized=$true
        $jobs=Allocate-FixtureBuffer 8
        [Runtime.InteropServices.Marshal]::WriteIntPtr($jobs,$job)
        Check-FixtureApi ($n::UpdateProcThreadAttribute($attributes,0,[IntPtr]0x2000D,$jobs,[UIntPtr]8,[IntPtr]::Zero,[IntPtr]::Zero)) 'Creation-time safety Job list'
        $startup=Allocate-FixtureBuffer 112
        [Runtime.InteropServices.Marshal]::WriteInt32($startup,0,112)
        [Runtime.InteropServices.Marshal]::WriteIntPtr($startup,104,$attributes)
        $pi=Allocate-FixtureBuffer 24
        $env=Allocate-FixtureBuffer $EnvironmentBlock.Length
        [Runtime.InteropServices.Marshal]::Copy($EnvironmentBlock,0,$env,$EnvironmentBlock.Length)
        $app=[Runtime.InteropServices.Marshal]::StringToHGlobalUni($Application); $buffers.Add($app)
        $cmd=[Runtime.InteropServices.Marshal]::StringToHGlobalUni($CommandLine); $buffers.Add($cmd)
        $cwd=[Runtime.InteropServices.Marshal]::StringToHGlobalUni($WorkingDirectory); $buffers.Add($cwd)
        Assert-FixtureDeadline
        # CREATE_SUSPENDED | EXTENDED_STARTUPINFO_PRESENT | CREATE_UNICODE_ENVIRONMENT
        # No inheritance, no breakaway, no run-then-assign interval.
        Check-FixtureApi ($n::CreateProcessW($app,$cmd,[IntPtr]::Zero,[IntPtr]::Zero,0,0x80404,$env,$cwd,$startup,$pi)) 'CreateProcessW'
        $process=[Runtime.InteropServices.Marshal]::ReadIntPtr($pi,0)
        $thread=[Runtime.InteropServices.Marshal]::ReadIntPtr($pi,8)
        $member=Allocate-FixtureBuffer 4
        Check-FixtureApi ($n::IsProcessInJob($process,$job,$member)) 'IsProcessInJob'
        if ([Runtime.InteropServices.Marshal]::ReadInt32($member) -ne 1) { throw 'Missing creation-time membership.' }
        Assert-FixtureDeadline
        if ($n::ResumeThread($thread) -ne 1) { throw 'ResumeThread failed or unexpected count.' }
        do {
            Assert-FixtureDeadline
            $wait=$n::WaitForSingleObject($process,10)
            if ($wait -ne 0 -and $wait -ne 258) { throw 'Original process wait failed.' }
        } while ($wait -eq 258)
        $exit=Allocate-FixtureBuffer 4
        Check-FixtureApi ($n::GetExitCodeProcess($process,$exit)) 'GetExitCodeProcess'
        $result=[ordered]@{originalHandleSignaled=$true; exitCode=[BitConverter]::ToUInt32([BitConverter]::GetBytes([Runtime.InteropServices.Marshal]::ReadInt32($exit)),0); creationSafetyMembership=$true}
    } finally {
        # Native API success alone is never cleanup. Keep the watchdog live and
        # every original handle owned until both original HANDLE signaling and
        # authoritative Job active zero are observed within the same deadline.
        if ($job -ne [IntPtr]::Zero) {
            try {
                Check-FixtureApi ($n::TerminateJobObject($job,72)) 'TerminateJobObject'
                $accounting=Allocate-FixtureBuffer 48
                do {
                    Assert-FixtureDeadline
                    $signaled=($process -eq [IntPtr]::Zero -or $n::WaitForSingleObject($process,0) -eq 0)
                    Check-FixtureApi ($n::QueryInformationJobObject($job,1,$accounting,48,[IntPtr]::Zero)) 'Job accounting'
                    $active=[Runtime.InteropServices.Marshal]::ReadInt32($accounting,40)
                    if (-not $signaled -or $active -ne 0) { [Threading.Thread]::Sleep(10) }
                } while (-not $signaled -or $active -ne 0)
                Assert-FixtureDeadline
                $cleanup=$true
            } catch {
                # Unknown: root termination closes the last Job handle; actual
                # last-close cleanup remains unobserved. Never continue a suite.
                [void]$n::TerminateProcess($n::GetCurrentProcess(),94)
                $n::ExitProcess(95)
            }
        } else { $cleanup=$true }
        if ($cleanup) {
            if ($clock.ElapsedMilliseconds -ge $DeadlineMilliseconds) {
                [void]$n::TerminateProcess($n::GetCurrentProcess(),94); $n::ExitProcess(95)
            }
            [void]$stop.Set()
            if (-not $watchdog.Join(1000)) { [void]$n::TerminateProcess($n::GetCurrentProcess(),96); $n::ExitProcess(97) }
            if ($initialized) { $n::DeleteProcThreadAttributeList($attributes) }
            foreach ($h in @($thread,$process,$job)) {
                if ($h -ne [IntPtr]::Zero) { Check-FixtureApi ($n::CloseHandle($h)) 'CloseHandle' }
            }
            foreach ($p in $buffers) { [Runtime.InteropServices.Marshal]::FreeHGlobal($p) }
            $stop.Dispose(); $script:FixtureControllerActive=$false
        }
    }
    $result.cleanup='original process signaled; Job active=0'
    return $result
}
