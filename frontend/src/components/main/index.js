import React from "react";
import styles from "./style.module.css";
import cn from "classnames";

const Main = ({ children, withBG, asFlex, className }) => {
  return (
    <main
      className={cn(styles.main, className, {
        [styles.mainBG]: withBG,
        [styles.asFlex]: asFlex,
      })}
    >
      {children}
    </main>
  );
};

export default Main;
