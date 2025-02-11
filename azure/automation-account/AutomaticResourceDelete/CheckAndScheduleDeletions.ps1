Param(
    [string] $vaultName,
    [string] $secretName,
    [string] $fromEmail,
    [string] $toEmail
)

# Authenticate to Azure using Managed Identity
$AzureContext = (Connect-AzAccount -Identity).Context
Set-AzContext -SubscriptionId $AzureContext.Subscription.Id | Out-Null

# Get the current date and time
$currentDate = Get-Date

# Get all resource groups in the subscription
$resourceGroups = Get-AzResourceGroup

foreach ($resourceGroup in $resourceGroups) {
    $resourceGroupName = $resourceGroup.ResourceGroupName

    # Get all resources in the resource group
    $resources = Get-AzResource -ResourceGroupName $resourceGroupName
    $allResourcesDeleted = $true

    foreach ($resource in $resources) {
        # Check if Tags property exists and contains the necessary tags
        if ($resource.Tags -and $resource.Tags.ContainsKey("CreatedOnDate") -and -not $resource.Tags.ContainsKey("ExcludeFromDeletion")) {
            $createdOnDate = $resource.Tags["CreatedOnDate"]
            $deletionTime = if ($resource.Tags.ContainsKey("ScheduledDeletion")) { $resource.Tags["ScheduledDeletion"] } else { $null }

            if ($createdOnDate) {
                $resourceCreatedDate = [datetime]::Parse($createdOnDate)
                $ageInMinutes = ($currentDate - $resourceCreatedDate).TotalMinutes

                if ($deletionTime) {
                    $scheduledDeletion = [datetime]::Parse($deletionTime)
                    if ($currentDate -ge $scheduledDeletion) {
                        # Delete resource
                        Remove-AzResource -ResourceId $resource.ResourceId -Force
                        Write-Output "Deleted resource: $($resource.Name)"
                    } else {
                        $allResourcesDeleted = $false
                    }
                } elseif ($ageInMinutes -gt 10) {
                    # Schedule deletion
                    $scheduledDeletion = $currentDate.AddMinutes(10)
                    $resource | Set-AzResource -Tag @{ "ScheduledDeletion" = $scheduledDeletion.ToString("o") } -Force
                    Write-Output "Scheduled deletion for resource: $($resource.Name) at $scheduledDeletion."

                    # Start Runbook 2 to send email notification
                    Start-AzAutomationRunbook -AutomationAccountName "yourAutomationAccountName" -ResourceGroupName "yourResourceGroupName" -Name "SendEmailNotification" -Parameters @{
                        "resourceName" = $resource.Name
                        "resourceGroupName" = $resourceGroupName
                        "deletionTime" = $scheduledDeletion
                        "vaultName" = $vaultName
                        "secretName" = $secretName
                        "fromEmail" = $fromEmail
                        "toEmail" = $toEmail
                    }

                    $allResourcesDeleted = $false
                } else {
                    $allResourcesDeleted = $false
                }
            } else {
                $allResourcesDeleted = $false
            }
        } else {
            $allResourcesDeleted = $false
        }
    }

    if ($allResourcesDeleted) {
        # Delete resource group
        Remove-AzResourceGroup -Name $resourceGroupName -Force
        Write-Output "Deleted resource group: $resourceGroupName"
    }
}
