# BGP Neighbor Troubleshooting

BGP troubleshooting should start by identifying the current neighbor state and determining whether the session is stable.

## Initial checks

Check:

- neighbor IP address
- BGP state
- uptime
- last reset reason
- prefixes received
- prefixes advertised

A neighbor in Established state indicates that the BGP session is currently established, but does not by itself prove that the session has always been stable.

## Session instability

For repeated flaps, review:

- interface errors
- packet loss
- TCP connectivity
- route filtering
- authentication
- timers
- configuration changes
- device CPU utilization

Correlate BGP reset times with interface and system events.

## TCP investigation

BGP uses TCP.

Check whether the router can maintain stable TCP connectivity to the configured neighbor address.

## Configuration investigation

Review:

- remote AS
- local AS
- update-source
- authentication
- route policy
- prefix filtering
- BGP timers

Compare the configuration with the intended network design.

## Operational conclusion

Do not conclude that a BGP session is unstable solely because an individual snapshot shows Established state.

Historical information and correlated telemetry are required to determine whether repeated flapping occurred.