import React from 'react';

export const BrainGraphic: React.FC<{ className?: string }> = ({ className = "w-48 h-28" }) => {
  return (
    <div className={`relative flex items-center justify-center ${className}`}>
      <svg
        viewBox="0 0 260 150"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full filter drop-shadow-[0_0_16px_rgba(255,138,0,0.55)]"
      >
        <defs>
          <linearGradient id="brainGlow" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FFA733" />
            <stop offset="50%" stopColor="#FF8A00" />
            <stop offset="100%" stopColor="#D97500" />
          </linearGradient>
          <radialGradient id="coreLight" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FF8A00" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#FF8A00" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* Ambient Glow */}
        <ellipse cx="130" cy="75" rx="85" ry="55" fill="url(#coreLight)" />

        {/* Neural Cortex Wireframe Lines */}
        <path
          d="M 50,75 C 45,50 65,25 95,25 C 115,25 125,35 130,42 C 135,35 145,25 165,25 C 195,25 215,50 210,75 C 205,100 185,120 160,120 C 145,120 135,112 130,105 C 125,112 115,120 100,120 C 75,120 55,100 50,75 Z"
          stroke="url(#brainGlow)"
          strokeWidth="1.8"
          strokeDasharray="4 2"
          opacity="0.8"
        />

        {/* Frontal Lobe & Temporal gyri internal contours */}
        <path
          d="M 60,65 Q 85,45 110,65 T 130,68 T 150,65 T 200,65"
          stroke="#FF8A00"
          strokeWidth="1.2"
          opacity="0.75"
        />
        <path
          d="M 65,85 Q 95,70 120,85 T 140,85 T 195,85"
          stroke="#FFA733"
          strokeWidth="1.2"
          opacity="0.7"
        />
        <path
          d="M 80,40 Q 105,55 130,50 T 180,40"
          stroke="#FF8A00"
          strokeWidth="1"
          opacity="0.65"
        />
        <path
          d="M 80,105 Q 105,95 130,100 T 180,105"
          stroke="#FF8A00"
          strokeWidth="1"
          opacity="0.65"
        />
        
        {/* Central Sulcus division */}
        <path
          d="M 130,35 Q 128,60 130,80 Q 132,100 130,115"
          stroke="#FFA333"
          strokeWidth="1.5"
          opacity="0.85"
        />

        {/* Interconnected Synaptic Nodes */}
        {[
          [55, 70], [70, 48], [95, 32], [120, 40], [130, 42], [140, 40], [165, 32], [190, 48], [205, 70],
          [68, 85], [85, 62], [105, 52], [128, 62], [152, 52], [175, 62], [192, 85],
          [80, 105], [105, 82], [115, 98], [130, 80], [145, 98], [155, 82], [180, 105],
          [100, 115], [130, 110], [160, 115]
        ].map(([cx, cy], i) => (
          <g key={i}>
            <circle cx={cx} cy={cy} r="2.2" fill="#FFA333" />
            <circle cx={cx} cy={cy} r="4.5" stroke="#FF8A00" strokeWidth="0.6" opacity="0.4" />
          </g>
        ))}

        {/* Dynamic Synaptic Cross-Connections */}
        <line x1="70" y1="48" x2="85" y2="62" stroke="#FF8A00" strokeWidth="0.8" opacity="0.6" />
        <line x1="85" y1="62" x2="105" y2="52" stroke="#FF8A00" strokeWidth="0.8" opacity="0.6" />
        <line x1="105" y1="52" x2="128" y2="62" stroke="#FF8A00" strokeWidth="0.8" opacity="0.6" />
        <line x1="128" y1="62" x2="152" y2="52" stroke="#FF8A00" strokeWidth="0.8" opacity="0.6" />
        <line x1="152" y1="52" x2="175" y2="62" stroke="#FF8A00" strokeWidth="0.8" opacity="0.6" />
        <line x1="175" y1="62" x2="190" y2="48" stroke="#FF8A00" strokeWidth="0.8" opacity="0.6" />
        <line x1="85" y1="62" x2="105" y2="82" stroke="#FF8A00" strokeWidth="0.8" opacity="0.5" />
        <line x1="105" y1="82" x2="130" y2="80" stroke="#FF8A00" strokeWidth="0.8" opacity="0.6" />
        <line x1="130" y1="80" x2="155" y2="82" stroke="#FF8A00" strokeWidth="0.8" opacity="0.6" />
        <line x1="155" y1="82" x2="175" y2="62" stroke="#FF8A00" strokeWidth="0.8" opacity="0.5" />
      </svg>
    </div>
  );
};
