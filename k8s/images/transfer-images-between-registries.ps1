#
# This script transfers Docker images from a source registry to a destination Azure Container Registry (ACR).
# It logs into both registries, pulls images from the source registry, tags them for the destination registry,
# and optionally pushes them to the destination registry.
#
# Parameters:
# - sourceRegistry: The source Docker registry (default: "source-registry.io").
# - destinationRegistry: The destination Azure Container Registry (default: "destination-registry.azurecr.io").
#
# Usage:
# 1. Ensure you have the Azure CLI and Docker installed and configured on your machine.
# 2. Run the script, providing the source and destination registries as needed.
# 3. The script will prompt you to confirm whether to push the images to the destination registry.
#
# Example:
# .\transfer-images-between-registries.ps1 -sourceRegistry "my-source-registry.io" -destinationRegistry "my-destination-registry.azurecr.io"
#
# List of images to transfer:
# - bash:5.2.26
# - fluent-bit:1.9.6
# - fuse-deployment:0.11
# - fuse-job:0.11
# - nvidia/k8s-device-plugin:v0.12.2
# - oauth2-proxy:v7.6.1-nc
# - postgres:10.23-alpine3.16
# - traefik:v2.1
#

param (
    [string]$sourceRegistry = "source-registry.io",
    [string]$destinationRegistry = "destination-registry.azurecr.io"
)

# List of images
$images = @(
    "bash:5.2.26",
    "fluent-bit:1.9.6",
    "fuse-deployment:0.11",
    "fuse-job:0.11",
    "nvidia/k8s-device-plugin:v0.12.2",
    "oauth2-proxy:v7.6.1-nc",
    "postgres:10.23-alpine3.16",
    "traefik:v2.1"
)

function Write-Log {
    param (
        [string]$message,
        [string]$type = "INFO"
    )
    Write-Host "[$type] $message"
}

function Connect-Azure {
    Write-Log "Logging into Azure..."
    az login
}

function Connect-Registry {
    param (
        [string]$registry
    )
    Write-Log "Logging into the registry: $registry..."
    docker login $registry
}

function Invoke-ImageTransfer {
    param (
        [array]$images,
        [string]$sourceRegistry,
        [string]$destinationRegistry,
        [bool]$pushImages
    )

    foreach ($image in $images) {
        $sourceImage = "$sourceRegistry/$image"
        $destinationImage = "$destinationRegistry/$image"

        Write-Log "Pulling $sourceImage..."
        docker pull $sourceImage

        Write-Log "Tagging $sourceImage as $destinationImage..."
        docker tag $sourceImage $destinationImage

        Write-Log "Deleting the source image $sourceImage..."
        docker rmi $sourceImage

        if ($pushImages) {
            Write-Log "Pushing $destinationImage to $destinationRegistry..."
            docker push $destinationImage
        }

        Write-Log "Image $image processed successfully."
    }
}

# Main script execution
Connect-Azure
Login-Registry -registry $sourceRegistry

$pushImages = Read-Host "Do you want to push the images to the destination registry ($destinationRegistry)? (yes/no)"
$pushImages = $pushImages -eq "yes"

if ($pushImages) {
    Login-Registry -registry $destinationRegistry
}

Invoke-ImageTransfer -images $images -sourceRegistry $sourceRegistry -destinationRegistry $destinationRegistry -pushImages $pushImages

Write-Log "All images have been processed."
