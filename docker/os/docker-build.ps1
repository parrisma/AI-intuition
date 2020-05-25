param (
    [String[]]$BuildFiles = @(),
    [switch]$Interactive,
    [switch]$All,
    [switch]$NoCache
)

. ..\..\ps1\GlobalDefaults.ps1
. ..\..\ps1\BuildDockerFile.ps1

#
# Estbalish list of dirs to process. If -All then recurse down. Always add current dir [.] as first
# dir to process.
#
$all_dirs = @()
$all_dirs += "."
if ($All)
{
    if ($BuildFiles.Count -gt 0)
    {
        Write-Output "** WARNING :: Mode [-All] selected any specified [-BuildFiles] will be ignored"
    }

    $dirs = Get-ChildItem -Directory -Recurse "."
    foreach ($d in $dirs)
    {
        Write-Output $d.FullName
        $all_dirs += $d.FullName
    }
    #
    # Iterate all directories starting at the top and working down
    #
    foreach ($build_dir in $all_dirs)
    {
        Write-Output "Processing build-<?>.csv files in location [$build_dir]"
        $BuildFiles = @()
        $files = Get-ChildItem -Path "$build_dir" -Filter "build-*.csv"
        if ($files.Length -gt 0)
        {
            foreach ($f in $files)
            {
                Write-Output $f.FullName
                $BuildFiles += $f.FullName
            }
            BuildDockerFiles -BuildFiles $BuildFiles -Location $build_dir -Interactive $Interactive -NoCache $NoCache
            Write-Output "Done in location [$build_dir]"
        }
        else
        {
            Write-Output "Nothing to process in location [$build_dir]"
        }
    }
}
else
{
    if ($BuildFiles.Count -eq 0)
    {
        Write-Output "Processing all build files in current diractory"
        $files = Get-ChildItem -Path "$build_dir" -Filter "build-*.csv"
        foreach ($f in $files)
        {
            $BuildFiles += $f.FullName
        }
    }
    else
    {
        Write-Output "Processing Specified build files."
    }
    BuildDockerFiles -BuildFiles $BuildFiles -Location "." -Interactive $Interactive -NoCache $NoCache
    Write-Output "Done"
}