Param(
    [string] $resourceName,
    [string] $resourceGroupName,
    [datetime] $deletionTime,
    [string] $vaultName,
    [string] $secretName,
    [string] $fromEmail,
    [string] $toEmail
)

# Authenticate to Azure using Managed Identity
$AzureContext = (Connect-AzAccount -Identity).Context
Set-AzContext -SubscriptionId $AzureContext.Subscription.Id | Out-Null

# Retrieve SendGrid API Key from Azure Key Vault
$sendGridApiKeySecret = Get-AzKeyVaultSecret -VaultName $vaultName -Name $secretName
$sendGridApiKey = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($sendGridApiKeySecret.SecretValue))

# Define the email notification function
function Send-EmailNotification($resourceName, $resourceGroupName, $deletionTime) {
    $emailBody = "Resource $resourceName in resource group $resourceGroupName will be deleted at $deletionTime. To prevent deletion, remove or update the 'ScheduledDeletion' tag."
    
    # Create email body
    $emailContent = @{
        personalizations = @(@{ to = @(@{ email = $toEmail }) })
        from = @{ email = $fromEmail }
        subject = "Resource Deletion Notification"
        content = @(@{ type = "text/plain"; value = $emailBody })
    } | ConvertTo-Json
    
    # Send email using SendGrid API
    Invoke-RestMethod -Uri "https://api.sendgrid.com/v3/mail/send" -Method Post -Headers @{ Authorization = "Bearer $sendGridApiKey" } -Body $emailContent
    Write-Output "Email notification sent for resource $resourceName."
}

# Send the email notification
Send-EmailNotification -resourceName $resourceName -resourceGroupName $resourceGroupName -deletionTime $deletionTime
