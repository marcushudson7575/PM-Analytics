import Logo from '@/components/Logo';
import MetricCard from '@/components/MetricCard';
import Charts from '@/components/Charts';
import FundTable from '@/components/FundTable';
import { mockFunds, dashboardMetrics, strategyData, vintageYearData } from '@/data/mockData';

export default function Home() {
  const formatCurrency = (value: number): string => {
    if (value >= 1_000_000_000) {
      return `$${(value / 1_000_000_000).toFixed(1)}B`;
    }
    return `$${(value / 1_000_000).toFixed(1)}M`;
  };

  return (
    <main className="min-h-screen p-4 md:p-8 max-w-7xl mx-auto">
      {/* Logo Header */}
      <Logo />

      {/* Key Metrics */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <span>📈</span>
          Key Metrics
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            label="Total Funds"
            value={dashboardMetrics.total_funds}
            helpText="Number of funds in database with ≥95% confidence"
          />
          <MetricCard
            label="Total AUM"
            value={formatCurrency(dashboardMetrics.total_aum_usd)}
            helpText="Total Assets Under Management across all funds"
          />
          <MetricCard
            label="Avg Fund Size"
            value={formatCurrency(dashboardMetrics.avg_fund_size_usd)}
            helpText="Average fund size across all strategies"
          />
          <MetricCard
            label="Data Quality"
            value={`${dashboardMetrics.data_quality_pct}%`}
            helpText="Percentage of funds with high confidence scores"
          />
        </div>
      </div>

      {/* Charts */}
      <Charts strategyData={strategyData} vintageData={vintageYearData} />

      {/* Fund Table */}
      <FundTable funds={mockFunds} />

      {/* Footer */}
      <footer className="mt-12 py-8 border-t border-gray-700 text-center">
        <p className="text-white font-semibold text-lg mb-2">PM Analytics - Private Markets Data Platform</p>
        <p className="text-gray-400 text-sm mb-1">
          Data sourced from authoritative regulatory filings and public disclosures
        </p>
        <p className="text-gray-500 text-xs">
          Only displaying funds with ≥95% confidence scores
        </p>
      </footer>
    </main>
  );
}
