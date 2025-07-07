import * as React from "react"

const Cart = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={24}
    height={24}
    fill="none"
    {...props}
  >
    <path
      stroke="#14181F"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.5}
      d="M6.667 3 4 6.6v12.6c0 .477.187.935.52 1.273.334.337.786.527 1.258.527h12.444c.472 0 .924-.19 1.257-.527.334-.338.521-.796.521-1.273V6.6L17.333 3H6.667ZM4 7h16"
    />
    <path
      stroke="#14181F"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.5}
      d="M16 11a4 4 0 1 1-8 0"
    />
  </svg>
)

export default Cart