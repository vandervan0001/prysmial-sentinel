# Parser and destination boundaries

Use this procedure for proxy chains, URL fetchers, imports, uploads or protocol gateways. Write the sequence of parsers, normalizers and authorization decisions before selecting cases.

## Compare the checked value with the consumed value

| Surface | Controlled cases | Observe |
|---|---|---|
| URL fetching | Redirect, multiple DNS answers, IPv6, alternate address form, user information in URL | Actual connected address, redirect policy and data sent |
| HTTP proxy chain | Ambiguous framing, protocol downgrade, duplicate headers | Frontend and backend request boundaries on a dedicated test connection |
| JSON, forms and queries | Duplicate keys, repeated parameters, null, absent value, array versus scalar | Each parser's value and the value authorized by the application |
| Paths and archives | Parent traversal, absolute path, symlink, case collision, duplicate member | Final destination and whether extraction leaves its assigned directory |
| Unicode and identifiers | Normalization, case folding, confusable display name | Stable internal identity and the representation used for permission checks |
| Compressed or nested input | Bounded expansion, depth, member count, truncated payload | Resource use, refusal and cleanup after partial processing |

For SSRF, hostname validation alone does not constrain the eventual connection. Review DNS resolution, destination checks, redirects, proxies and outbound policy together. Use a synthetic resolver or receiver to test restricted address classes. Avoid probing real metadata services. [OWASP SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

For HTTP/1.1, use the framing rules in RFC 9112 sections 6.3 and 11.2. Assess the complete intermediary chain, including conversion from another HTTP version. Record the parsed requests on both ends; an unusual response or delay alone does not prove desynchronization. [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html).

## Filesystem and execution checks

Trace names through validation, open, extraction and later use. A path checked before a symlink or parent directory changes may identify a different object at open time. Prefer descriptor-based operations when the environment requires protection against concurrent changes. Rechecking a string narrows some risks but does not create a filesystem sandbox.

For external tools, inspect executable lookup, inherited environment, working directory, plugin discovery and configuration files. A copied input tree may still influence tool behavior. Read version-matched documentation and test a harmless substitute executable before claiming that target code cannot run.

## Acceptance

Record the original bytes privately, parser versions, interpreted values and observed effect. Include a well-formed case and a rejected malformed case. Confirm cleanup and resource ceilings. Keep desynchronization, resource-exhaustion and extraction tests in an isolated fixture with explicit limits.
