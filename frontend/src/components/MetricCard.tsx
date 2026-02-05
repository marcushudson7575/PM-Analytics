interface MetricCardProps {
  label: string;
  value: string | number;
  helpText?: string;
}

export default function MetricCard({ label, value, helpText }: MetricCardProps) {
  return (
    <div className="bg-pm-navy/50 backdrop-blur-sm border border-gray-700 rounded-lg p-6 hover:border-pm-blue transition-colors">
      <div className="flex items-center gap-2 mb-2">
        <p className="text-sm text-gray-400 uppercase tracking-wide">{label}</p>
        {helpText && (
          <div className="group relative">
            <svg
              className="w-4 h-4 text-gray-500 cursor-help"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div className="absolute hidden group-hover:block bg-gray-900 text-white text-xs rounded py-1 px-2 -top-8 left-0 whitespace-nowrap z-10">
              {helpText}
            </div>
          </div>
        )}
      </div>
      <p className="text-3xl md:text-4xl font-bold text-white">{value}</p>
    </div>
  );
}
