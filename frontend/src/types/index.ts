export interface Fund {
  id: string;
  name: string;
  strategy: string;
  vintage_year: number;
  geography: string;
  fund_size_usd: number;
  data_confidence_score: number;
  data_source: string;
}

export interface DashboardMetrics {
  total_funds: number;
  total_aum_usd: number;
  avg_fund_size_usd: number;
  data_quality_pct: number;
}

export interface StrategyData {
  strategy: string;
  aum_usd: number;
  fund_count: number;
  percentage: number;
}

export interface VintageYearData {
  year: number;
  fund_count: number;
  total_aum_usd: number;
}
