import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Hydra capacity profile. This script generates ordinary GET traffic only.
// High-scale runs require distributed generators and explicit operator approval.
const target = __ENV.TARGET_URL || '';
const allowHost = (__ENV.ALLOW_HOST || '').toLowerCase();
const confirmHost = (__ENV.CONFIRM_HOST || '').toLowerCase();
const maxVus = Number(__ENV.HYDRA_MAX_VUS || '1000');
const thinkTime = Number(__ENV.HYDRA_THINK_TIME || '5');

if (!target || !allowHost || !confirmHost) {
  throw new Error('Set TARGET_URL, ALLOW_HOST and CONFIRM_HOST.');
}
let parsed;
try { parsed = new URL(target); } catch (_) { throw new Error('TARGET_URL must be a valid absolute URL.'); }
if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('Only HTTP(S) targets are supported.');
if (parsed.hostname.toLowerCase() !== allowHost || allowHost !== confirmHost) {
  throw new Error('Target hostname must exactly match ALLOW_HOST and CONFIRM_HOST.');
}
if (!Number.isInteger(maxVus) || maxVus < 1 || maxVus > 100000) {
  throw new Error('HYDRA_MAX_VUS must be an integer from 1 to 100000.');
}
if (!Number.isFinite(thinkTime) || thinkTime < 1 || thinkTime > 60) {
  throw new Error('HYDRA_THINK_TIME must be between 1 and 60 seconds.');
}
if (__ENV.HYDRA_AUTHORIZED !== 'YES') {
  throw new Error('Set HYDRA_AUTHORIZED=YES only when you own the target or have written authorization.');
}
if (maxVus > 5000 && (__ENV.HYDRA_HIGH_SCALE_APPROVED !== 'YES' || __ENV.HYDRA_PROVIDER_APPROVAL !== 'YES')) {
  throw new Error('Above 5,000 VUs requires HYDRA_HIGH_SCALE_APPROVED=YES and HYDRA_PROVIDER_APPROVAL=YES after provider approval and a scheduled test window.');
}

const rate429 = new Rate('http_429_rate');
const rate5xx = new Rate('http_5xx_rate');

const ladder = [100, 500, 1000, 2500, 5000, 10000, 25000, 50000, 75000, 100000]
  .filter((v) => v < maxVus);
ladder.push(maxVus);

export const options = {
  discardResponseBodies: true,
  maxRedirects: 0,
  scenarios: {
    capacity_ramp: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        ...ladder.map((targetVUs) => ({ duration: '2m', target: targetVUs })),
        { duration: '3m', target: maxVus },
        { duration: '2m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
  },
  thresholds: {
    http_req_failed: [{ threshold: 'rate<0.01', abortOnFail: true, delayAbortEval: '30s' }],
    http_req_duration: [{ threshold: 'p(95)<2000', abortOnFail: true, delayAbortEval: '60s' }],
    http_429_rate: [{ threshold: 'rate<0.01', abortOnFail: true, delayAbortEval: '30s' }],
    http_5xx_rate: [{ threshold: 'rate<0.01', abortOnFail: true, delayAbortEval: '30s' }],
  },
};

export default function () {
  const response = http.get(target, {
    headers: { 'User-Agent': 'Hydra-Authorized-Capacity-Test/1.0' },
    redirects: 0,
    tags: { test_type: 'capacity', target_host: parsed.hostname },
  });
  rate429.add(response.status === 429);
  rate5xx.add(response.status >= 500);
  check(response, {
    'response is not a server error': (r) => r.status < 500,
    'response is not rate limited': (r) => r.status !== 429,
  });
  sleep(thinkTime);
}
