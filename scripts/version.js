// Writes web/version.js with the git commit being built (used by the page title).
const { execSync } = require('child_process');
const fs = require('fs');
let sha = process.env.WORKERS_CI_COMMIT_SHA || '';
let msg = '';
try { if (!sha) sha = execSync('git rev-parse HEAD').toString().trim(); } catch (e) {}
try { msg = execSync('git log -1 --format=%s').toString().trim(); } catch (e) {}
const info = { commit: (sha || 'unknown').slice(0, 7), message: msg, built: new Date().toISOString() };
fs.writeFileSync(__dirname + '/../web/version.js', 'window.APP_VERSION = ' + JSON.stringify(info) + ';\n');
console.log('version.js:', info.commit, msg);
