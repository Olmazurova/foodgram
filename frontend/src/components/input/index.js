import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import styles from "./styles.module.css";
import cn from "classnames";

const Input = ({
  onChange,
  placeholder,
  label,
  type = "text",
  inputClassName,
  labelClassName,
  className,
  name,
  required,
  onFocus,
  onBlur,
  isAuth,
  error,
  submitError,
  value = "",
  ...rest
}) => {
  const [inputValue, setInputValue] = useState(value);

  const errorText = (error && error[name]) || submitError?.submitError;

  const handleValueChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    onChange(e);
  };
  useEffect(() => {
    if (value !== inputValue) {
      setInputValue(value);
    }
  }, [value]);

  return (
    <div className={cn(styles.input, className)}>
      <label className={cn(styles.inputLabel, { [styles.auth]: isAuth })}>
        {label && (
          <div className={cn(styles.inputLabelText, labelClassName)}>
            {label}
          </div>
        )}
        <input
          type={type}
          placeholder={placeholder}
          required={required}
          name={name}
          className={cn(styles.inputField, inputClassName, {
            [styles.inputError]: errorText,
          })}
          onChange={(e) => {
            handleValueChange(e);
          }}
          onFocus={onFocus}
          value={inputValue}
          onBlur={onBlur}
          {...rest}
        />
        {errorText && (
          <div className={styles.errorBox}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="15"
              height="14"
              viewBox="0 0 15 14"
              fill="none"
            >
              <g clip-path="url(#clip0_101_848)">
                <circle cx="7.5" cy="7" r="7" fill="#FF3B30" />
                <path
                  d="M5.85008 5.35011L7.5 7.00003M7.5 7.00003L9.14992 8.64994M7.5 7.00003L5.85008 8.64994M7.5 7.00003L9.14992 5.35011"
                  stroke="white"
                  stroke-width="1.2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </g>
              <defs>
                <clipPath id="clip0_101_848">
                  <rect
                    width="14"
                    height="14"
                    fill="white"
                    transform="translate(0.5)"
                  />
                </clipPath>
              </defs>
            </svg>
            <p className={styles.error}>{errorText}</p>
          </div>
        )}
      </label>
    </div>
  );
};

export default Input;
