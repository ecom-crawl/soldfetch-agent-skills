import assert from 'node:assert/strict';
const contract=await fetch('https://soldfetch.com/api/v1/openapi.json',{signal:AbortSignal.timeout(20000)});
assert.equal(contract.status,200);const spec=await contract.json();
for(const path of ['/v1/scrape','/v1/item/{itemId}','/usage','/requests'])assert.ok(spec.paths[path]?.get);
const response=await fetch('https://soldfetch.com/v1/scrape?keyword=sony&count=1',{signal:AbortSignal.timeout(65000),redirect:'error'});
assert.equal(response.status,401);assert.equal(response.headers.get('x-soldfetch-usage-units'),'0');
console.log('Public contract and unauthenticated REST rejection verified; zero charged requests.');
