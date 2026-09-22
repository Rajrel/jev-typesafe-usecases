# Incident runbook

## Checkout 500s

If shoppers see HTTP 500 on checkout after a deploy, roll back the payment service and page the infra on-call. Compare the alert with open incident INC-14 before opening a second ticket.

## Label printer

A jammed label printer does not stop orders. Clear the jam and reprint. Do not page the whole company.

## Disk full

A full disk on a staging runner is an infra problem. Production checkout is unrelated unless the same host is named.
