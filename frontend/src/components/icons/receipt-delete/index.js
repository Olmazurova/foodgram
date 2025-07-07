import * as React from "react"

const SvgBin = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={24}
    height={24}
    fill="none"
    {...props}
  >
    <path
      stroke="#A0A0A0"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.5}
      d="M8.571 7V4.8c0-.477.181-.935.503-1.273A1.674 1.674 0 0 1 10.286 3h3.428c.455 0 .891.19 1.213.527.321.338.502.796.502 1.273V7M19 7l-1 12.2c0 .477-.18.935-.502 1.273a1.674 1.674 0 0 1-1.212.527H7.714c-.454 0-.89-.19-1.212-.527A1.847 1.847 0 0 1 6 19.2L5 7h14ZM4 7h16M10 11v5M14 11v5"
    />
  </svg>
)

export default SvgBin