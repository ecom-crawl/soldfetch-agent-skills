# Operations

| Operation | REST | MCP | Required input |
| --- | --- | --- | --- |
| Search | GET /v1/scrape | search_ebay_sold | keyword |
| Category | GET /v1/scrape/category | search_ebay_category | categoryId |
| Item | GET /v1/item/{itemId} | get_ebay_item | itemId (9–15 digits) |

REST search defaults to 60 results; MCP and this helper default to 20. Search count is 1–200, page 1–100. Use ebaySite hostnames, not country codes. Set sold=false for active listings. Search accepts itemCondition any/new/used, minPrice, maxPrice, buyingFormat, sortOrder, and exactMatch as documented in OpenAPI. Item lookup accepts only itemId and ebaySite.

Use one credential header: Authorization: Bearer or API-KEY. REST Idempotency-Key replays identical successful data operations for 24 hours without another charge; different inputs return 409. Use fresh keys for new observations and pages. MCP calls are not automatically deduplicated by the REST retry mechanism.

60 data requests/minute and five concurrent requests are shared by workspace. Honor Retry-After on 429; use bounded retries for transient failures. Do not retry bad credentials, invalid inputs, unsupported capabilities, or exhausted quota indefinitely. GET /usage and GET /requests are free account calls with a separate rate limit.

Date filters, accepted-offer enrichment, email exports, sellerType, conditionId, aspectFilter, non-default itemLocation, and distance sorting are unavailable. Category-only sold searches can return an uncharged 503.
