import * as React from "react"

const PaginationArrow = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={7}
    height={12}
    fill="none"
    {...props}
  >
    <path
      stroke="#fff"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M5.466 10.4 1.066 6l4.4-4.4"
    />
  </svg>
)

export default PaginationArrow