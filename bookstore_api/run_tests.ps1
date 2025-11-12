# Run tests in an isolated mode by disabling pytest plugin autoload which can cause environment errors
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$outFile = Join-Path $env:TEMP 'bookstore_test_results.txt'
# Remove any stale test output files that pytest might try to collect
if (Test-Path .\test_results.txt) { Remove-Item .\test_results.txt -Force }
if (Test-Path .\test_results) { Remove-Item .\test_results -Force }
python -m pytest -q 2>&1 | Tee-Object -FilePath $outFile
if ($LASTEXITCODE -eq 0) {
    Write-Output "Tests passed. Results saved to $outFile"
} else {
    Write-Output "Some tests failed or there was an error. See $outFile"
}
