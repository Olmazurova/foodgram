import * as React from "react";
const SvgIndex = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={12}
    height={14}
    fill="none"
    {...props}
  >
    <g
      stroke="#14181F"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.5}
      clipPath="url(#index_svg__a)"
    >
      <path d="M1.195 5.236a3.788 3.788 0 0 1 1.11-1.57 4.066 4.066 0 0 1 1.77-.864 4.188 4.188 0 0 1 1.989.056 4.036 4.036 0 0 1 1.712.962l2.057 1.837M1.166 7.343 3.222 9.18a4.037 4.037 0 0 0 1.713.963 4.188 4.188 0 0 0 1.989.055 4.066 4.066 0 0 0 1.77-.864 3.789 3.789 0 0 0 1.11-1.57" />
      <path d="M9.941 3.034v2.708H7.233M1.112 9.967V7.258h2.709" />
    </g>
    <defs>
      <clipPath id="index_svg__a">
        <path fill="#fff" d="M0 0h12v14H0z" />
      </clipPath>
    </defs>
  </svg>
);
export default SvgIndex;