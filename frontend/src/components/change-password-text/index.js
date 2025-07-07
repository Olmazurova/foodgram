import styles from "./style.module.css";

export const ChangePasswordText = ({ text }) => {
  return (
    <div className={styles.container}>
      <div className={styles.iconBox}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="8"
          height="8"
          viewBox="0 0 8 8"
          fill="none"
        >
          <g clip-path="url(#clip0_101_883)">
            <path
              d="M5.5 7C5.5 7.55228 5.05228 8 4.5 8C3.94772 8 3.5 7.55228 3.5 7C3.5 6.44772 3.94772 6 4.5 6C5.05228 6 5.5 6.44772 5.5 7Z"
              fill="white"
            />
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M4.5 5C3.94771 5 3.5 4.50254 3.5 3.88889L3.5 1.11111C3.5 0.497461 3.94772 -5.08894e-08 4.5 -3.27836e-08C5.05229 -1.46777e-08 5.5 0.497461 5.5 1.11111L5.5 3.88889C5.5 4.50254 5.05228 5 4.5 5Z"
              fill="white"
            />
          </g>
          <defs>
            <clipPath id="clip0_101_883">
              <rect width="8" height="8" fill="white" />
            </clipPath>
          </defs>
        </svg>
      </div>
      <p className={styles.text}>{text}</p>
    </div>
  );
};
