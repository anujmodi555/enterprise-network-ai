# High CPU Utilization Troubleshooting

High CPU utilization on a network router should be investigated using current telemetry and recent operational changes.

## Initial checks

Check the current CPU utilization and determine whether the condition is persistent or temporary.

Review CPU history when available rather than relying only on a single instantaneous reading.

Identify processes consuming CPU resources.

## Interface investigation

Inspect interface statistics for:

- input errors
- output errors
- packet drops
- abnormal traffic rates
- flapping interfaces

A sudden traffic increase or interface-related problem can contribute to increased device processing.

## Routing investigation

Review routing protocol state and recent changes.

For BGP, check whether neighbors are repeatedly transitioning between states.

For OSPF, check for adjacency instability and excessive SPF activity.

## Configuration investigation

Review recent configuration changes.

Check for:

- access-list changes
- routing policy changes
- QoS changes
- telemetry configuration changes
- debug commands

Debugging features can increase CPU utilization significantly.

## Escalation

If CPU remains high after identifying the responsible process and no configuration explanation is available, collect detailed telemetry and escalate for deeper platform investigation.

Do not assume high CPU alone establishes the root cause.