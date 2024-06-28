$serverJob = start-job -ScriptBlock {python server_entrypoint.py}
$clientJob1 = start-job -ScriptBlock {python client_entrypoint.py}
$clientJob2 = start-job -ScriptBlock {python client_entrypoint.py}

#kill -Name python

#($serverJob, $clientJob1, $clientJob2) | echo

[console]::TreatControlCAsInput = $true
while($true)
{
	if($Host.UI.RawUI.KeyAvailable -and (3 -eq [int]$Host.UI.RawUI.ReadKey("AllowCtrlC,IncludeKeyUp,NoEcho").Character))
	{
		echo "Stopping..."
		($serverJob, $clientJob1, $clientJob2) | stop-job
		break
	}
}
