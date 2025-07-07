import Icons from "../icons";
import styles from "./style.module.css";
import cn from "classnames";

export const Notification = ({ text, className, onClose, ...rest }) => {
  return (
    <div className={cn(styles.container, className)} {...rest}>
      <p className={styles.text}>{text}</p>
      {onClose && (
        <button className={styles.closeBtn} onClick={onClose}>
          <Icons.PopupClose />
        </button>
      )}
    </div>
  );
};
