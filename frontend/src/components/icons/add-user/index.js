import * as React from "react"

const AddUserIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={18}
    height={24}
    fill="none"
    {...props}
  >
    <g
      stroke="#000"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.6}
      clipPath="url(#Minus_L_svg__a)"
    >
      <path d="M6 18c0-1.473 2.09-3 4.667-3s4.666 1.527 4.666 3M3 15.334v-4M1 13.334h4M10.667 12.667a3.333 3.333 0 1 0 0-6.667 3.333 3.333 0 0 0 0 6.667Z" />
    </g>
    <defs>
      <clipPath id="Minus_L_svg__a">
        <path fill="#fff" d="M0 0h18v24H0z" />
      </clipPath>
    </defs>
  </svg>
)

export default AddUserIcon