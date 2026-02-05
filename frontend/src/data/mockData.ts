import { Fund, DashboardMetrics, StrategyData, VintageYearData } from '@/types';

export const mockFunds: Fund[] = [
  {
    id: '1',
    name: 'Blackstone Capital Partners IX',
    strategy: 'Buyout',
    vintage_year: 2022,
    geography: 'Global',
    fund_size_usd: 30_500_000_000,
    data_confidence_score: 0.98,
    data_source: 'blackstone_10k'
  },
  {
    id: '2',
    name: 'Blackstone Real Estate Partners X',
    strategy: 'Real Estate',
    vintage_year: 2023,
    geography: 'Global',
    fund_size_usd: 30_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'blackstone_10k'
  },
  {
    id: '3',
    name: 'Carlyle Partners VIII',
    strategy: 'Buyout',
    vintage_year: 2022,
    geography: 'Global',
    fund_size_usd: 27_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'carlyle_10k'
  },
  {
    id: '4',
    name: 'Apollo Investment Fund X',
    strategy: 'Buyout',
    vintage_year: 2022,
    geography: 'Global',
    fund_size_usd: 25_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'apollo_10k'
  },
  {
    id: '5',
    name: 'KKR Americas Fund XIII',
    strategy: 'Buyout',
    vintage_year: 2022,
    geography: 'North America',
    fund_size_usd: 19_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'kkr_10k'
  },
  {
    id: '6',
    name: 'KKR Global Infrastructure Investors IV',
    strategy: 'Infrastructure',
    vintage_year: 2021,
    geography: 'Global',
    fund_size_usd: 17_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'kkr_10k'
  },
  {
    id: '7',
    name: 'KKR Asian Fund IV',
    strategy: 'Buyout',
    vintage_year: 2021,
    geography: 'Asia-Pacific',
    fund_size_usd: 15_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'kkr_10k'
  },
  {
    id: '8',
    name: 'Blackstone Infrastructure Partners II',
    strategy: 'Infrastructure',
    vintage_year: 2023,
    geography: 'Global',
    fund_size_usd: 15_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'blackstone_10k'
  },
  {
    id: '9',
    name: 'Apollo Infrastructure Opportunity Fund II',
    strategy: 'Infrastructure',
    vintage_year: 2023,
    geography: 'Global',
    fund_size_usd: 12_500_000_000,
    data_confidence_score: 0.98,
    data_source: 'apollo_10k'
  },
  {
    id: '10',
    name: 'Apollo Hybrid Value Fund',
    strategy: 'Private Credit',
    vintage_year: 2021,
    geography: 'Global',
    fund_size_usd: 10_500_000_000,
    data_confidence_score: 0.98,
    data_source: 'apollo_10k'
  },
  {
    id: '11',
    name: 'Brookfield Infrastructure Fund V',
    strategy: 'Infrastructure',
    vintage_year: 2022,
    geography: 'Global',
    fund_size_usd: 20_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'brookfield_filings'
  },
  {
    id: '12',
    name: 'TPG Partners VIII',
    strategy: 'Buyout',
    vintage_year: 2021,
    geography: 'Global',
    fund_size_usd: 14_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'tpg_filings'
  },
  {
    id: '13',
    name: 'Ares Corporate Opportunities Fund VI',
    strategy: 'Private Credit',
    vintage_year: 2022,
    geography: 'North America',
    fund_size_usd: 11_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'ares_10k'
  },
  {
    id: '14',
    name: 'Warburg Pincus Private Equity XIII',
    strategy: 'Buyout',
    vintage_year: 2021,
    geography: 'Global',
    fund_size_usd: 16_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'warburg_filings'
  },
  {
    id: '15',
    name: 'Oaktree Opportunities Fund XI',
    strategy: 'Private Credit',
    vintage_year: 2023,
    geography: 'Global',
    fund_size_usd: 9_000_000_000,
    data_confidence_score: 0.98,
    data_source: 'oaktree_filings'
  }
];

export const dashboardMetrics: DashboardMetrics = {
  total_funds: 15,
  total_aum_usd: 235_500_000_000,
  avg_fund_size_usd: 15_700_000_000,
  data_quality_pct: 100.0
};

export const strategyData: StrategyData[] = [
  { strategy: 'Buyout', aum_usd: 126_500_000_000, fund_count: 6, percentage: 53.7 },
  { strategy: 'Infrastructure', aum_usd: 64_500_000_000, fund_count: 4, percentage: 27.4 },
  { strategy: 'Real Estate', aum_usd: 30_000_000_000, fund_count: 2, percentage: 12.7 },
  { strategy: 'Private Credit', aum_usd: 30_500_000_000, fund_count: 3, percentage: 13.0 }
];

export const vintageYearData: VintageYearData[] = [
  { year: 2021, fund_count: 6, total_aum_usd: 72_500_000_000 },
  { year: 2022, fund_count: 5, total_aum_usd: 107_500_000_000 },
  { year: 2023, fund_count: 4, total_aum_usd: 66_500_000_000 }
];
