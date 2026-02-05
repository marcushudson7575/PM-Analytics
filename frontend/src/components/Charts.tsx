'use client';

import { StrategyData, VintageYearData } from '@/types';

interface ChartsProps {
  strategyData: StrategyData[];
  vintageData: VintageYearData[];
}

export default function Charts({ strategyData, vintageData }: ChartsProps) {
  const colors = ['#93c5fd', '#60a5fa', '#3b82f6', '#ef4444'];

  return (
    <>
      {/* Asset Allocation Section */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <span>📊</span>
          Asset Allocation
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* AUM Distribution - Donut Chart */}
          <div className="bg-pm-navy/30 backdrop-blur-sm border border-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">AUM Distribution by Strategy</h3>
            <div className="flex items-center justify-center h-64">
              <div className="relative w-48 h-48">
                <svg viewBox="0 0 200 200" className="transform -rotate-90">
                  {(() => {
                    let cumulativePercent = 0;
                    return strategyData.map((item, index) => {
                      const percent = item.percentage;
                      const offset = cumulativePercent * 2.51327; // Circumference for radius 40 (with hole)
                      const strokeDasharray = `${percent * 2.51327} ${251.327}`;
                      cumulativePercent += percent;

                      return (
                        <circle
                          key={item.strategy}
                          cx="100"
                          cy="100"
                          r="40"
                          fill="none"
                          stroke={colors[index % colors.length]}
                          strokeWidth="30"
                          strokeDasharray={strokeDasharray}
                          strokeDashoffset={-offset}
                        />
                      );
                    });
                  })()}
                </svg>
              </div>
            </div>
            <div className="mt-4 space-y-2">
              {strategyData.map((item, index) => (
                <div key={item.strategy} className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-sm"
                      style={{ backgroundColor: colors[index % colors.length] }}
                    />
                    <span className="text-gray-300">{item.strategy}</span>
                  </div>
                  <span className="text-white font-semibold">{item.percentage.toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Fund Count by Strategy - Bar Chart */}
          <div className="bg-pm-navy/30 backdrop-blur-sm border border-gray-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Number of Funds by Strategy</h3>
            <div className="flex items-end justify-around h-64 px-4">
              {strategyData.map((item, index) => {
                const maxCount = Math.max(...strategyData.map(d => d.fund_count));
                const height = (item.fund_count / maxCount) * 100;

                return (
                  <div key={item.strategy} className="flex flex-col items-center gap-2 flex-1 max-w-[100px]">
                    <div className="text-white font-bold text-lg">{item.fund_count}</div>
                    <div
                      className="w-full rounded-t-lg transition-all hover:opacity-80"
                      style={{
                        height: `${height}%`,
                        backgroundColor: colors[index % colors.length],
                        minHeight: '20px'
                      }}
                    />
                    <div className="text-xs text-gray-400 text-center mt-2 leading-tight">
                      {item.strategy}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Vintage Year Analysis */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <span>📅</span>
          Vintage Year Analysis
        </h2>

        <div className="bg-pm-navy/30 backdrop-blur-sm border border-gray-700 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Funds by Vintage Year</h3>
          <div className="flex items-end justify-around h-80 px-8">
            {vintageData.map((item) => {
              const maxCount = Math.max(...vintageData.map(d => d.fund_count));
              const height = (item.fund_count / maxCount) * 100;
              const maxAum = Math.max(...vintageData.map(d => d.total_aum_usd));
              const aumHeight = (item.total_aum_usd / maxAum) * 50; // Scale for line overlay

              return (
                <div key={item.year} className="flex flex-col items-center gap-2 flex-1 max-w-[150px] relative">
                  <div className="text-white font-bold text-sm">
                    ${(item.total_aum_usd / 1_000_000_000).toFixed(0)}B
                  </div>
                  <div className="text-pm-blue-light font-semibold">{item.fund_count}</div>
                  <div
                    className="w-full bg-pm-blue-lighter rounded-t-lg transition-all hover:opacity-80"
                    style={{
                      height: `${height}%`,
                      minHeight: '30px'
                    }}
                  />
                  <div className="text-sm text-gray-300 font-medium mt-2">{item.year}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </>
  );
}
