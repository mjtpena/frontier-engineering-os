# L2 Platform — Power Platform

- Solutions only (managed in test/prod); environment strategy documented; ALM via Power Platform pipelines or GitHub Actions for Power Platform.
- Connection references and environment variables — never hard-coded connections.
- DLP policies respected; any new connector requires a DLP review recorded in evidence.
- Dataverse security roles least-privilege; service principals (application users) for automation.
