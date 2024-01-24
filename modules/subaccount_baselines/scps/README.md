These are for SCPs specific to the account, that do not make sense to be at the OU level.

Primary examples include:

- SCPs with specific values in them. E.g. blocking `ec2:RunInstances` in public subnets.
- Service and region specific allowlist SCPs, if desired.

You could argue it is desirable to be able to disable SCPs be at the account level. In the case that a particular SCP needs to be temporarily disabled.

**Note this assumes GuardDuty and CloudTrail are enabled at the organization-level**
