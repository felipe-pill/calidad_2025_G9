import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Counter } from 'k6/metrics';  // 👈 import correcto

export const options = {
  stages: [
    { duration: '15s', target: 10 },
    { duration: '45s', target: 10 },
    { duration: '30s', target: 50 },
    { duration: '15s', target: 0  },
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<300'],
  },
};

// métricas personalizadas
const v1Hits = new Counter('v1_hits');
const v2Hits = new Counter('v2_hits');
const ttfb   = new Trend('time_to_first_byte');

// Permite cambiar destino vía variable de entorno: TARGET=ip:puerto o host
const TARGET = __ENV.TARGET || 'demo.local';
// Si usás IP (ej: minikube ip), mantené el Host header para que NGINX Ingress rutee por host:
const USE_HOST_HDR = __ENV.USE_HOST_HDR || 'true';

export default function () {
  const url = TARGET.startsWith('http') ? TARGET : `http://${TARGET}/`;
  const params = USE_HOST_HDR === 'true' ? { headers: { Host: 'demo.local' } } : {};

  const res = http.get(url, params);

  check(res, {
    'status 200': (r) => r.status === 200,
  });

  const body = (res.body || '').toString();
  if (body.includes('v2') || body.includes('Versión 2.0') || body.includes('Version 2.0')) {
    v2Hits.add(1);
  } else if (body.includes('v1') || body.includes('Versión 1.0') || body.includes('Version 1.0')) {
    v1Hits.add(1);
  }

  ttfb.add(res.timings.waiting);
  sleep(0.2);
}
