import * as React from "react"

const PopupClose = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={14}
    height={14}
    fill="none"
    {...props}
  >
    <path
      stroke="#A0A0A0"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.5}
      d="M13 13 1 1M13 1 1 13"
    />
  </svg>
)

export default PopupClose