// Static fixtures, never execute this file.
// ruleid: cyber-js-tls-disabled
const unsafeOptions = { rejectUnauthorized: false };
// ok: cyber-js-tls-disabled
const safeOptions = { rejectUnauthorized: true };

function bad(req) {
  const code = req.query.code;
  // ruleid: cyber-js-eval-request
  eval(code);
}
function good(req) {
  // ok: cyber-js-eval-request
  eval('1 + 1');
}
