import * as React from "react";
const SvgVector = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={22}
    height={28}
    fill="none"
    {...props}
  >
    <path
      fill="#000"
      stroke="#000"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.5}
      d="M20.916 26.75 11 19.667 1.083 26.75V4.083A2.833 2.833 0 0 1 3.916 1.25h14.167a2.833 2.833 0 0 1 2.833 2.833V26.75Z"
    />
  </svg>
);
export default SvgVector;