These are for SCPs specific to the account, that do not make sense to be at the OU level.

Primary examples include:

- SCPs with specific values in them. E.g. blocking `ec2:RunInstances` in public subnets.
- Service and region specific allowlist SCPs, if desired.



Arguably, it should be possible to have all SCPs be at the account level. In the case that an SCP needs to be temporarily disabled. 

(Unless we had an additional N! OUs, for every possible combination of SCPs. This does not make sense to do.)


