import * as React from "react"

const SvgCloseS = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={18}
    height={19}
    fill="none"
    {...props}
  >
    <path
      stroke="#000"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.4}
      d="M14 14.5 4 4.5M14 4.5l-10 10"
    />
  </svg>
);
export default SvgCloseS;