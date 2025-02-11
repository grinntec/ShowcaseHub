<#
.SYNOPSIS
    Sends an email using the SendGrid API via Azure Automation.

.DESCRIPTION
    This script sends an email by interfacing with the SendGrid API. It retrieves
    the SendGrid API key from Azure Key Vault and leverages Azure Automation's 
    system-assigned managed identity for secure authentication. The documentation 
    below outlines the required parameters and provides an example of usage.

.PARAMETER destEmailAddress
    Specifies the recipient email address.

.PARAMETER fromEmailAddress
    Specifies the sender email address.

.PARAMETER subject
    Specifies the subject line of the email.

.PARAMETER content
    Contains the body content of the email.

.EXAMPLE
    Send-EmailViaSendGrid -destEmailAddress "recipient@example.com" `
                         -fromEmailAddress "sender@example.com" `
                         -subject "Test Email" `
                         -content "This is a sample email message."

.REMARKS
    - Ensure the Azure Key Vault is configured with the SendGrid API key.
    - The script depends on a system-assigned managed identity for authentication.
    - For improved robustness, consider adding parameter validation and error handling.
#>

Param(
    [Parameter(Mandatory = $true)]
    [string] $destEmailAddress,

    [Parameter(Mandatory = $true)]
    [string] $fromEmailAddress,

    [Parameter(Mandatory = $true)]
    [string] $subject,

    [Parameter(Mandatory = $true)]
    [string] $content,
    
    [Parameter(Mandatory = $true)]
    [string] $vaultName,

    [Parameter(Mandatory = $true)]
    [string] $secretName
)

# Ensure AzContext is not inherited
Disable-AzContextAutosave -Scope Process 

# Authenticate using Managed Identity
$AzureContext = (Connect-AzAccount -Identity).Context
Set-AzContext -SubscriptionId $AzureContext.Subscription.Id | Out-Null

# Retrieve SendGrid API Key from Azure Key Vault
$VaultName = $vaultName
$sendGridApiKeySecure = Get-AzKeyVaultSecret -VaultName $VaultName -Name $secretName

# Convert SecureString to plain text
$sendGridApiKey = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($sendGridApiKeySecure.SecretValue)
)

# Construct HTTP headers
$headers = @{
    "Authorization" = "Bearer $sendGridApiKey"
    "Content-Type"  = "application/json"
}

# Construct email body
$body = @{
    personalizations = @(@{ to = @(@{ email = $destEmailAddress }) })
    from             = @{ email = $fromEmailAddress }
    subject          = $subject
    content          = @(@{ type = "text/plain"; value = $content })
}

# Convert body to JSON
$bodyJson = $body | ConvertTo-Json -Depth 10 -Compress

# Send email using SendGrid API
try {
    Invoke-RestMethod -Uri "https://api.sendgrid.com/v3/mail/send" -Method Post -Headers $headers -Body $bodyJson | Out-Null
    Write-Output "Email sent successfully to $destEmailAddress"
} catch {
    Write-Error "Failed to send email: $_"
}
