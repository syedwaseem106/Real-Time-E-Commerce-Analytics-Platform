<div align="center">

# ⚡ Real-Time E-Commerce Analytics Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Kafka-7.5.0-231F20?style=for-the-badge&logo=apachekafka&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Spark-3.5.0-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Airflow-2.7-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/dbt_Core-1.7-FF694B?style=for-the-badge&logo=dbt&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/MinIO-S3_Compatible-C72E49?style=for-the-badge&logo=minio&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</p>

## 📊 Dashboard Preview
Real-Time E-Commerce Analytics Live pipeline
Syed Waseem · 2026
Kafka · PySpark
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font-sans)}
.header{padding:1.5rem 1.5rem 1rem;border-bottom:0.5px solid var(--color-border-tertiary)}
.badge{display:inline-block;font-size:11px;padding:3px 8px;border-radius:var(--border-radius-md);background:var(--color-background-info);color:var(--color-text-info);font-weight:500;margin-left:8px}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;padding:1rem 1.5rem}
.metric{background:var(--color-background-secondary);border-radius:var(--border-radius-md);padding:0.875rem 1rem}
.metric-label{font-size:11px;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px}
.metric-value{font-size:22px;font-weight:500;color:var(--color-text-primary);line-height:1}
.metric-sub{font-size:11px;color:var(--color-text-tertiary);margin-top:4px}
.metric-up{color:var(--color-text-success)}
.section{padding:0 1.5rem 1rem}
.section-title{font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px;padding-top:1rem}
.two-col{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:12px;padding:0 1.5rem 1rem}
.card{background:var(--color-background-primary);border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);padding:1rem 1.25rem}
.card-title{font-size:12px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px}
.funnel-row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.funnel-label{font-size:12px;color:var(--color-text-secondary);width:90px;flex-shrink:0}
.funnel-bar-wrap{flex:1;height:20px;background:var(--color-background-secondary);border-radius:4px;overflow:hidden}
.funnel-bar{height:100%;border-radius:4px;transition:width 1s ease}
.funnel-count{font-size:12px;color:var(--color-text-secondary);width:56px;text-align:right;flex-shrink:0}
.funnel-pct{font-size:11px;color:var(--color-text-tertiary);width:36px;text-align:right;flex-shrink:0}
.seg-row{display:flex;align-items:center;justify-content:space-between;padding:7px 0;border-bottom:0.5px solid var(--color-border-tertiary);font-size:13px}
.seg-row:last-child{border-bottom:none}
.seg-pill{font-size:11px;padding:2px 7px;border-radius:999px;font-weight:500}
.pill-vip{background:#EEEDFE;color:#3C3489}
.pill-reg{background:#E1F5EE;color:#085041}
.pill-new{background:#FAEEDA;color:#633806}
.arch-wrap{padding:0 1.5rem 1.5rem}
.tag-row{display:flex;flex-wrap:wrap;gap:6px;padding:0 1.5rem 1.5rem}
.tag{font-size:11px;padding:3px 8px;border-radius:var(--border-radius-md);border:0.5px solid var(--color-border-secondary);color:var(--color-text-secondary)}
.nav{display:flex;gap:2px;padding:1rem 1.5rem 0}
.nav-btn{font-size:12px;padding:5px 12px;border-radius:var(--border-radius-md);border:0.5px solid transparent;color:var(--color-text-secondary);cursor:pointer;background:transparent}
.nav-btn.active{background:var(--color-background-secondary);border-color:var(--color-border-secondary);color:var(--color-text-primary);font-weight:500}
canvas{width:100%!important}
</style>

<h2 class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)">Real-Time E-Commerce Analytics Platform — project dashboard showing pipeline metrics, architecture diagram, funnel analysis, and segment breakdown</h2>

<div class="header">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <div>
      <span style="font-size:16px;font-weight:500;color:var(--color-text-primary)">Real-Time E-Commerce Analytics</span>
      <span class="badge">Live pipeline</span>
    </div>
    <span style="font-size:12px;color:var(--color-text-tertiary)">Syed Waseem · 2026</span>
  </div>
  <div style="margin-top:6px;font-size:12px;color:var(--color-text-secondary)">Kafka · PySpark · Airflow · dbt · PostgreSQL · MinIO · Docker</div>
</div>

<div class="nav">
  <button class="nav-btn active" onclick="showTab('overview')">Overview</button>
  <button class="nav-btn" onclick="showTab('architecture')">Architecture</button>
  <button class="nav-btn" onclick="showTab('funnel')">Funnel & Segments</button>
</div>

<!-- OVERVIEW TAB -->
<div id="tab-overview">
  <div class="metrics">
    <div class="metric">
      <div class="metric-label">Simulated users</div>
      <div class="metric-value">1,000</div>
      <div class="metric-sub">VIP · Regular · New</div>
    </div>
    <div class="metric">
      <div class="metric-label">Events processed</div>
      <div class="metric-value">239K+</div>
      <div class="metric-sub metric-up">↑ streaming</div>
    </div>
    <div class="metric">
      <div class="metric-label">BI reports</div>
      <div class="metric-value">7</div>
      <div class="metric-sub">Power BI · Tableau</div>
    </div>
    <div class="metric">
      <div class="metric-label">Docker services</div>
      <div class="metric-value">6</div>
      <div class="metric-sub">Single command</div>
    </div>
  </div>

  <div class="two-col">
    <div class="card">
      <div class="card-title">Hourly event volume (simulated)</div>
      <canvas id="chart-events" height="130"></canvas>
    </div>
    <div class="card">
      <div class="card-title">Pipeline layers</div>
      <div style="font-size:12px;color:var(--color-text-secondary)">
        <div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:0.5px solid var(--color-border-tertiary)"><span style="width:8px;height:8px;border-radius:2px;background:#7F77DD;flex-shrink:0"></span>Event Generation → Kafka</div>
        <div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:0.5px solid var(--color-border-tertiary)"><span style="width:8px;height:8px;border-radius:2px;background:#1D9E75;flex-shrink:0"></span>PySpark Streaming → MinIO Lake</div>
        <div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:0.5px solid var(--color-border-tertiary)"><span style="width:8px;height:8px;border-radius:2px;background:#378ADD;flex-shrink:0"></span>Spark Batch → PostgreSQL</div>
        <div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:0.5px solid var(--color-border-tertiary)"><span style="width:8px;height:8px;border-radius:2px;background:#D85A30;flex-shrink:0"></span>dbt transforms → Star Schema</div>
        <div style="display:flex;align-items:center;gap:8px;padding:6px 0"><span style="width:8px;height:8px;border-radius:2px;background:#BA7517;flex-shrink:0"></span>Airflow DAG Orchestration</div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">Tech stack</div>
    <div class="tag-row" style="padding:0 0 1rem">
      <span class="tag">Python 3.10</span><span class="tag">Apache Kafka 7.5</span><span class="tag">PySpark 3.5</span><span class="tag">Airflow 2.7</span><span class="tag">dbt Core 1.7</span><span class="tag">PostgreSQL 15</span><span class="tag">MinIO S3</span><span class="tag">Docker Compose</span><span class="tag">Parquet</span><span class="tag">SQLAlchemy</span>
    </div>
  </div>
</div>

<!-- ARCHITECTURE TAB -->
<div id="tab-architecture" style="display:none;padding:1rem 1.5rem 1.5rem">
  <svg width="100%" viewBox="0 0 640 540" role="img">
    <title>Pipeline architecture diagram</title>
    <desc>End-to-end data pipeline from event generation through Kafka, Spark streaming, MinIO, batch processing, dbt transforms, to BI reporting, orchestrated by Airflow.</desc>
    <defs>
      <marker id="arr2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
        <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </marker>
    </defs>

    <!-- Event Generation -->
    <g>
      <rect x="20" y="20" width="200" height="56" rx="8" fill="#EEEDFE" stroke="#7F77DD" stroke-width="0.5"/>
      <text font-family="var(--font-sans)" font-size="13" font-weight="500" fill="#3C3489" x="120" y="43" text-anchor="middle" dominant-baseline="central">Event Generator</text>
      <text font-family="var(--font-sans)" font-size="11" fill="#534AB7" x="120" y="62" text-anchor="middle" dominant-baseline="central">Faker · 1,000 users · funnel weights</text>
    </g>

    <!-- Kafka -->
    <g>
      <rect x="260" y="20" width="180" height="56" rx="8" fill="#E1F5EE" stroke="#1D9E75" stroke-width="0.5"/>
      <text font-family="var(--font-sans)" font-size="13" font-weight="500" fill="#085041" x="350" y="40" text-anchor="middle" dominant-baseline="central">Apache Kafka</text>
      <text font-family="var(--font-sans)" font-size="11" fill="#0F6E56" x="350" y="58" text-anchor="middle" dominant-baseline="central">3 partitions + DLQ</text>
    </g>
    <line x1="220" y1="48" x2="258" y2="48" stroke="#888780" stroke-width="0.8" marker-end="url(#arr2)" fill="none"/>

    <!-- PySpark Streaming -->
    <g>
      <rect x="20" y="130" width="200" height="56" rx="8" fill="#E6F1FB" stroke="#378ADD" stroke-width="0.5"/>
      <text font-family="var(--font-sans)" font-size="13" font-weight="500" fill="#0C447C" x="120" y="150" text-anchor="middle" dominant-baseline="central">PySpark Streaming</text>
      <text font-family="var(--font-sans)" font-size="11" fill="#185FA5" x="120" y="168" text-anchor="middle" dominant-baseline="central">Schema validation · watermarking</text>
    </g>
    <line x1="350" y1="76" x2="350" y2="104" stroke="#888780" stroke-width="0.8" fill="none"/>
    <line x1="350" y1="104" x2="122" y2="104" stroke="#888780" stroke-width="0.8" fill="none"/>
    <line x1="122" y1="104" x2="122" y2="128" stroke="#888780" stroke-width="0.8" marker-end="url(#arr2)" fill="none"/>

    <!-- MinIO -->
    <g>
      <rect x="260" y="130" width="180" height="56" rx="8" fill="#FAEEDA" stroke="#BA7517" stroke-width="0.5"/>
      <text font-family="var(--font-sans)" font-size="13" font-weight="500" fill="#633806" x="350" y="150" text-anchor="middle" dominant-baseline="central">MinIO Data Lake</text>
      <text font-family="var(--font-sans)" font-size="11" fill="#854F0B" x="350" y="168" text-anchor="middle" dominant-baseline="central">Parquet · year/month/day/hour</text>
    </g>
    <line x1="220" y1="158" x2="258" y2="158" stroke="#888780" stroke-width="0.8" marker-end="url(#arr2)" fill="none"/>

    <!-- Spark Batch -->
    <g>
      <rect x="20" y="240" width="200" height="56" rx="8" fill="#E6F1FB" stroke="#378ADD" stroke-width="0.5"/>
      <text font-family="var(--font-sans)" font-size="13" font-weight="500" fill="#0C447C" x="120" y="260" text-anchor="middle" dominant-baseline="central">Spark Batch</text>
      <text font-family="var(--font-sans)" font-size="11" fill="#185FA5" x="120" y="278" text-anchor="middle" dominant-baseline="central">Dedup · JDBC load</text>
    </g>
    <line x1="350" y1="186" x2="350" y2="214" stroke="#888780" stroke-width="0.8" fill="none"/>
    <line x1="350" y1="214" x2="122" y2="214" stroke="#888780" stroke-width="0.8" fill="none"/>
    <line x1="122" y1="214" x2="122" y2="238" stroke="#888780" stroke-width="0.8" marker-end="url(#arr2)" fill="none"/>

    <!-- PostgreSQL -->
    <g>
      <rect x="260" y="240" width="180" height="56" rx="8" fill="#EAF3DE" stroke="#3B6D11" stroke-width="0.5"/>
      <text font-family="var(--font-sans)" font-size="13" font-weight="500" fill="#173404" x="350" y="260" text-anchor="middle" dominant-baseline="central">PostgreSQL</text>
      <text font-family="var(--font-sans)" font-size="11" fill="#27500A" x="350" y="278" text-anchor="middle" dominant-baseline="central">staging.stg_events</text>
    </g>
    <line x1="220" y1="268" x2="258" y2="268" stroke="#888780" stroke-width="0.8" marker-end="url(#arr2)" fill="none"/>

    <!-- dbt -->
    <g>
      <rect x="20" y="350" width="200" height="56" rx="8" fill="#FAECE7" stroke="#993C1D" stroke-width="0.5"/>
      <text font-family="var(--font-sans)" font-size="13" font-weight="500" fill="#4A1B0C" x="120" y="370" text-anchor="middle" dominant-baseline="central">dbt Core 1.7</text>
      <text font-family="var(--font-sans)" font-size="11" fill="#712B13" x="120" y="388" text-anchor="middle" dominant-baseline="central">Staging · dim_* · fct_events</text>
    </g>
    <line x1="350" y1="296" x2="350" y2="324" stroke="#888780" stroke-width="0.8" fill="none"/>
    <line x1="350" y1="324" x2="122" y2="324" stroke="#888780" stroke-width="0.8" fill="none"/>
    <line x1="122" y1="324" x2="122" y2="348" stroke="#888780" stroke-width="0.8" marker-end="url(#arr2)" fill="none"/>

    <!-- BI Reports -->
    <g>
      <rect x="260" y="350" width="180" height="56" rx="8" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5"/>
      <text font-family="var(--font-sans)" font-size="13" font-weight="500" fill="#2C2C2A" x="350" y="370" text-anchor="middle" dominant-baseline="central">BI Reports</text>
      <text font-family="var(--font-sans)" font-size="11" fill="#444441" x="350" y="388" text-anchor="middle" dominant-baseline="central">7 CSV exports · Power BI · Tableau</text>
    </g>
    <line x1="220" y1="378" x2="258" y2="378" stroke="#888780" stroke-width="0.8" marker-end="url(#arr2)" fill="none"/>

    <!-- Airflow orchestration bracket -->
    <rect x="470" y="20" width="150" height="390" rx="8" fill="none" stroke="#BA7517" stroke-width="0.5" stroke-dasharray="4 3"/>
    <text font-family="var(--font-sans)" font-size="12" font-weight="500" fill="#854F0B" x="545" y="44" text-anchor="middle">Airflow DAG</text>
    <text font-family="var(--font-sans)" font-size="11" fill="#BA7517" x="545" y="62" text-anchor="middle">Hourly · 6 stages</text>
    <text font-family="var(--font-sans)" font-size="11" fill="#BA7517" x="545" y="78" text-anchor="middle">retry handling</text>

    <!-- Airflow stage dots -->
    <circle cx="510" cy="130" r="4" fill="#EF9F27"/>
    <circle cx="510" cy="190" r="4" fill="#EF9F27"/>
    <circle cx="510" cy="250" r="4" fill="#EF9F27"/>
    <circle cx="510" cy="310" r="4" fill="#EF9F27"/>
    <circle cx="510" cy="370" r="4" fill="#EF9F27"/>
    <line x1="510" y1="134" x2="510" y2="186" stroke="#BA7517" stroke-width="0.5" stroke-dasharray="2 2"/>
    <line x1="510" y1="194" x2="510" y2="246" stroke="#BA7517" stroke-width="0.5" stroke-dasharray="2 2"/>
    <line x1="510" y1="254" x2="510" y2="306" stroke="#BA7517" stroke-width="0.5" stroke-dasharray="2 2"/>
    <line x1="510" y1="314" x2="510" y2="366" stroke="#BA7517" stroke-width="0.5" stroke-dasharray="2 2"/>

    <!-- Docker label -->
    <rect x="20" y="460" width="420" height="32" rx="6" fill="none" stroke="#888780" stroke-width="0.5" stroke-dasharray="3 3"/>
    <text font-family="var(--font-sans)" font-size="11" fill="#5F5E5A" x="230" y="476" text-anchor="middle" dominant-baseline="central">Docker Compose — 6 services: Zookeeper · Kafka · Spark · PostgreSQL · MinIO · Airflow</text>
  </svg>
</div>

<!-- FUNNEL & SEGMENTS TAB -->
<div id="tab-funnel" style="display:none">
  <div class="two-col">
    <div class="card" style="margin:1rem 0 0 1.5rem">
      <div class="card-title">Conversion funnel</div>
      <div class="funnel-row">
        <span class="funnel-label" style="font-size:12px">Page view</span>
        <div class="funnel-bar-wrap"><div class="funnel-bar" style="width:100%;background:#7F77DD"></div></div>
        <span class="funnel-count">100,000</span>
        <span class="funnel-pct">100%</span>
      </div>
      <div class="funnel-row">
        <span class="funnel-label" style="font-size:12px">Add to cart</span>
        <div class="funnel-bar-wrap"><div class="funnel-bar" style="width:62%;background:#534AB7"></div></div>
        <span class="funnel-count">62,000</span>
        <span class="funnel-pct">62%</span>
      </div>
      <div class="funnel-row">
        <span class="funnel-label" style="font-size:12px">Checkout</span>
        <div class="funnel-bar-wrap"><div class="funnel-bar" style="width:31%;background:#3C3489"></div></div>
        <span class="funnel-count">31,000</span>
        <span class="funnel-pct">31%</span>
      </div>
      <div class="funnel-row">
        <span class="funnel-label" style="font-size:12px">Purchase</span>
        <div class="funnel-bar-wrap"><div class="funnel-bar" style="width:14%;background:#26215C"></div></div>
        <span class="funnel-count">14,000</span>
        <span class="funnel-pct">14%</span>
      </div>
      <div style="margin-top:12px">
        <canvas id="chart-funnel" height="110"></canvas>
      </div>
    </div>
    <div style="margin:1rem 1.5rem 0 0">
      <div class="card" style="margin-bottom:10px">
        <div class="card-title">User segments</div>
        <div class="seg-row"><span><span class="seg-pill pill-vip">VIP</span></span><span style="font-size:13px;color:var(--color-text-secondary)">High spend · loyal</span><span style="font-size:13px;font-weight:500">~200</span></div>
        <div class="seg-row"><span><span class="seg-pill pill-reg">Regular</span></span><span style="font-size:13px;color:var(--color-text-secondary)">Moderate activity</span><span style="font-size:13px;font-weight:500">~550</span></div>
        <div class="seg-row"><span><span class="seg-pill pill-new">New</span></span><span style="font-size:13px;color:var(--color-text-secondary)">First-time buyers</span><span style="font-size:13px;font-weight:500">~250</span></div>
      </div>
      <div class="card">
        <div class="card-title">dbt models</div>
        <div style="font-size:12px;color:var(--color-text-secondary)">
          <div style="padding:4px 0;border-bottom:0.5px solid var(--color-border-tertiary)">stg_events · stg_users · stg_products</div>
          <div style="padding:4px 0;border-bottom:0.5px solid var(--color-border-tertiary)">dim_users · dim_products · dim_date</div>
          <div style="padding:4px 0;border-bottom:0.5px solid var(--color-border-tertiary)">fct_events (SCD) · agg_user_summary</div>
          <div style="padding:4px 0">Tests: unique · not_null · ref integrity</div>
        </div>
      </div>
    </div>
  </div>
  <div style="height:1.5rem"></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const dark = matchMedia('(prefers-color-scheme: dark)').matches;
const textColor = dark ? 'rgba(194,192,182,0.7)' : 'rgba(61,61,58,0.6)';
const gridColor = dark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';

function showTab(name) {
  ['overview','architecture','funnel'].forEach(t => {
    document.getElementById('tab-'+t).style.display = t===name ? '' : 'none';
  });
  document.querySelectorAll('.nav-btn').forEach((b,i) => {
    b.classList.toggle('active', ['overview','architecture','funnel'][i]===name);
  });
  if(name==='funnel' && !window._funnelChart) initFunnelChart();
}

const hours = Array.from({length:24},(_,i)=>i+':00');
const evts = [420,180,90,60,110,310,780,1420,1850,2100,2340,2180,1960,2050,2200,2380,2150,1820,1540,1200,980,750,600,480];

window._eventsChart = new Chart(document.getElementById('chart-events'), {
  type:'line',
  data:{
    labels:hours,
    datasets:[{
      data:evts,
      borderColor:'#7F77DD',
      backgroundColor:'rgba(127,119,221,0.08)',
      borderWidth:1.5,
      pointRadius:0,
      tension:0.4,
      fill:true
    }]
  },
  options:{
    responsive:true,
    plugins:{legend:{display:false},tooltip:{enabled:true}},
    scales:{
      x:{ticks:{color:textColor,font:{size:10},maxTicksLimit:8},grid:{color:gridColor}},
      y:{ticks:{color:textColor,font:{size:10}},grid:{color:gridColor}}
    }
  }
});

function initFunnelChart() {
  window._funnelChart = new Chart(document.getElementById('chart-funnel'), {
    type:'bar',
    data:{
      labels:['Page view','Add to cart','Checkout','Purchase'],
      datasets:[{
        data:[100,62,31,14],
        backgroundColor:['#EEEDFE','#AFA9EC','#7F77DD','#534AB7'],
        borderColor:['#7F77DD','#7F77DD','#534AB7','#3C3489'],
        borderWidth:0.5,
        borderRadius:4
      }]
    },
    options:{
      responsive:true,
      plugins:{legend:{display:false}},
      scales:{
        x:{ticks:{color:textColor,font:{size:10}},grid:{display:false}},
        y:{ticks:{color:textColor,font:{size:10},callback:v=>v+'%'},grid:{color:gridColor},max:110}
      }
    }
  });
}
</script>
 · Airflow · dbt · PostgreSQL · MinIO · Docker
[Uploading ecommerce_analytics_dashboard.html…]()
<img width="1366" height="1222" alt="image" src="https://github.com/user-attachments/assets/088fb922-2714-4a80-a0da-445e8bfde243" />

<p align="center">
  <b>Production-grade hybrid Batch + Streaming data engineering platform simulating real-world e-commerce clickstream events.</b><br/>
  <i>End-to-end pipeline — Event Generation → Kafka → Spark → MinIO Data Lake → PostgreSQL → dbt → BI Exports</i>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#️-tech-stack">Tech Stack</a> •
  <a href="#-data-model">Data Model</a> •
  <a href="#-bi-reports">BI Reports</a> •
  <a href="#-engineering-decisions">Engineering Decisions</a>
</p>

</div>

---

## 📊 Platform at a Glance

| Metric | Value |
|:--|:--|
| 👤 Simulated Users | 1,000 (VIP / Regular / New segments) |
| 📡 Event Types | `page_view` · `add_to_cart` · `checkout` · `purchase` · `session` |
| 🗂️ Kafka Partitions | 3 main + 1 Dead Letter Queue |
| 🗄️ Parquet Partitioning | `year / month / day / hour` |
| 🔧 dbt Models | Staging views + 4 mart models |
| 📁 BI CSV Reports | 7 Power BI / Tableau-ready exports |
| ⏰ Orchestration | Hourly 6-stage Airflow DAG |
| 🐳 Docker Services | 6 (Zookeeper, Kafka, Spark, PostgreSQL, MinIO, Airflow) |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        EVENT GENERATION LAYER                        │
│                                                                      │
│   Faker-based Behavioral Simulator                                   │
│   ├── 1,000 synthetic users with segment profiles (VIP/Regular/New) │
│   ├── Funnel-weighted event distribution                             │
│   │     page_view → add_to_cart → checkout → purchase               │
│   └── JSON event payload → Kafka Producer (Linger + GZip batch)     │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                    Kafka Broker (Confluent 7.5.0)
              Topic: ecommerce_events  |  3 partitions
              DLQ:   ecommerce_events_dlq  (corrupt / invalid events)
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                     STREAM PROCESSING LAYER                          │
│                                                                      │
│   PySpark Structured Streaming (3.5.0)                               │
│   ├── Event-time watermarking (late arrival tolerance)               │
│   ├── Schema validation — invalid events → DLQ topic                 │
│   ├── Derived metrics:                                               │
│   │     engagement_score · funnel_stage · session_duration           │
│   └── Partitioned Parquet write → MinIO data lake                   │
│         Partition: year= / month= / day= / hour=                     │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
              MinIO S3-Compatible Data Lake (raw-events/)
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                      BATCH PROCESSING LAYER                          │
│                                                                      │
│   PySpark SQL + JDBC (hourly, triggered by Airflow)                  │
│   ├── dropDuplicates on event_id (idempotent re-run safe)            │
│   └── JDBC bulk load → PostgreSQL staging.stg_events                 │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                PostgreSQL → staging.stg_events
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                    TRANSFORMATION LAYER  (dbt Core 1.7)              │
│                                                                      │
│   Staging Models              Mart Models            Seeds           │
│   ├── stg_events              ├── dim_users           ├── products   │
│   ├── stg_users               ├── dim_products        └── segments   │
│   └── stg_products            ├── dim_date                           │
│                               ├── fct_events (SCD)                   │
│                               └── agg_user_summary                   │
│                                                                      │
│   Tests: unique · not_null · accepted_values · referential integrity │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                    WAREHOUSE LAYER  (Star Schema)                    │
│                                                                      │
│   dim_users ──┐                                                      │
│   dim_products┼──► fct_events ◄── dim_date                          │
│   dim_segments┘         │                                            │
│                         └──► analytics.v_reports (15 SQL queries)   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                         REPORTING LAYER                              │
│                                                                      │
│   Pandas CSV Exporter → data/exports/ → Power BI / Tableau          │
│   7 business reports: executive · daily sales · products ·           │
│   categories · user segments · conversion funnel · hourly traffic   │
└──────────────────────────────────────────────────────────────────────┘

  Orchestration: Apache Airflow 2.7 — hourly 6-stage DAG with retry handling
  Infrastructure: Docker Compose — single-command full stack deployment
```

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|:--|:--|:--|:--|
| **Language** | Python · SQL | 3.10 | Core pipeline scripting and analytics |
| **Message Broker** | Apache Kafka + Zookeeper | 7.5.0 | Decoupled high-velocity streaming commit log |
| **Stream Processing** | PySpark Structured Streaming | 3.5.0 | Real-time event consumption and Parquet writes |
| **Batch Processing** | PySpark SQL + JDBC | 3.5.0 | Hourly deduplication and warehouse loading |
| **Data Lake** | MinIO (S3-compatible) | Latest | Local cloud-style object storage for raw Parquet |
| **Data Warehouse** | PostgreSQL | 15 | Star schema OLAP relational storage |
| **Transformation** | dbt Core | 1.7.2 | Staging, mart models, tests, and lineage docs |
| **Orchestration** | Apache Airflow | 2.7.3 | Scheduled DAG execution, retries, monitoring |
| **Infrastructure** | Docker + Docker Compose | Latest | Fully containerized single-command deployment |

---

## ⚡ Quick Start

> **Prerequisites:** Docker Desktop · Git Bash or a Unix-compatible terminal

### 1. Clone the repository
```bash
git clone https://github.com/syedwaseem106/Real-Time-E-Commerce-Analytics-Platform.git
cd Real-Time-E-Commerce-Analytics-Platform
```

### 2. Bootstrap the full platform
```bash
./scripts/setup.sh
```
Builds all custom Docker images and spins up Zookeeper, Kafka, MinIO, Spark, PostgreSQL, and Airflow. Creates Kafka topics, initializes the database schema, and seeds 1,000 synthetic users, a 2024–2026 date spine, and the product catalog.

### 3. Run the end-to-end pipeline
```bash
./scripts/run_pipeline.sh
```
Launches Structured Streaming, generates clickstream traffic, runs Spark batch deduplication, executes dbt builds, loads surrogate fact keys into PostgreSQL, and exports all 7 BI reports to `data/exports/`.


## 📁 Project Structure

```
real-time-ecommerce-analytics/
│
├── docker-compose.yml               # Full 6-service orchestration
├── .env                             # Credentials and port configuration
├── Makefile                         # CLI shortcuts (make setup, make run, etc.)
├── requirements.txt                 # Python dependencies
│
├── scripts/
│   ├── setup.sh                     # Bootstrap all containers + seed data
│   ├── run_pipeline.sh              # End-to-end pipeline trigger
│   └── teardown.sh                  # Clean shutdown and volume reset
│
├── docker/
│   ├── spark/Dockerfile             # PySpark image with MinIO S3 connectors
│   ├── kafka/init-topics.sh         # Creates ecommerce_events + DLQ topics
│   └── postgres/init.sql            # PostgreSQL schema initialization
│
├── airflow/
│   ├── Dockerfile                   # Custom Airflow image
│   └── dags/
│       └── ecommerce_pipeline_dag.py  # 6-stage hourly orchestration DAG
│
├── src/
│   ├── event_generator/
│   │   ├── config.py                # Funnel distributions, product catalog
│   │   ├── generator.py             # Faker-based clickstream constructor
│   │   └── kafka_producer.py        # Kafka publisher with GZip batching
│   │
│   ├── spark/
│   │   ├── streaming_consumer.py    # Structured Streaming engine
│   │   ├── batch_processor.py       # Hourly deduplication Spark job
│   │   └── transformations.py       # Derived metrics, time dimensions
│   │
│   ├── warehouse/
│   │   ├── schema.sql               # PostgreSQL DDL (PKs, FKs, indexes)
│   │   ├── models.py                # SQLAlchemy ORM mappings
│   │   ├── seed_dimensions.py       # Seeds 1,000 users + date spine + products
│   │   └── load_facts.py            # Surrogate key resolution + fact load
│   │
│   ├── quality/
│   │   ├── validators.py            # Payload schema + business rule checks
│   │   └── filters.py               # Deduplication and outlier removal
│   │
│   └── analytics/
│       ├── queries.sql              # 15 advanced analytical SQL queries
│       ├── create_views.sql         # BI reporting view DDL
│       └── export_csv.py            # Pandas CSV export script
│
├── dbt_project/
│   ├── dbt_project.yml              # Materialization config
│   ├── profiles.yml                 # Dev/Prod PostgreSQL profiles
│   ├── models/
│   │   ├── staging/                 # stg_events, stg_users, stg_products
│   │   ├── marts/                   # dim_*, fct_events, agg_user_summary
│   │   └── schema.yml               # Model tests, docs, and metadata
│   ├── macros/                      # Custom Jinja macros
│   ├── tests/                       # Custom dbt data assertions
│   └── seeds/                       # Product catalog and segment CSVs
│
└── data/
    ├── sample/                      # Sample event JSON payloads
    └── exports/                     # BI-ready CSV output folder
```

---

## 🗄️ Data Model — Star Schema

### Dimension Tables

| Table | Key Columns | Description |
|:--|:--|:--|
| `dim_users` | `user_id (PK)`, `segment`, `created_at` | 1,000 synthetic users with VIP / Regular / New segments |
| `dim_products` | `product_id (PK)`, `category`, `price` | 50+ products across categories |
| `dim_date` | `date_id (PK)`, `year`, `month`, `week`, `day_of_week` | Full 2024–2026 date spine |
| `dim_segments` | `segment_id (PK)`, `segment_name`, `tier` | User tier classifications |

### Fact Table — `fct_events`

| Column | Type | Notes |
|:--|:--|:--|
| `event_id` | `VARCHAR (PK)` | Deduplicated unique event identifier |
| `user_id` | `INT (FK)` | Resolves to `dim_users` surrogate key |
| `product_id` | `INT (FK)` | Resolves to `dim_products` surrogate key |
| `date_id` | `INT (FK)` | Resolves to `dim_date` surrogate key |
| `event_type` | `VARCHAR` | `page_view` / `add_to_cart` / `checkout` / `purchase` |
| `session_id` | `VARCHAR` | Groups events into user sessions |
| `quantity` | `INT` | Units per transaction event |
| `revenue` | `DOUBLE PRECISION` | Derived: `quantity × product price` |
| `funnel_stage` | `INT` | 1–4 numeric funnel position |
| `created_at` | `TIMESTAMP` | Event timestamp with timezone |

---

## 📈 BI Report Exports

After `run_pipeline.sh` completes, Power BI / Tableau-ready CSVs land in `data/exports/`:

| Report File | Description |
|:--|:--|
| `executive_summary_report.csv` | Gross revenue, visits, transaction counts, and basket sizes |
| `daily_sales_report.csv` | Order volume, daily revenue, units sold, and day-over-day growth |
| `product_performance_report.csv` | Units sold, views, and revenue per product |
| `category_revenue_report.csv` | Revenue aggregated by product category |
| `user_segments_report.csv` | Spend metrics segmented by user tier (VIP, Regular, New) |
| `conversion_funnel_report.csv` | Drop-off rates across browse → cart → checkout → payment |
| `hourly_traffic_report.csv` | Active session volume by hour of day |

---

## 🔍 SQL Analytics — Sample Query

15 analytical queries live in `src/analytics/queries.sql`, covering funnel drop-off, revenue by segment, hourly traffic peaks, product conversion rates, repeat purchase analysis, and day-over-day growth.

```sql
-- Conversion funnel drop-off analysis
SELECT
    funnel_stage,
    event_type,
    COUNT(*)                                             AS event_count,
    ROUND(
        100.0 * COUNT(*) / FIRST_VALUE(COUNT(*)) OVER (
            ORDER BY funnel_stage
        ), 2
    )                                                    AS funnel_pct
FROM fct_events
GROUP BY funnel_stage, event_type
ORDER BY funnel_stage;
```

---

## 🔒 Data Quality & Observability

| Practice | Implementation |
|:--|:--|
| **Schema Validation** | Enforces required fields, non-null user keys, and valid quantities on every Kafka event |
| **Dead Letter Queue** | Malformed or out-of-range events route to `ecommerce_events_dlq` — main pipeline stays clean |
| **Idempotency** | Spark deduplicates on `event_id`; fact loader uses `LEFT JOIN` guard to block duplicate inserts on re-run |
| **dbt Tests** | `unique`, `not_null`, `accepted_values`, and referential integrity tests on every model build |
| **Structured Logging** | JSON logs with `pipeline_name`, `step`, `row_count`, and `duration_seconds` on every job execution |

---

## 💡 Engineering Decisions

<details>
<summary><b>Why Kafka over writing directly to the database?</b></summary>

Kafka decouples producers from consumers, absorbs traffic spikes without data loss, and enables event replay for late arrivals or pipeline failures — critical for at-least-once delivery guarantees.
</details>

<details>
<summary><b>Why Parquet partitioned by time on MinIO?</b></summary>

Columnar Parquet with `year/month/day/hour` partitioning enables partition pruning in both Spark Streaming writes and hourly batch reads, cutting scan cost as data volume grows.
</details>

<details>
<summary><b>Why dbt for transformations instead of raw SQL scripts?</b></summary>

Version-controlled, testable, self-documenting models with full lineage graphs. Staging → mart separation mirrors how professional data teams manage transformation layers. dbt tests catch data contract breaks automatically.
</details>

<details>
<summary><b>Why MinIO instead of a real S3 bucket?</b></summary>

Identical S3-compatible API at zero cost. The same Spark S3A connector and boto3 code runs unchanged when deployed to AWS — no production code changes needed.
</details>

<details>
<summary><b>Why surrogate key resolution on fact load?</b></summary>

Natural keys (user email, product SKU) change over time. Surrogate integer keys resolve this and enable SCD (Slowly Changing Dimension) tracking in dbt mart models.
</details>

---

## 🗺️ Planned Enhancements

- [ ] AWS S3 as production data lake (replace MinIO for cloud deployment)
- [ ] Redshift or Snowflake as cloud warehouse
- [ ] Incremental dbt models (process only new hourly partitions)
- [ ] Data quality checks with Great Expectations
- [ ] CI/CD pipeline with GitHub Actions for dbt test automation
- [ ] Grafana dashboard wired to PostgreSQL for live pipeline monitoring
- [ ] Kafka Schema Registry with Avro for enforced event contracts

---

## 👤 Author

<table>
  <tr>
    <td align="center">
      <b>Syed Waseem</b><br/>
      AWS Certified Data Engineer Associate (DEA-C01)<br/>
      <a href="https://github.com/syedwaseem106">GitHub</a> ·
      <a href="<a href="https://linkedin.com/in/syed-waseem-i-b61132216">LinkedIn</a>"></a>
    </td>
  </tr>
</table>

---

## 📄 License

This project is licensed under the **MIT License** — contributions and pull requests are welcome.

---

<div align="center">
  <sub>Built with ❤️ using Apache Kafka · Spark · Airflow · dbt · PostgreSQL · MinIO · Docker</sub>
</div>
