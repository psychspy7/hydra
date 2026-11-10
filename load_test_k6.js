import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 100 }, // Ramp up to 100 users
    { duration: '1m', target: 500 },  // Spike to 500 users
    { duration: '30s', target: 0 },   // Scale down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
    http_req_failed: ['rate<0.01'],   // Error rate must be less than 1%
  },
};

export default function () {
  const res = http.get('https://thekittycorp.com', {
    headers: { 'User-Agent': 'KittyCorp-k6/2.0' },
  });
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(0.1);
}
