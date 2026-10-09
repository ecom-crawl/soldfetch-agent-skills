"""Standard-library SoldFetch client. No automatic retries or redirects."""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE_URL = "https://soldfetch.com"
ALLOWED = re.compile(r"/(?:v1/scrape(?:/category)?|v1/item/[0-9]{9,15}|usage|requests|v1/capabilities)")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def get(path, params=None, *, key=None, idempotency_key=None):
    if not ALLOWED.fullmatch(path):
        raise ValueError("Unsupported SoldFetch path")
    key = (key or os.environ.get("SOLDFETCH_API_KEY", "")).strip()
    if not key:
        raise ValueError("Set SOLDFETCH_API_KEY")
    params = {k: str(v).lower() if isinstance(v, bool) else v for k, v in (params or {}).items() if v is not None}
    url = BASE_URL + path + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + key, "Accept": "application/json",
        "Idempotency-Key": idempotency_key or str(uuid.uuid4()),
    })
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=65) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"SoldFetch HTTP {error.code}; request ID: {error.headers.get('x-request-id', 'unavailable')}") from None
    except urllib.error.URLError:
        raise RuntimeError("Could not reach SoldFetch; retry deliberately with the same idempotency key") from None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Call one SoldFetch operation; successful data calls cost one request.")
    parser.add_argument("operation", choices=["search", "category", "item", "usage"])
    parser.add_argument("--keyword")
    parser.add_argument("--category-id")
    parser.add_argument("--item-id")
    parser.add_argument("--site", default="ebay.com", choices=["ebay.com", "ebay.co.uk", "ebay.de", "ebay.fr", "ebay.it", "ebay.es", "ebay.ca", "ebay.com.au"])
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--active", action="store_true")
    parser.add_argument("--idempotency-key")
    args = parser.parse_args()
    if not 1 <= args.count <= 200 or not 1 <= args.page <= 100:
        parser.error("count must be 1–200 and page 1–100")
    params = {"ebaySite": args.site}
    if args.operation == "item":
        if not re.fullmatch(r"[0-9]{9,15}", args.item_id or ""):
            parser.error("item requires --item-id with 9–15 digits")
        path = "/v1/item/" + args.item_id
    elif args.operation == "usage":
        path, params = "/usage", {}
    else:
        params.update(count=args.count, page=args.page, sold=not args.active)
        path = "/v1/scrape"
        if args.operation == "search":
            if not args.keyword or not 1 <= len(args.keyword.strip()) <= 200:
                parser.error("search requires --keyword with 1–200 characters")
            params["keyword"] = args.keyword.strip()
        if args.category_id:
            if not re.fullmatch(r"[0-9]{1,12}", args.category_id) or int(args.category_id)==0:
                parser.error("category ID must be a positive numeric identifier")
            params["categoryId"] = args.category_id
        if args.operation == "category":
            if not args.category_id:
                parser.error("category requires --category-id")
            path += "/category"
    print(json.dumps(get(path, params, idempotency_key=args.idempotency_key), indent=2))

if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as error:
        raise SystemExit(str(error)) from None
