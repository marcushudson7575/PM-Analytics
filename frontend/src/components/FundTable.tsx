'use client';

import { Fund } from '@/types';
import { useState } from 'react';

interface FundTableProps {
  funds: Fund[];
}

export default function FundTable({ funds }: FundTableProps) {
  const [selectedStrategy, setSelectedStrategy] = useState<string>('All');

  const strategies = ['All', ...Array.from(new Set(funds.map(f => f.strategy)))];

  const filteredFunds = selectedStrategy === 'All'
    ? funds
    : funds.filter(f => f.strategy === selectedStrategy);

  const formatCurrency = (value: number): string => {
    if (value >= 1_000_000_000) {
      return `$${(value / 1_000_000_000).toFixed(1)}B`;
    }
    return `$${(value / 1_000_000).toFixed(1)}M`;
  };

  return (
    <div className="bg-pm-navy/30 backdrop-blur-sm border border-gray-700 rounded-lg p-6">
      <div className="flex items-center gap-4 mb-6">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>📋</span>
          Fund Database
        </h2>
        <div className="ml-auto">
          <label className="text-sm text-gray-400 mr-2">Filter by Strategy</label>
          <select
            value={selectedStrategy}
            onChange={(e) => setSelectedStrategy(e.target.value)}
            className="bg-pm-dark border border-gray-600 text-white px-4 py-2 rounded-lg focus:outline-none focus:border-pm-blue"
          >
            {strategies.map(strategy => (
              <option key={strategy} value={strategy}>{strategy}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="text-left py-3 px-4 text-gray-400 font-semibold text-sm">Name</th>
              <th className="text-left py-3 px-4 text-gray-400 font-semibold text-sm">Strategy</th>
              <th className="text-left py-3 px-4 text-gray-400 font-semibold text-sm">Vintage Year</th>
              <th className="text-left py-3 px-4 text-gray-400 font-semibold text-sm">Geography</th>
              <th className="text-left py-3 px-4 text-gray-400 font-semibold text-sm">Fund Size</th>
              <th className="text-left py-3 px-4 text-gray-400 font-semibold text-sm">Confidence</th>
              <th className="text-left py-3 px-4 text-gray-400 font-semibold text-sm">Source</th>
            </tr>
          </thead>
          <tbody>
            {filteredFunds.map((fund) => (
              <tr key={fund.id} className="border-b border-gray-800 hover:bg-pm-navy/30 transition-colors">
                <td className="py-3 px-4 text-white">{fund.name}</td>
                <td className="py-3 px-4 text-gray-300">{fund.strategy}</td>
                <td className="py-3 px-4 text-gray-300">{fund.vintage_year}</td>
                <td className="py-3 px-4 text-gray-300">{fund.geography}</td>
                <td className="py-3 px-4 text-gray-300">{formatCurrency(fund.fund_size_usd)}</td>
                <td className="py-3 px-4 text-gray-300">{(fund.data_confidence_score * 100).toFixed(0)}%</td>
                <td className="py-3 px-4 text-gray-300 text-sm">{fund.data_source}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-sm text-gray-400 mt-4">
        Showing {filteredFunds.length} of {funds.length} total funds
      </p>
    </div>
  );
}
