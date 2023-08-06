# SDKMS Git Signing Tool

This is a utility for signing/verifying git commits with keys stored in Fortanix Self-Defending Key Management System. It includes commands for generating a PGP compatible key in SDKMS.

# Setup
1. In SDKMS create an App and an EC key (only NISTP256, NISTP384 and NISTP512 are supported). Take notes of:
    - App API Key
    - Key UUID

2. In you git repository, the following configuration is needed:

```
git config --local gpg.program </path/to/sdkms-git-sign-tool>
git config --local user.signingkey <Key UUID>
git config --local sdkms.endpoint <SDKMS endpoint>
git config --local sdkms.apikey <SDKMS API Key>
```

