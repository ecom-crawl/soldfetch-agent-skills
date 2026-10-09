import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
const manifest=JSON.parse(readFileSync('manifest.json','utf8'));
for(const skill of manifest.skills){const text=readFileSync(skill.path+'/SKILL.md','utf8');assert.ok(text.startsWith('---\nname: '+skill.name+'\n'));for(const ref of text.matchAll(/\]\((references\/[^)]+)\)/g))assert.ok(existsSync(skill.path+'/'+ref[1]));}
assert.equal(spawnSync('python3',['-m','unittest','discover','-s','tests','-v'],{stdio:'inherit'}).status,0);
