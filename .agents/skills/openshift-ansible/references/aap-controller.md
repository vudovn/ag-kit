# AAP Controller — OpenShift Ansible

## Job Template Diagnosis

1. Check Job Template configuration: variables, inventory, credentials.
2. Check Execution Environment image: available, correct Python deps.
3. Check Project source: Git URL, branch, credential, sync status.
4. Check Credential type matches target (machine, cloud, vault, SCM).
5. Check Job launch logs for pre-flight errors.

## Credential Issues

- Machine credential: SSH key or password must be valid.
- Vault credential: vault password must decrypt vault files.
- SCM credential: must have access to the Git repository.
- Cloud credential: API key/token must be valid and not expired.
- Never display credential values — check only by attempting access.

## Inventory Issues

- Static: verify host entries and group membership.
- Dynamic: verify script/plugin runs, check cloud API access.
- Smart: verify filter expression matches expected hosts.
- Verify `ansible_host`, `ansible_user`, `ansible_connection` vars.

## Evidence Commands (via AAP API or UI)

- Check Job Template details → Variables, Credentials, Inventory.
- Check Job output → full log, not summary.
- Check Project sync status.
- Check Execution Environment status.
