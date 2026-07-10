An Apache-style access log is available at `/app/access.log`. Analyze the traffic and write a JSON report to `/app/report.json`.

Your report must be a JSON object with these fields:

- `total_requests` (int): number of non-empty lines in the access log
- `unique_ips` (int): number of distinct client IP addresses (the first whitespace-delimited token on each non-empty line)
- `top_path` (string): the most frequently requested path, extracted from lines matching the pattern `"(?:GET|POST|PUT|DELETE|HEAD|PATCH) <path> `

## Success criteria

1. `/app/report.json` exists and contains valid JSON.
2. `total_requests` exactly matches the count of non-empty lines in `/app/access.log`.
3. `unique_ips` exactly matches the number of distinct first-token IP addresses across non-empty log lines.
4. `top_path` exactly matches the most common request path found via the HTTP method/path pattern above.
