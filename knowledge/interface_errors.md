# Interface Error Troubleshooting

Interface errors can indicate physical, link-layer, congestion, or traffic-related problems.

## Initial checks

Check:

- interface operational state
- input errors
- output errors
- CRC errors
- packet drops
- interface resets
- traffic rate

Determine whether errors are increasing over time.

## Physical layer checks

For physical interfaces, inspect:

- cable condition
- transceiver condition
- speed
- duplex
- negotiated settings
- interface counters

Compare both ends of the connection where possible.

## Neighbor investigation

Inspect the connected device for corresponding errors.

A problem visible on one side should be correlated with counters and state on the peer.

## Traffic investigation

Review traffic utilization and packet rates.

High utilization combined with drops can indicate congestion.

## Corrective action

Do not immediately change configuration.

First collect counters, determine the error type, establish whether counters are increasing, and correlate the issue with the peer device.

## Escalation

Escalate when errors continue increasing after physical and configuration checks, or when the issue is associated with hardware alarms.