#cloud-config
users:
  - name: appuser
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: sudo
    ssh-authorized-keys:
      - "${public_key_appuser}"