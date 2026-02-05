import Image from 'next/image';

export default function Logo() {
  return (
    <div className="bg-pm-navy py-8 px-8 mb-8 rounded-lg shadow-xl">
      <div className="flex items-center gap-4">
        <div className="flex flex-col">
          <h1 className="text-4xl md:text-5xl font-bold text-white tracking-tight">
            Private Markets
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 font-light mt-1">
            Analytics Software
          </p>
        </div>
        <div className="ml-auto hidden md:flex items-center gap-2">
          {/* Chart Icon */}
          <svg
            className="w-16 h-16"
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Rising bars */}
            <rect x="10" y="60" width="15" height="30" fill="#93c5fd" rx="2" />
            <rect x="35" y="45" width="15" height="45" fill="#60a5fa" rx="2" />
            <rect x="60" y="30" width="15" height="60" fill="#3b82f6" rx="2" />
            {/* Trend line */}
            <path
              d="M 5 75 Q 30 60 42.5 52.5 T 70 25 L 95 15"
              stroke="white"
              strokeWidth="3"
              fill="none"
              strokeLinecap="round"
            />
            <circle cx="95" cy="15" r="4" fill="white" />
          </svg>
        </div>
      </div>
    </div>
  );
}
